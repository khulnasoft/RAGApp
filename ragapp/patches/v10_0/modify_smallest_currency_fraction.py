# Copyright (c) 2018, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp


def execute():
	ragapp.db.set_value("Currency", "USD", "smallest_currency_fraction_value", "0.01")
