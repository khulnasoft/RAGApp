import ragapp


def execute():
	item = ragapp.db.exists("Navbar Item", {"item_label": "Background Jobs"})
	if not item:
		return

	ragapp.delete_doc("Navbar Item", item)
