# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

from urllib.parse import parse_qsl

import ragapp
from ragapp import _
from ragapp.twofactor import get_qr_svg_code


def get_context(context):
	context.no_cache = 1
	context.qr_code_user, context.qrcode_svg = get_user_svg_from_cache()


def get_query_key():
	"""Return query string arg."""
	query_string = ragapp.local.request.query_string
	query = dict(parse_qsl(query_string))
	query = {key.decode(): val.decode() for key, val in query.items()}
	if "k" not in list(query):
		ragapp.throw(_("Not Permitted"), ragapp.PermissionError)
	query = (query["k"]).strip()
	if False in [i.isalpha() or i.isdigit() for i in query]:
		ragapp.throw(_("Not Permitted"), ragapp.PermissionError)
	return query


def get_user_svg_from_cache():
	"""Get User and SVG code from cache."""
	key = get_query_key()
	totp_uri = ragapp.cache.get_value(f"{key}_uri")
	user = ragapp.cache.get_value(f"{key}_user")
	if not totp_uri or not user:
		ragapp.throw(_("Page has expired!"), ragapp.PermissionError)
	if not ragapp.db.exists("User", user):
		ragapp.throw(_("Not Permitted"), ragapp.PermissionError)
	user = ragapp.get_doc("User", user)
	svg = get_qr_svg_code(totp_uri)
	return (user, svg.decode())
