# Copyright (c) 2023, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import ragapp
from ragapp import _
from ragapp.apps import get_apps


def get_context():
	all_apps = get_apps()

	system_default_app = ragapp.get_system_settings("default_app")
	user_default_app = ragapp.db.get_value("User", ragapp.session.user, "default_app")
	default_app = user_default_app if user_default_app else system_default_app

	if len(all_apps) == 0:
		ragapp.local.flags.redirect_location = "/app"
		raise ragapp.Redirect

	for app in all_apps:
		app["is_default"] = True if app.get("name") == default_app else False

	return {"apps": all_apps}
