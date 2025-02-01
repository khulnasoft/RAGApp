# Copyright (c) 2022, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.model import is_default_field
from ragapp.query_builder import Order
from ragapp.query_builder.functions import Count
from ragapp.query_builder.terms import SubQuery
from ragapp.query_builder.utils import DocType


@ragapp.whitelist()
def get_list_settings(doctype):
	try:
		return ragapp.get_cached_doc("List View Settings", doctype)
	except ragapp.DoesNotExistError:
		ragapp.clear_messages()


@ragapp.whitelist()
def set_list_settings(doctype, values):
	try:
		doc = ragapp.get_doc("List View Settings", doctype)
	except ragapp.DoesNotExistError:
		doc = ragapp.new_doc("List View Settings")
		doc.name = doctype
		ragapp.clear_messages()
	doc.update(ragapp.parse_json(values))
	doc.save()


@ragapp.whitelist()
def get_group_by_count(doctype: str, current_filters: str, field: str) -> list[dict]:
	current_filters = ragapp.parse_json(current_filters)

	if field == "assigned_to":
		ToDo = DocType("ToDo")
		User = DocType("User")
		count = Count("*").as_("count")
		filtered_records = ragapp.qb.get_query(
			doctype,
			filters=current_filters,
			fields=["name"],
			validate_filters=True,
		)

		return (
			ragapp.qb.from_(ToDo)
			.from_(User)
			.select(ToDo.allocated_to.as_("name"), count)
			.where(
				(ToDo.status != "Cancelled")
				& (ToDo.allocated_to == User.name)
				& (User.user_type == "System User")
				& (ToDo.reference_name.isin(SubQuery(filtered_records)))
			)
			.groupby(ToDo.allocated_to)
			.orderby(count, order=Order.desc)
			.limit(50)
			.run(as_dict=True)
		)

	meta = ragapp.get_meta(doctype)

	if not meta.has_field(field) and not is_default_field(field):
		raise ValueError("Field does not belong to doctype")

	data = ragapp.get_list(
		doctype,
		filters=current_filters,
		group_by=f"`tab{doctype}`.{field}",
		fields=["count(*) as count", f"`{field}` as name"],
		order_by="count desc",
		limit=1000,
	)

	if field == "owner":
		owner_idx = None

		for idx, item in enumerate(data):
			if item.name == ragapp.session.user:
				owner_idx = idx
				break

		if owner_idx:
			data = [data.pop(owner_idx)] + data[0:49]
		else:
			data = data[0:50]
	else:
		data = data[0:50]

	# Add in title if it's a link field and `show_title_field_in_link` is set
	if (field_meta := meta.get_field(field)) and field_meta.fieldtype == "Link":
		link_meta = ragapp.get_meta(field_meta.options)
		if link_meta.show_title_field_in_link:
			title_field = link_meta.get_title_field()
			for item in data:
				item.title = ragapp.get_value(field_meta.options, item.name, title_field)

	return data
