# Copyright (c) 2025, KhulnaSoft, Ltd and contributors
# License: MIT. See LICENSE

from ragapp.model.document import Document


class BlockModule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		module: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
