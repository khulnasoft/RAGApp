# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.reload_doc("core", "doctype", "system_settings")
	ragapp.db.set_single_value("System Settings", "allow_login_after_fail", 60)
