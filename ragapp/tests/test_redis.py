import functools
from unittest.mock import patch

import redis

import ragapp
from ragapp.tests import IntegrationTestCase
from ragapp.utils import get_cli_id
from ragapp.utils.background_jobs import get_redis_conn
from ragapp.utils.redis_queue import RedisQueue


def version_tuple(version):
	return tuple(map(int, (version.split("."))))


def skip_if_redis_version_lt(version):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			conn = get_redis_conn()
			redis_version = conn.execute_command("info")["redis_version"]
			if version_tuple(redis_version) < version_tuple(version):
				return
			return func(*args, **kwargs)

		return wrapper

	return decorator


class TestRedisAuth(IntegrationTestCase):
	@skip_if_redis_version_lt("6.0")
	@patch.dict(ragapp.conf, {"cli_id": "test_cli", "use_rq_auth": False})
	def test_rq_gen_acllist(self):
		"""Make sure that ACL list is genrated"""
		acl_list = RedisQueue.gen_acl_list()
		self.assertEqual(acl_list[1]["cli"][0], get_cli_id())

	@skip_if_redis_version_lt("6.0")
	@patch.dict(ragapp.conf, {"cli_id": "test_cli", "use_rq_auth": False})
	def test_adding_redis_user(self):
		acl_list = RedisQueue.gen_acl_list()
		username, password = acl_list[1]["cli"]
		conn = get_redis_conn()

		conn.acl_deluser(username)
		_ = RedisQueue(conn).add_user(username, password)
		self.assertTrue(conn.acl_getuser(username))
		conn.acl_deluser(username)

	@skip_if_redis_version_lt("6.0")
	@patch.dict(ragapp.conf, {"cli_id": "test_cli", "use_rq_auth": False})
	def test_rq_namespace(self):
		"""Make sure that user can access only their respective namespace."""
		# Current cli ID
		cli_id = ragapp.conf.get("cli_id")
		conn = get_redis_conn()
		conn.set("rq:queue:test_cli1:abc", "value")
		conn.set(f"rq:queue:{cli_id}:abc", "value")

		# Create new Redis Queue user
		tmp_cli_id = "test_cli1"
		username, password = tmp_cli_id, "password1"
		conn.acl_deluser(username)
		ragapp.conf.update({"cli_id": tmp_cli_id})
		_ = RedisQueue(conn).add_user(username, password)
		test_cli1_conn = RedisQueue.get_connection(username, password)

		self.assertEqual(test_cli1_conn.get("rq:queue:test_cli1:abc"), b"value")

		# User should not be able to access queues apart from their cli queues
		with self.assertRaises(redis.exceptions.NoPermissionError):
			test_cli1_conn.get(f"rq:queue:{cli_id}:abc")

		ragapp.conf.update({"cli_id": cli_id})
		conn.acl_deluser(username)
