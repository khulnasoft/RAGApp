import ragapp


def execute():
	"""
	Rename the Marketing Campaign table to UTM Campaign table
	"""
	if ragapp.db.exists("DocType", "UTM Campaign"):
		return

	if not ragapp.db.exists("DocType", "Marketing Campaign"):
		return

	ragapp.rename_doc("DocType", "Marketing Campaign", "UTM Campaign", force=True)
	ragapp.reload_doctype("UTM Campaign", force=True)
