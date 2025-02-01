import ragapp


def execute():
	doctype = "Top Bar Item"
	if not ragapp.db.table_exists(doctype) or not ragapp.db.has_column(doctype, "target"):
		return

	ragapp.reload_doc("website", "doctype", "top_bar_item")
	ragapp.db.set_value(doctype, {"target": 'target = "_blank"'}, "open_in_new_tab", 1)
