# Copyright (c) 2022, Ragapp Technologies and contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.deferred_insert import deferred_insert as _deferred_insert
from ragapp.model.document import Document


class RouteHistory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		route: DF.Data | None
		user: DF.Link | None
	# end: auto-generated types

	@staticmethod
	def clear_old_logs(days=30):
		from ragapp.query_builder import Interval
		from ragapp.query_builder.functions import Now

		table = ragapp.qb.DocType("Route History")
		ragapp.db.delete(table, filters=(table.creation < (Now() - Interval(days=days))))


@ragapp.whitelist()
def deferred_insert(routes):
	routes = [
		{
			"user": ragapp.session.user,
			"route": route.get("route"),
			"creation": route.get("creation"),
		}
		for route in ragapp.parse_json(routes)
	]

	_deferred_insert("Route History", routes)


@ragapp.whitelist()
def frequently_visited_links():
	return ragapp.get_all(
		"Route History",
		fields=["route", "count(name) as count"],
		filters={"user": ragapp.session.user},
		group_by="route",
		order_by="count desc",
		limit=5,
	)
