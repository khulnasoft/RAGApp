# Copyright (c) 2020, Ragapp Technologies and contributors
# License: MIT. See LICENSE

import json

import ragapp
from ragapp.model.document import Document
from ragapp.utils.safe_exec import read_sql, safe_exec


class SystemConsole(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		commit: DF.Check
		console: DF.Code | None
		output: DF.Code | None
		show_processlist: DF.Check
		type: DF.Literal["Python", "SQL"]
	# end: auto-generated types

	def run(self):
		ragapp.only_for("System Manager")
		try:
			ragapp.local.debug_log = []
			if self.type == "Python":
				safe_exec(self.console, script_filename="System Console")
				self.output = "\n".join(ragapp.debug_log)
			elif self.type == "SQL":
				self.output = ragapp.as_json(read_sql(self.console, as_dict=1))
		except Exception:
			self.commit = False
			self.output = ragapp.get_traceback()

		if self.commit:
			ragapp.db.commit()
		else:
			ragapp.db.rollback()
		ragapp.get_doc(
			doctype="Console Log", script=self.console, type=self.type, committed=self.commit
		).insert()
		ragapp.db.commit()


@ragapp.whitelist()
def execute_code(doc):
	console = ragapp.get_doc(json.loads(doc))
	console.run()
	return console.as_dict()


@ragapp.whitelist()
def show_processlist():
	ragapp.only_for("System Manager")
	return _show_processlist()


def _show_processlist():
	return ragapp.db.multisql(
		{
			"postgres": """
			SELECT pid AS "Id",
				query_start AS "Time",
				state AS "State",
				query AS "Info",
				wait_event AS "Progress"
			FROM pg_stat_activity""",
			"mariadb": "show full processlist",
		},
		as_dict=True,
	)
