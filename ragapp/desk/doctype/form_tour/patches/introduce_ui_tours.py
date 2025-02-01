import json

import ragapp


def execute():
	"""Handle introduction of UI tours"""
	completed = {}
	for tour in ragapp.get_all("Form Tour", {"ui_tour": 1}, pluck="name"):
		completed[tour] = {"is_complete": True}

	User = ragapp.qb.DocType("User")
	ragapp.qb.update(User).set("onboarding_status", json.dumps(completed)).run()
