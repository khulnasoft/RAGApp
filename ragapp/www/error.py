# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import ragapp
from ragapp import _

no_cache = 1


def get_context(context):
	if ragapp.flags.in_migrate:
		return

	allow_traceback = ragapp.get_system_settings("allow_error_traceback") if ragapp.db else False
	if ragapp.local.flags.disable_traceback and not ragapp.local.dev_server:
		allow_traceback = False

	if not context.title:
		context.title = _("Server Error")
	if not context.message:
		context.message = _("There was an error building this page")

	return {
		"error": ragapp.get_traceback().replace("<", "&lt;").replace(">", "&gt;") if allow_traceback else ""
	}
