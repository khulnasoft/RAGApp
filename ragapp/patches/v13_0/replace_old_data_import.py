# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	if not ragapp.db.table_exists("Data Import"):
		return

	meta = ragapp.get_meta("Data Import")
	# if Data Import is the new one, return early
	if meta.fields[1].fieldname == "import_type":
		return

	ragapp.db.sql("DROP TABLE IF EXISTS `tabData Import Legacy`")
	ragapp.rename_doc("DocType", "Data Import", "Data Import Legacy")
	ragapp.db.commit()
	ragapp.db.sql("DROP TABLE IF EXISTS `tabData Import`")
	ragapp.rename_doc("DocType", "Data Import Beta", "Data Import")
