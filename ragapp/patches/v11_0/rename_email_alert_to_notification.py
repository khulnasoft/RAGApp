import ragapp
from ragapp.model.rename_doc import rename_doc


def execute():
	if ragapp.db.table_exists("Email Alert Recipient") and not ragapp.db.table_exists(
		"Notification Recipient"
	):
		rename_doc("DocType", "Email Alert Recipient", "Notification Recipient")
		ragapp.reload_doc("email", "doctype", "notification_recipient")

	if ragapp.db.table_exists("Email Alert") and not ragapp.db.table_exists("Notification"):
		rename_doc("DocType", "Email Alert", "Notification")
		ragapp.reload_doc("email", "doctype", "notification")
