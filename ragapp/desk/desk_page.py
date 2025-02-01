# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp


@ragapp.whitelist()
def get(name):
	"""
	Return the :term:`doclist` of the `Page` specified by `name`
	"""
	page = ragapp.get_doc("Page", name)
	if page.is_permitted():
		page.load_assets()
		docs = ragapp._dict(page.as_dict())
		if getattr(page, "_dynamic_page", None):
			docs["_dynamic_page"] = 1

		return docs
	else:
		ragapp.response["403"] = 1
		raise ragapp.PermissionError("No read permission for Page %s" % (page.title or name))


@ragapp.whitelist(allow_guest=True)
def getpage():
	"""
	Load the page from `ragapp.form` and send it via `ragapp.response`
	"""
	page = ragapp.form_dict.get("name")
	doc = get(page)

	ragapp.response.docs.append(doc)
