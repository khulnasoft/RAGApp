import ragapp


def execute():
	ragapp.reload_doctype("System Settings")
	doc = ragapp.get_single("System Settings")
	doc.enable_chat = 1

	# Changes prescribed by Nabin Hait (nabin@ragapp.khulnasoft.com)
	doc.flags.ignore_mandatory = True
	doc.flags.ignore_permissions = True

	doc.save()
