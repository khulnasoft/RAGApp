# Copyright (c) 2021, Ragapp Technologies and contributors
# For license information, please see license.txt

# import ragapp
from ragapp.model.document import Document


class NewsletterAttachment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		attachment: DF.Attach
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
