"""
Modify the Integer 10 Digits Value to BigInt 20 Digit value
to generate long Naming Series

"""

import ragapp


def execute():
	ragapp.db.sql(""" ALTER TABLE `tabSeries` MODIFY current BIGINT """)
