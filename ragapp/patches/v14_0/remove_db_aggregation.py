import re

import ragapp
from ragapp.query_builder import DocType


def execute():
	"""Replace temporarily available Database Aggregate APIs on ragapp (develop)

	APIs changed:
	        * ragapp.db.max => ragapp.qb.max
	        * ragapp.db.min => ragapp.qb.min
	        * ragapp.db.sum => ragapp.qb.sum
	        * ragapp.db.avg => ragapp.qb.avg
	"""
	ServerScript = DocType("Server Script")
	server_scripts = (
		ragapp.qb.from_(ServerScript)
		.where(
			ServerScript.script.like("%ragapp.db.max(%")
			| ServerScript.script.like("%ragapp.db.min(%")
			| ServerScript.script.like("%ragapp.db.sum(%")
			| ServerScript.script.like("%ragapp.db.avg(%")
		)
		.select("name", "script")
		.run(as_dict=True)
	)

	for server_script in server_scripts:
		name, script = server_script["name"], server_script["script"]

		for agg in ["avg", "max", "min", "sum"]:
			script = re.sub(f"ragapp.db.{agg}\\(", f"ragapp.qb.{agg}(", script)

		ragapp.db.set_value("Server Script", name, "script", script)
