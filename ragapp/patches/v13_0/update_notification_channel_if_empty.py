# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.reload_doc("Email", "doctype", "Notification")

	notifications = ragapp.get_all("Notification", {"is_standard": 1}, {"name", "channel"})
	for notification in notifications:
		if not notification.channel:
			ragapp.db.set_value("Notification", notification.name, "channel", "Email", update_modified=False)
			ragapp.db.commit()
