# Copyright (c) 2019, Ragapp Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import time

import sqlparse

import ragapp
import ragapp.recorder
from ragapp.recorder import normalize_query
from ragapp.tests import IntegrationTestCase, timeout
from ragapp.utils import set_request
from ragapp.utils.doctor import any_job_pending
from ragapp.website.serve import get_response_content


class TestRecorder(IntegrationTestCase):
	def setUp(self):
		self.wait_for_background_jobs()
		ragapp.recorder.stop()
		ragapp.recorder.delete()
		set_request()
		ragapp.recorder.start()
		ragapp.recorder.record()

	@timeout
	def wait_for_background_jobs(self):
		while any_job_pending(ragapp.local.site):
			time.sleep(1)

	def stop_recording(self):
		ragapp.recorder.dump()
		ragapp.recorder.stop()

	def test_start(self):
		self.stop_recording()
		requests = ragapp.recorder.get()
		self.assertEqual(len(requests), 1)

	def test_do_not_record(self):
		ragapp.recorder.do_not_record(ragapp.get_all)("DocType")
		self.stop_recording()
		requests = ragapp.recorder.get()
		self.assertEqual(len(requests), 0)

	def test_get(self):
		self.stop_recording()

		requests = ragapp.recorder.get()
		self.assertEqual(len(requests), 1)

		request = ragapp.recorder.get(requests[0]["uuid"])
		self.assertTrue(request)

	def test_delete(self):
		self.stop_recording()

		requests = ragapp.recorder.get()
		self.assertEqual(len(requests), 1)

		ragapp.recorder.delete()

		requests = ragapp.recorder.get()
		self.assertEqual(len(requests), 0)

	def test_record_without_sql_queries(self):
		self.stop_recording()

		requests = ragapp.recorder.get()
		request = ragapp.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"]), 0)

	def test_record_with_sql_queries(self):
		ragapp.get_all("DocType")
		self.stop_recording()

		requests = ragapp.recorder.get()
		request = ragapp.recorder.get(requests[0]["uuid"])

		self.assertNotEqual(len(request["calls"]), 0)

	def test_explain(self):
		ragapp.db.sql("SELECT * FROM tabDocType")
		ragapp.db.sql("COMMIT")
		ragapp.db.sql("select 1", run=0)
		self.stop_recording()

		requests = ragapp.recorder.get()
		request = ragapp.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"][0]["explain_result"]), 1)
		self.assertEqual(len(request["calls"][1]["explain_result"]), 0)

	def test_multiple_queries(self):
		queries = [
			{"mariadb": "SELECT * FROM tabDocType", "postgres": 'SELECT * FROM "tabDocType"'},
			{"mariadb": "SELECT COUNT(*) FROM tabDocType", "postgres": 'SELECT COUNT(*) FROM "tabDocType"'},
			{"mariadb": "COMMIT", "postgres": "COMMIT"},
		]

		sql_dialect = ragapp.db.db_type or "mariadb"
		for query in queries:
			ragapp.db.sql(query[sql_dialect])

		self.stop_recording()

		requests = ragapp.recorder.get()
		request = ragapp.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"]), len(queries))

		for query, call in zip(queries, request["calls"], strict=False):
			self.assertEqual(
				call["query"],
				sqlparse.format(
					query[sql_dialect].strip(), keyword_case="upper", reindent=True, strip_comments=True
				),
			)

	def test_duplicate_queries(self):
		queries = [
			("SELECT * FROM tabDocType", 2),
			("SELECT COUNT(*) FROM tabDocType", 1),
			("select * from tabDocType", 2),
			("COMMIT", 3),
			("COMMIT", 3),
			("COMMIT", 3),
		]
		for query in queries:
			ragapp.db.sql(query[0])

		self.stop_recording()

		requests = ragapp.recorder.get()
		request = ragapp.recorder.get(requests[0]["uuid"])

		for query, call in zip(queries, request["calls"], strict=False):
			self.assertEqual(call["exact_copies"], query[1])

	def test_error_page_rendering(self):
		content = get_response_content("error")
		self.assertIn("Error", content)


class TestRecorderDeco(IntegrationTestCase):
	def test_recorder_flag(self):
		ragapp.recorder.delete()

		@ragapp.recorder.record_queries
		def test():
			ragapp.get_all("User")

		test()
		self.assertTrue(ragapp.recorder.get())


class TestQueryNormalization(IntegrationTestCase):
	def test_query_normalization(self):
		test_cases = {
			"select * from user where name = 'x'": "select * from user where name = ?",
			"select * from user where a > 5": "select * from user where a > ?",
			"select * from `user` where a > 5": "select * from `user` where a > ?",
			"select `name` from `user`": "select `name` from `user`",
			"select `name` from `user` limit 10": "select `name` from `user` limit ?",
			"select `name` from `user` where name in ('a', 'b', 'c')": "select `name` from `user` where name in (?)",
		}

		for query, normalized in test_cases.items():
			self.assertEqual(normalize_query(query), normalized)
