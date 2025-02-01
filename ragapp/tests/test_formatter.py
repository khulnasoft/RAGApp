import ragapp
from ragapp import format
from ragapp.tests import IntegrationTestCase


class TestFormatter(IntegrationTestCase):
	def test_currency_formatting(self):
		df = ragapp._dict({"fieldname": "amount", "fieldtype": "Currency", "options": "currency"})

		doc = ragapp._dict({"amount": 5})
		ragapp.db.set_default("currency", "INR")

		# if currency field is not passed then default currency should be used.
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "₹ 100,000.00")

		doc.currency = "USD"
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "$ 100,000.00")

		ragapp.db.set_default("currency", None)
