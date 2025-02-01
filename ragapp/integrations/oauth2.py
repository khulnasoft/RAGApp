import json
from urllib.parse import quote, urlencode

from oauthlib.oauth2 import FatalClientError, OAuth2Error
from oauthlib.openid.connect.core.endpoints.pre_configured import Server as WebApplicationServer

import ragapp
from ragapp.integrations.doctype.oauth_provider_settings.oauth_provider_settings import (
	get_oauth_settings,
)
from ragapp.oauth import (
	OAuthWebRequestValidator,
	generate_json_error_response,
	get_server_url,
	get_userinfo,
)


def get_oauth_server():
	if not getattr(ragapp.local, "oauth_server", None):
		oauth_validator = OAuthWebRequestValidator()
		ragapp.local.oauth_server = WebApplicationServer(oauth_validator)

	return ragapp.local.oauth_server


def sanitize_kwargs(param_kwargs):
	"""Remove 'data' and 'cmd' keys, if present."""
	arguments = param_kwargs
	arguments.pop("data", None)
	arguments.pop("cmd", None)

	return arguments


def encode_params(params):
	"""
	Encode a dict of params into a query string.

	Use `quote_via=urllib.parse.quote` so that whitespaces will be encoded as
	`%20` instead of as `+`. This is needed because oauthlib cannot handle `+`
	as a whitespace.
	"""
	return urlencode(params, quote_via=quote)


@ragapp.whitelist()
def approve(*args, **kwargs):
	r = ragapp.request

	try:
		(
			scopes,
			ragapp.flags.oauth_credentials,
		) = get_oauth_server().validate_authorization_request(r.url, r.method, r.get_data(), r.headers)

		headers, body, status = get_oauth_server().create_authorization_response(
			uri=ragapp.flags.oauth_credentials["redirect_uri"],
			body=r.get_data(),
			headers=r.headers,
			scopes=scopes,
			credentials=ragapp.flags.oauth_credentials,
		)
		uri = headers.get("Location", None)

		ragapp.local.response["type"] = "redirect"
		ragapp.local.response["location"] = uri
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@ragapp.whitelist(allow_guest=True)
def authorize(**kwargs):
	success_url = "/api/method/ragapp.integrations.oauth2.approve?" + encode_params(sanitize_kwargs(kwargs))
	failure_url = ragapp.form_dict.get("redirect_uri", "") + "?error=access_denied"

	if ragapp.session.user == "Guest":
		# Force login, redirect to preauth again.
		ragapp.local.response["type"] = "redirect"
		ragapp.local.response["location"] = "/login?" + encode_params({"redirect-to": ragapp.request.url})
	else:
		try:
			r = ragapp.request
			(
				scopes,
				ragapp.flags.oauth_credentials,
			) = get_oauth_server().validate_authorization_request(r.url, r.method, r.get_data(), r.headers)

			skip_auth = ragapp.db.get_value(
				"OAuth Client",
				ragapp.flags.oauth_credentials["client_id"],
				"skip_authorization",
			)
			unrevoked_tokens = ragapp.db.exists(
				"OAuth Bearer Token", {"status": "Active", "user": ragapp.session.user}
			)

			if skip_auth or (get_oauth_settings().skip_authorization == "Auto" and unrevoked_tokens):
				ragapp.local.response["type"] = "redirect"
				ragapp.local.response["location"] = success_url
			else:
				if "openid" in scopes:
					scopes.remove("openid")
					scopes.extend(["Full Name", "Email", "User Image", "Roles"])

				# Show Allow/Deny screen.
				response_html_params = ragapp._dict(
					{
						"client_id": ragapp.db.get_value("OAuth Client", kwargs["client_id"], "app_name"),
						"success_url": success_url,
						"failure_url": failure_url,
						"details": scopes,
					}
				)
				resp_html = ragapp.render_template(
					"templates/includes/oauth_confirmation.html", response_html_params
				)
				ragapp.respond_as_web_page(ragapp._("Confirm Access"), resp_html, primary_action=None)
		except (FatalClientError, OAuth2Error) as e:
			return generate_json_error_response(e)


@ragapp.whitelist(allow_guest=True)
def get_token(*args, **kwargs):
	try:
		r = ragapp.request
		headers, body, status = get_oauth_server().create_token_response(
			r.url, r.method, r.form, r.headers, ragapp.flags.oauth_credentials
		)
		body = ragapp._dict(json.loads(body))

		if body.error:
			ragapp.local.response = body
			ragapp.local.response["http_status_code"] = 400
			return

		ragapp.local.response = body
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@ragapp.whitelist(allow_guest=True)
def revoke_token(*args, **kwargs):
	try:
		r = ragapp.request
		headers, body, status = get_oauth_server().create_revocation_response(
			r.url,
			headers=r.headers,
			body=r.form,
			http_method=r.method,
		)
	except (FatalClientError, OAuth2Error):
		pass

	# status_code must be 200
	ragapp.local.response = ragapp._dict({})
	ragapp.local.response["http_status_code"] = status or 200
	return


@ragapp.whitelist()
def openid_profile(*args, **kwargs):
	try:
		r = ragapp.request
		headers, body, status = get_oauth_server().create_userinfo_response(
			r.url,
			headers=r.headers,
			body=r.form,
		)
		body = ragapp._dict(json.loads(body))
		ragapp.local.response = body
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@ragapp.whitelist(allow_guest=True)
def openid_configuration():
	ragapp_server_url = get_server_url()
	ragapp.local.response = ragapp._dict(
		{
			"issuer": ragapp_server_url,
			"authorization_endpoint": f"{ragapp_server_url}/api/method/ragapp.integrations.oauth2.authorize",
			"token_endpoint": f"{ragapp_server_url}/api/method/ragapp.integrations.oauth2.get_token",
			"userinfo_endpoint": f"{ragapp_server_url}/api/method/ragapp.integrations.oauth2.openid_profile",
			"revocation_endpoint": f"{ragapp_server_url}/api/method/ragapp.integrations.oauth2.revoke_token",
			"introspection_endpoint": f"{ragapp_server_url}/api/method/ragapp.integrations.oauth2.introspect_token",
			"response_types_supported": [
				"code",
				"token",
				"code id_token",
				"code token id_token",
				"id_token",
				"id_token token",
			],
			"subject_types_supported": ["public"],
			"id_token_signing_alg_values_supported": ["HS256"],
		}
	)


@ragapp.whitelist(allow_guest=True)
def introspect_token(token=None, token_type_hint=None):
	if token_type_hint not in ["access_token", "refresh_token"]:
		token_type_hint = "access_token"
	try:
		bearer_token = None
		if token_type_hint == "access_token":
			bearer_token = ragapp.get_doc("OAuth Bearer Token", {"access_token": token})
		elif token_type_hint == "refresh_token":
			bearer_token = ragapp.get_doc("OAuth Bearer Token", {"refresh_token": token})

		client = ragapp.get_doc("OAuth Client", bearer_token.client)

		token_response = ragapp._dict(
			{
				"client_id": client.client_id,
				"trusted_client": client.skip_authorization,
				"active": bearer_token.status == "Active",
				"exp": round(bearer_token.expiration_time.timestamp()),
				"scope": bearer_token.scopes,
			}
		)

		if "openid" in bearer_token.scopes:
			sub = ragapp.get_value(
				"User Social Login",
				{"provider": "ragapp", "parent": bearer_token.user},
				"userid",
			)

			if sub:
				token_response.update({"sub": sub})
				user = ragapp.get_doc("User", bearer_token.user)
				userinfo = get_userinfo(user)
				token_response.update(userinfo)

		ragapp.local.response = token_response

	except Exception:
		ragapp.local.response = ragapp._dict({"active": False})
