import ragapp


def execute():
	providers = ragapp.get_all("Social Login Key")

	for provider in providers:
		doc = ragapp.get_doc("Social Login Key", provider)
		doc.set_icon()
		doc.save()
