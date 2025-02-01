import ragapp


def execute():
	column = "apply_user_permissions"
	to_remove = ["DocPerm", "Custom DocPerm"]

	for doctype in to_remove:
		if ragapp.db.table_exists(doctype):
			if column in ragapp.db.get_table_columns(doctype):
				ragapp.db.sql(f"alter table `tab{doctype}` drop column {column}")

	ragapp.reload_doc("core", "doctype", "docperm", force=True)
	ragapp.reload_doc("core", "doctype", "custom_docperm", force=True)
