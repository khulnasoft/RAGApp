import ragapp
from ragapp.model.rename_doc import rename_doc


def execute():
	if ragapp.db.table_exists("Standard Reply") and not ragapp.db.table_exists("Email Template"):
		rename_doc("DocType", "Standard Reply", "Email Template")
		ragapp.reload_doc("email", "doctype", "email_template")
