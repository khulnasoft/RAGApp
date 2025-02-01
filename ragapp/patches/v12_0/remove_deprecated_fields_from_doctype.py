import ragapp


def execute():
	ragapp.reload_doc("core", "doctype", "doctype_link")
	ragapp.reload_doc("core", "doctype", "doctype_action")
	ragapp.reload_doc("core", "doctype", "doctype")
	ragapp.model.delete_fields({"DocType": ["hide_heading", "image_view", "read_only_onload"]}, delete=1)

	ragapp.db.delete("Property Setter", {"property": "read_only_onload"})
