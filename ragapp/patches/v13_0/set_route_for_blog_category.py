import ragapp


def execute():
	categories = ragapp.get_list("Blog Category")
	for category in categories:
		doc = ragapp.get_doc("Blog Category", category["name"])
		doc.set_route()
		doc.save()
