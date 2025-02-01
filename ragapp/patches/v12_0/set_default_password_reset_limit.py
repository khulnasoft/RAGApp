# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.reload_doc("core", "doctype", "system_settings", force=1)
	ragapp.db.set_single_value("System Settings", "password_reset_limit", 3)
