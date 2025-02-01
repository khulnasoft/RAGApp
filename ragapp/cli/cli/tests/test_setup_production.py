# imports - standard imports
import getpass
import os
import pathlib
import re
import subprocess
import time
import unittest

# imports - module imports
from cli.utils import exec_cmd, get_cmd_output, which
from cli.config.production_setup import get_supervisor_confdir
from cli.tests.test_base import TestCliBase


class TestSetupProduction(TestCliBase):
	def test_setup_production(self):
		user = getpass.getuser()

		for cli_name in ("test-cli-1", "test-cli-2"):
			cli_path = os.path.join(os.path.abspath(self.clies_path), cli_name)
			self.init_cli(cli_name)
			exec_cmd(f"sudo cli setup production {user} --yes", cwd=cli_path)
			self.assert_nginx_config(cli_name)
			self.assert_supervisor_config(cli_name)
			self.assert_supervisor_process(cli_name)

		self.assert_nginx_process()
		exec_cmd(f"sudo cli setup sudoers {user}")
		self.assert_sudoers(user)

		for cli_name in self.clies:
			cli_path = os.path.join(os.path.abspath(self.clies_path), cli_name)
			exec_cmd("sudo cli disable-production", cwd=cli_path)

	def production(self):
		try:
			self.test_setup_production()
		except Exception:
			print(self.get_traceback())

	def assert_nginx_config(self, cli_name):
		conf_src = os.path.join(
			os.path.abspath(self.clies_path), cli_name, "config", "nginx.conf"
		)
		conf_dest = f"/etc/nginx/conf.d/{cli_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			for key in (
				f"upstream {cli_name}-ragapp",
				f"upstream {cli_name}-socketio-server",
			):
				self.assertTrue(key in f)

	def assert_nginx_process(self):
		out = get_cmd_output("sudo nginx -t 2>&1")
		self.assertTrue(
			"nginx: configuration file /etc/nginx/nginx.conf test is successful" in out
		)

	def assert_sudoers(self, user):
		sudoers_file = "/etc/sudoers.d/ragapp"
		service = which("service")
		nginx = which("nginx")

		self.assertTrue(self.file_exists(sudoers_file))

		if os.environ.get("CI"):
			sudoers = subprocess.check_output(["sudo", "cat", sudoers_file]).decode("utf-8")
		else:
			sudoers = pathlib.Path(sudoers_file).read_text()
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {service} nginx *" in sudoers)
		self.assertTrue(f"{user} ALL = (root) NOPASSWD: {nginx}" in sudoers)

	def assert_supervisor_config(self, cli_name, use_rq=True):
		conf_src = os.path.join(
			os.path.abspath(self.clies_path), cli_name, "config", "supervisor.conf"
		)

		supervisor_conf_dir = get_supervisor_confdir()
		conf_dest = f"{supervisor_conf_dir}/{cli_name}.conf"

		self.assertTrue(self.file_exists(conf_src))
		self.assertTrue(self.file_exists(conf_dest))

		# symlink matches
		self.assertEqual(os.path.realpath(conf_dest), conf_src)

		# file content
		with open(conf_src) as f:
			f = f.read()

			tests = [
				f"program:{cli_name}-ragapp-web",
				f"program:{cli_name}-redis-cache",
				f"program:{cli_name}-redis-queue",
				f"group:{cli_name}-web",
				f"group:{cli_name}-workers",
				f"group:{cli_name}-redis",
			]

			if not os.environ.get("CI"):
				tests.append(f"program:{cli_name}-node-socketio")

			if use_rq:
				tests.extend(
					[
						f"program:{cli_name}-ragapp-schedule",
						f"program:{cli_name}-ragapp-default-worker",
						f"program:{cli_name}-ragapp-short-worker",
						f"program:{cli_name}-ragapp-long-worker",
					]
				)

			else:
				tests.extend(
					[
						f"program:{cli_name}-ragapp-workerbeat",
						f"program:{cli_name}-ragapp-worker",
						f"program:{cli_name}-ragapp-longjob-worker",
						f"program:{cli_name}-ragapp-async-worker",
					]
				)

			for key in tests:
				self.assertTrue(key in f)

	def assert_supervisor_process(self, cli_name, use_rq=True, disable_production=False):
		out = get_cmd_output("supervisorctl status")

		while "STARTING" in out:
			print("Waiting for all processes to start...")
			time.sleep(10)
			out = get_cmd_output("supervisorctl status")

		tests = [
			r"{cli_name}-web:{cli_name}-ragapp-web[\s]+RUNNING",
			# Have commented for the time being. Needs to be uncommented later on. Cli is failing on travis because of this.
			# It works on one cli and fails on another.giving FATAL or BACKOFF (Exited too quickly (process log may have details))
			# "{cli_name}-web:{cli_name}-node-socketio[\s]+RUNNING",
			r"{cli_name}-redis:{cli_name}-redis-cache[\s]+RUNNING",
			r"{cli_name}-redis:{cli_name}-redis-queue[\s]+RUNNING",
		]

		if use_rq:
			tests.extend(
				[
					r"{cli_name}-workers:{cli_name}-ragapp-schedule[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-default-worker-0[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-short-worker-0[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-long-worker-0[\s]+RUNNING",
				]
			)

		else:
			tests.extend(
				[
					r"{cli_name}-workers:{cli_name}-ragapp-workerbeat[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-worker[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-longjob-worker[\s]+RUNNING",
					r"{cli_name}-workers:{cli_name}-ragapp-async-worker[\s]+RUNNING",
				]
			)

		for key in tests:
			if disable_production:
				self.assertFalse(re.search(key, out))
			else:
				self.assertTrue(re.search(key, out))


if __name__ == "__main__":
	unittest.main()
