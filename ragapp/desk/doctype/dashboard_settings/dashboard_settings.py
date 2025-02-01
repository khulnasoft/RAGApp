# Copyright (c) 2020, Ragapp Technologies and contributors
# License: MIT. See LICENSE

import json

import ragapp

# import ragapp
from ragapp.model.document import Document


class DashboardSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		chart_config: DF.Code | None
		user: DF.Link | None
	# end: auto-generated types

	pass


@ragapp.whitelist()
def create_dashboard_settings(user):
	if not ragapp.db.exists("Dashboard Settings", user):
		doc = ragapp.new_doc("Dashboard Settings")
		doc.name = user
		doc.insert(ignore_permissions=True)
		ragapp.db.commit()
		return doc


def get_permission_query_conditions(user):
	if not user:
		user = ragapp.session.user

	return f"""(`tabDashboard Settings`.name = {ragapp.db.escape(user)})"""


@ragapp.whitelist()
def save_chart_config(reset, config, chart_name):
	reset = ragapp.parse_json(reset)
	doc = ragapp.get_doc("Dashboard Settings", ragapp.session.user)
	chart_config = ragapp.parse_json(doc.chart_config) or {}

	if reset:
		chart_config[chart_name] = {}
	else:
		config = ragapp.parse_json(config)
		if chart_name not in chart_config:
			chart_config[chart_name] = {}
		chart_config[chart_name].update(config)

	ragapp.db.set_value("Dashboard Settings", ragapp.session.user, "chart_config", json.dumps(chart_config))
