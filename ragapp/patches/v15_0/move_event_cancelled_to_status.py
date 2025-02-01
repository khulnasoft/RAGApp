import ragapp


def execute():
	Event = ragapp.qb.DocType("Event")
	query = (
		ragapp.qb.update(Event)
		.set(Event.event_type, "Private")
		.set(Event.status, "Cancelled")
		.where(Event.event_type == "Cancelled")
	)
	query.run()
