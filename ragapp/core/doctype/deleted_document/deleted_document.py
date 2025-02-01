# Copyright (c) 2015, Ragapp Technologies and contributors
# License: MIT. See LICENSE

import json

import ragapp
from ragapp import _
from ragapp.desk.doctype.bulk_update.bulk_update import show_progress
from ragapp.model.document import Document
from ragapp.model.workflow import get_workflow_name


class DeletedDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		data: DF.Code | None
		deleted_doctype: DF.Data | None
		deleted_name: DF.Data | None
		new_name: DF.ReadOnly | None
		restored: DF.Check
	# end: auto-generated types

	no_feed_on_delete = True

	@staticmethod
	def clear_old_logs(days=180):
		from ragapp.query_builder import Interval
		from ragapp.query_builder.functions import Now

		table = ragapp.qb.DocType("Deleted Document")
		ragapp.db.delete(table, filters=(table.creation < (Now() - Interval(days=days))))


@ragapp.whitelist()
def restore(name, alert=True):
	deleted = ragapp.get_doc("Deleted Document", name)

	if deleted.restored:
		ragapp.throw(_("Document {0} Already Restored").format(name), exc=ragapp.DocumentAlreadyRestored)

	doc = ragapp.get_doc(json.loads(deleted.data))

	try:
		doc.insert()
	except ragapp.DocstatusTransitionError:
		ragapp.msgprint(_("Cancelled Document restored as Draft"))
		doc.docstatus = 0
		active_workflow = get_workflow_name(doc.doctype)
		if active_workflow:
			workflow_state_fieldname = ragapp.get_value("Workflow", active_workflow, "workflow_state_field")
			if doc.get(workflow_state_fieldname):
				doc.set(workflow_state_fieldname, None)
		doc.insert()

	doc.add_comment("Edit", _("restored {0} as {1}").format(deleted.deleted_name, doc.name))

	deleted.new_name = doc.name
	deleted.restored = 1
	deleted.db_update()

	if alert:
		ragapp.msgprint(_("Document Restored"))


@ragapp.whitelist()
def bulk_restore(docnames):
	docnames = ragapp.parse_json(docnames)
	message = _("Restoring Deleted Document")
	restored, invalid, failed = [], [], []

	for i, d in enumerate(docnames):
		try:
			show_progress(docnames, message, i + 1, d)
			restore(d, alert=False)
			ragapp.db.commit()
			restored.append(d)

		except ragapp.DocumentAlreadyRestored:
			ragapp.clear_last_message()
			invalid.append(d)

		except Exception:
			ragapp.clear_last_message()
			failed.append(d)
			ragapp.db.rollback()

	return {"restored": restored, "invalid": invalid, "failed": failed}
