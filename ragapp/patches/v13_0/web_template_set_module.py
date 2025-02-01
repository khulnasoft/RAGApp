# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	"""Set default module for standard Web Template, if none."""
	ragapp.reload_doc("website", "doctype", "Web Template Field")
	ragapp.reload_doc("website", "doctype", "web_template")

	standard_templates = ragapp.get_list("Web Template", {"standard": 1})
	for template in standard_templates:
		doc = ragapp.get_doc("Web Template", template.name)
		if not doc.module:
			doc.module = "Website"
			doc.save()
