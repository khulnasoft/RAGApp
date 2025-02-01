# Copyright (c) 2021, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import ragapp


def execute():
	ragapp.reload_doc("website", "doctype", "web_form_list_column")
	ragapp.reload_doctype("Web Form")

	for web_form in ragapp.get_all("Web Form", fields=["*"]):
		if web_form.allow_multiple and not web_form.show_list:
			ragapp.db.set_value("Web Form", web_form.name, "show_list", True)
