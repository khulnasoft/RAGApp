# Copyright (c) 2025, KhulnaSoft, Ltd and contributors
# License: MIT. See LICENSE

import ragapp
from ragapp import _
from ragapp.model.document import Document


class EmailUnsubscribe(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		email: DF.Data
		global_unsubscribe: DF.Check
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
	# end: auto-generated types

	def validate(self):
		if not self.global_unsubscribe and not (self.reference_doctype and self.reference_name):
			ragapp.throw(_("Reference DocType and Reference Name are required"), ragapp.MandatoryError)

		if not self.global_unsubscribe and ragapp.db.get_value(self.doctype, self.name, "global_unsubscribe"):
			ragapp.throw(_("Delete this record to allow sending to this email address"))

		if self.global_unsubscribe:
			if ragapp.get_all(
				"Email Unsubscribe",
				filters={"email": self.email, "global_unsubscribe": 1, "name": ["!=", self.name]},
			):
				ragapp.throw(_("{0} already unsubscribed").format(self.email), ragapp.DuplicateEntryError)

		else:
			if ragapp.get_all(
				"Email Unsubscribe",
				filters={
					"email": self.email,
					"reference_doctype": self.reference_doctype,
					"reference_name": self.reference_name,
					"name": ["!=", self.name],
				},
			):
				ragapp.throw(
					_("{0} already unsubscribed for {1} {2}").format(
						self.email, self.reference_doctype, self.reference_name
					),
					ragapp.DuplicateEntryError,
				)

	def on_update(self):
		if self.reference_doctype and self.reference_name:
			doc = ragapp.get_doc(self.reference_doctype, self.reference_name)
			doc.add_comment("Label", _("Left this conversation"), comment_email=self.email)
