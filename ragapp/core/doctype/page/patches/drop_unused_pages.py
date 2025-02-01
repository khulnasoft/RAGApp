import ragapp


def execute():
	for name in ("desktop", "space"):
		ragapp.delete_doc("Page", name)
