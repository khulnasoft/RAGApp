# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.reload_doc("core", "doctype", "DocField")

	if ragapp.db.has_column("DocField", "show_days"):
		ragapp.db.sql(
			"""
			UPDATE
				tabDocField
			SET
				hide_days = 1 WHERE show_days = 0
		"""
		)
		ragapp.db.sql_ddl("alter table tabDocField drop column show_days")

	if ragapp.db.has_column("DocField", "show_seconds"):
		ragapp.db.sql(
			"""
			UPDATE
				tabDocField
			SET
				hide_seconds = 1 WHERE show_seconds = 0
		"""
		)
		ragapp.db.sql_ddl("alter table tabDocField drop column show_seconds")

	ragapp.clear_cache(doctype="DocField")
