# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp
import ragapp.www.list
from ragapp import _

no_cache = 1


def get_context(context):
	if ragapp.session.user == "Guest":
		ragapp.throw(_("You need to be logged in to access this page"), ragapp.PermissionError)

	context.current_user = ragapp.get_doc("User", ragapp.session.user)
	context.show_sidebar = False
