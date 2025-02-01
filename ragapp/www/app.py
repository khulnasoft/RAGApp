# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import os

no_cache = 1

import json
import re
from urllib.parse import urlencode

import ragapp
import ragapp.sessions
from ragapp import _
from ragapp.utils.jinja_globals import is_rtl

SCRIPT_TAG_PATTERN = re.compile(r"\<script[^<]*\</script\>")
CLOSING_SCRIPT_TAG_PATTERN = re.compile(r"</script\>")


def get_context(context):
	if ragapp.session.user == "Guest":
		ragapp.response["status_code"] = 403
		ragapp.msgprint(_("Log in to access this page."))
		ragapp.redirect(f"/login?{urlencode({'redirect-to': ragapp.request.path})}")

	elif ragapp.session.data.user_type == "Website User":
		ragapp.throw(_("You are not permitted to access this page."), ragapp.PermissionError)

	try:
		boot = ragapp.sessions.get()
	except Exception as e:
		raise ragapp.SessionBootFailed from e

	# this needs commit
	csrf_token = ragapp.sessions.get_csrf_token()

	ragapp.db.commit()

	hooks = ragapp.get_hooks()
	app_include_js = hooks.get("app_include_js", []) + ragapp.conf.get("app_include_js", [])
	app_include_css = hooks.get("app_include_css", []) + ragapp.conf.get("app_include_css", [])
	app_include_icons = hooks.get("app_include_icons", [])

	if ragapp.get_system_settings("enable_telemetry") and os.getenv("RAGAPP_SENTRY_DSN"):
		app_include_js.append("sentry.bundle.js")

	context.update(
		{
			"no_cache": 1,
			"build_version": ragapp.utils.get_build_version(),
			"app_include_js": app_include_js,
			"app_include_css": app_include_css,
			"app_include_icons": app_include_icons,
			"layout_direction": "rtl" if is_rtl() else "ltr",
			"lang": ragapp.local.lang,
			"sounds": hooks["sounds"],
			"boot": boot,
			"desk_theme": boot.get("desk_theme") or "Light",
			"csrf_token": csrf_token,
			"google_analytics_id": ragapp.conf.get("google_analytics_id"),
			"google_analytics_anonymize_ip": ragapp.conf.get("google_analytics_anonymize_ip"),
			"app_name": (
				ragapp.get_website_settings("app_name") or ragapp.get_system_settings("app_name") or "Ragapp"
			),
		}
	)

	return context
