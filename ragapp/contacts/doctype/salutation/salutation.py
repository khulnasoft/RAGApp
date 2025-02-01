# Copyright (c) 2017, Ragapp Technologies and contributors
# License: MIT. See LICENSE

from ragapp.model.document import Document


class Salutation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		salutation: DF.Data | None
	# end: auto-generated types

	pass
