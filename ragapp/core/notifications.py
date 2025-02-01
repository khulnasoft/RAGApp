# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp


def get_notification_config():
	return {
		"for_doctype": {
			"Error Log": {"seen": 0},
			"Communication": {"status": "Open", "communication_type": "Communication"},
			"ToDo": "ragapp.core.notifications.get_things_todo",
			"Event": "ragapp.core.notifications.get_todays_events",
			"Workflow Action": {"status": "Open"},
		},
	}


def get_things_todo(as_list=False):
	"""Return a count of incomplete ToDos."""
	data = ragapp.get_list(
		"ToDo",
		fields=["name", "description"] if as_list else "count(*)",
		filters=[["ToDo", "status", "=", "Open"]],
		or_filters=[
			["ToDo", "allocated_to", "=", ragapp.session.user],
			["ToDo", "assigned_by", "=", ragapp.session.user],
		],
		as_list=True,
	)

	if as_list:
		return data
	return data[0][0]


def get_todays_events(as_list: bool = False):
	"""Return a count of today's events in calendar."""
	from ragapp.desk.doctype.event.event import get_events
	from ragapp.utils import nowdate

	today = nowdate()
	events = get_events(today, today)
	return events if as_list else len(events)
