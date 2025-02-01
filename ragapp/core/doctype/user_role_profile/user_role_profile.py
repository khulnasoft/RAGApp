# Copyright (c) 2024, Ragapp Technologies and contributors
# For license information, please see license.txt

# import ragapp
from ragapp.model.document import Document


class UserRoleProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from ragapp.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		role_profile: DF.Link | None
	# end: auto-generated types

	pass
