# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import json

import ragapp
from ragapp import _


@ragapp.whitelist()
def update_event(args, field_map):
	"""Updates Event (called via calendar) based on passed `field_map`"""
	args = ragapp._dict(json.loads(args))
	field_map = ragapp._dict(json.loads(field_map))
	w = ragapp.get_doc(args.doctype, args.name)
	w.set(field_map.start, args[field_map.start])
	w.set(field_map.end, args.get(field_map.end))
	w.save()


def get_event_conditions(doctype, filters=None):
	"""Return SQL conditions with user permissions and filters for event queries."""
	from ragapp.desk.reportview import get_filters_cond

	if not ragapp.has_permission(doctype):
		ragapp.throw(_("Not Permitted"), ragapp.PermissionError)

	return get_filters_cond(doctype, filters, [], with_match_conditions=True)


@ragapp.whitelist()
def get_events(doctype, start, end, field_map, filters=None, fields=None):
	field_map = ragapp._dict(json.loads(field_map))
	fields = ragapp.parse_json(fields)

	doc_meta = ragapp.get_meta(doctype)
	for d in doc_meta.fields:
		if d.fieldtype == "Color":
			field_map.update({"color": d.fieldname})

	filters = json.loads(filters) if filters else []

	if not fields:
		fields = [field_map.start, field_map.end, field_map.title, "name"]

	if field_map.color:
		fields.append(field_map.color)

	start_date = "ifnull({}, '0001-01-01 00:00:00')".format(field_map.start)
	end_date = "ifnull({}, '2199-12-31 00:00:00')".format(field_map.end)

	filters += [
		[doctype, start_date, "<=", end],
		[doctype, end_date, ">=", start],
	]
	fields = list({field for field in fields if field})
	return ragapp.get_list(doctype, fields=fields, filters=filters)
