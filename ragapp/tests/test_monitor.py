# Copyright (c) 2020, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import ragapp
import ragapp.monitor
from ragapp.monitor import MONITOR_REDIS_KEY, get_trace_id
from ragapp.tests import IntegrationTestCase
from ragapp.utils import set_request
from ragapp.utils.response import build_response


class TestMonitor(IntegrationTestCase):
	def setUp(self):
		ragapp.conf.monitor = 1
		ragapp.cache.delete_value(MONITOR_REDIS_KEY)

	def tearDown(self):
		ragapp.conf.monitor = 0
		ragapp.cache.delete_value(MONITOR_REDIS_KEY)

	def test_enable_monitor(self):
		set_request(method="GET", path="/api/method/ragapp.ping")
		response = build_response("json")

		ragapp.monitor.start()
		ragapp.monitor.stop(response)

		logs = ragapp.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)

		log = ragapp.parse_json(logs[0].decode())
		self.assertTrue(log.duration)
		self.assertTrue(log.site)
		self.assertTrue(log.timestamp)
		self.assertTrue(log.uuid)
		self.assertTrue(log.request)
		self.assertEqual(log.transaction_type, "request")
		self.assertEqual(log.request["method"], "GET")

	def test_no_response(self):
		set_request(method="GET", path="/api/method/ragapp.ping")

		ragapp.monitor.start()
		ragapp.monitor.stop(response=None)

		logs = ragapp.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)

		log = ragapp.parse_json(logs[0].decode())
		self.assertEqual(log.request["status_code"], 500)
		self.assertEqual(log.transaction_type, "request")
		self.assertEqual(log.request["method"], "GET")

	def test_job(self):
		ragapp.utils.background_jobs.execute_job(
			ragapp.local.site, "ragapp.ping", None, None, {}, is_async=False
		)

		logs = ragapp.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)
		log = ragapp.parse_json(logs[0].decode())
		self.assertEqual(log.transaction_type, "job")
		self.assertTrue(log.job)
		self.assertEqual(log.job["method"], "ragapp.ping")
		self.assertEqual(log.job["scheduled"], False)
		self.assertEqual(log.job["wait"], 0)

	def test_flush(self):
		set_request(method="GET", path="/api/method/ragapp.ping")
		response = build_response("json")
		ragapp.monitor.start()
		ragapp.monitor.stop(response)

		open(ragapp.monitor.log_file(), "w").close()
		ragapp.monitor.flush()

		with open(ragapp.monitor.log_file()) as f:
			logs = f.readlines()

		self.assertEqual(len(logs), 1)
		log = ragapp.parse_json(logs[0])
		self.assertEqual(log.transaction_type, "request")

	def test_trace_ids(self):
		set_request(method="GET", path="/api/method/ragapp.ping")
		response = build_response("json")
		ragapp.monitor.start()
		ragapp.db.sql("select 1")
		self.assertIn(get_trace_id(), str(ragapp.db.last_query))
		ragapp.monitor.stop(response)
