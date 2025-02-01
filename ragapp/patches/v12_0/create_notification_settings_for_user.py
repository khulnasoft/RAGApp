import ragapp
from ragapp.desk.doctype.notification_settings.notification_settings import (
	create_notification_settings,
)


def execute():
	ragapp.reload_doc("desk", "doctype", "notification_settings")
	ragapp.reload_doc("desk", "doctype", "notification_subscribed_document")

	users = ragapp.get_all("User", fields=["name"])
	for user in users:
		create_notification_settings(user.name)
