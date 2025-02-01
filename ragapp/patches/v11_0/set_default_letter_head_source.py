import ragapp


def execute():
	ragapp.reload_doctype("Letter Head")

	# source of all existing letter heads must be HTML
	ragapp.db.sql("update `tabLetter Head` set source = 'HTML'")
