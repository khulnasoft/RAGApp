# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE
import ragapp
from ragapp.model.document import Document


class ClientScript(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		dt: DF.Link
		enabled: DF.Check
		module: DF.Link | None
		script: DF.Code | None
		view: DF.Literal["List", "Form"]
	# end: auto-generated types

	def on_update(self):
		ragapp.clear_cache(doctype=self.dt)

	def on_trash(self):
		ragapp.clear_cache(doctype=self.dt)
