import requests

import ragapp
from ragapp import _


def get_base_url():
	url = "https://ragappcloud.com"
	if ragapp.conf.developer_mode and ragapp.conf.get("saas_billing_base_url"):
		url = ragapp.conf.get("saas_billing_base_url")
	return url


def get_site_name():
	site_name = ragapp.local.site
	if ragapp.conf.developer_mode and ragapp.conf.get("saas_billing_site_name"):
		site_name = ragapp.conf.get("saas_billing_site_name")
	return site_name


def get_headers():
	# check if user is system manager
	if ragapp.get_roles(ragapp.session.user).count("System Manager") == 0:
		ragapp.throw(_("You are not allowed to access this resource"))

	# check if communication secret is set
	if not ragapp.conf.get("fc_communication_secret"):
		ragapp.throw(_("Communication secret not set"))

	return {
		"X-Site-Token": ragapp.conf.get("fc_communication_secret"),
		"X-Site": get_site_name(),
	}


@ragapp.whitelist()
def get_token_and_base_url():
	request = requests.post(
		f"{get_base_url()}/api/method/press.saas.api.auth.generate_access_token",
		headers=get_headers(),
	)
	if request.status_code == 200:
		return {
			"base_url": get_base_url(),
			"token": request.json()["message"],
		}
	else:
		ragapp.throw(_("Failed to generate access token"))


@ragapp.whitelist()
def is_access_token_valid(token):
	headers = {"Content-Type": "application/json"}
	request = requests.post(
		f"{get_base_url()}/api/method/press.saas.api.auth.is_access_token_valid",
		headers,
		json={token},
	)
	return request.json()["message"]


@ragapp.whitelist()
def current_site_info():
	request = requests.post(f"{get_base_url()}/api/method/press.saas.api.site.info", headers=get_headers())
	if request.status_code == 200:
		return request.json().get("message")
	else:
		ragapp.throw(_("Failed to get site info"))


@ragapp.whitelist()
def api(method, data=None):
	if data is None:
		data = {}
	request = requests.post(
		f"{get_base_url()}/api/method/press.saas.api.{method}",
		headers=get_headers(),
		json=data,
	)
	if request.status_code == 200:
		return request.json().get("message")
	else:
		ragapp.throw(_("Failed while calling API {0}", method))


@ragapp.whitelist()
def is_fc_site():
	is_system_manager = ragapp.get_roles(ragapp.session.user).count("System Manager")
	setup_completed = ragapp.get_system_settings("setup_complete")
	return is_system_manager and setup_completed and ragapp.conf.get("fc_communication_secret")


# login to ragapp cloud dashboard
@ragapp.whitelist()
def send_verification_code():
	request = requests.post(
		f"{get_base_url()}/api/method/press.api.developer.saas.request_login_to_fc",
		headers=get_headers(),
		json={"domain": get_site_name()},
	)
	if request.status_code == 200:
		return request.json().get("message")
	else:
		ragapp.throw(_("Failed to request login to Ragapp Cloud"))


@ragapp.whitelist()
def verify_and_login(verification_code: str):
	request = requests.post(
		f"{get_base_url()}/api/method/press.api.developer.saas.validate_login_to_fc",
		headers=get_headers(),
		json={"domain": get_site_name(), "otp": verification_code},
	)

	if request.status_code == 200:
		return {
			"base_url": get_base_url(),
			"login_token": request.json()["login_token"],
		}
	else:
		ragapp.throw(_("Invalid Code. Please try again."))
