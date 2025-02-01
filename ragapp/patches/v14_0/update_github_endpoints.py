import json

import ragapp


def execute():
	if ragapp.db.exists("Social Login Key", "github"):
		ragapp.db.set_value(
			"Social Login Key", "github", "auth_url_data", json.dumps({"scope": "user:email"})
		)
