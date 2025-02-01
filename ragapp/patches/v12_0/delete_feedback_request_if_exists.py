import ragapp


def execute():
	ragapp.db.delete("DocType", {"name": "Feedback Request"})
