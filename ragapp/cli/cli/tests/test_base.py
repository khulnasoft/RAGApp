# imports - standard imports
import getpass
import json
import os
import shutil
import subprocess
import sys
import traceback
import unittest

# imports - module imports
from cli.utils import paths_in_cli, exec_cmd
from cli.utils.system import init
from cli.cli import Cli

PYTHON_VER = sys.version_info

RAGAPP_BRANCH = "version-13-hotfix"
if PYTHON_VER.major == 3:
	if PYTHON_VER.minor >= 10:
		RAGAPP_BRANCH = "develop"


class TestCliBase(unittest.TestCase):
	def setUp(self):
		self.clies_path = "."
		self.clies = []

	def tearDown(self):
		for cli_name in self.clies:
			cli_path = os.path.join(self.clies_path, cli_name)
			cli = Cli(cli_path)
			mariadb_password = (
				"travis"
				if os.environ.get("CI")
				else getpass.getpass(prompt="Enter MariaDB root Password: ")
			)

			if cli.exists:
				for site in cli.sites:
					subprocess.call(
						[
							"cli",
							"drop-site",
							site,
							"--force",
							"--no-backup",
							"--root-password",
							mariadb_password,
						],
						cwd=cli_path,
					)
				shutil.rmtree(cli_path, ignore_errors=True)

	def assert_folders(self, cli_name):
		for folder in paths_in_cli:
			self.assert_exists(cli_name, folder)
		self.assert_exists(cli_name, "apps", "ragapp")

	def assert_virtual_env(self, cli_name):
		cli_path = os.path.abspath(cli_name)
		python_path = os.path.abspath(os.path.join(cli_path, "env", "bin", "python"))
		self.assertTrue(python_path.startswith(cli_path))
		for subdir in ("bin", "lib", "share"):
			self.assert_exists(cli_name, "env", subdir)

	def assert_config(self, cli_name):
		for config, search_key in (
			("redis_queue.conf", "redis_queue.rdb"),
			("redis_cache.conf", "redis_cache.rdb"),
		):

			self.assert_exists(cli_name, "config", config)

			with open(os.path.join(cli_name, "config", config)) as f:
				self.assertTrue(search_key in f.read())

	def assert_common_site_config(self, cli_name, expected_config):
		common_site_config_path = os.path.join(
			self.clies_path, cli_name, "sites", "common_site_config.json"
		)
		self.assertTrue(os.path.exists(common_site_config_path))

		with open(common_site_config_path) as f:
			config = json.load(f)

		for key, value in list(expected_config.items()):
			self.assertEqual(config.get(key), value)

	def assert_exists(self, *args):
		self.assertTrue(os.path.exists(os.path.join(*args)))

	def new_site(self, site_name, cli_name):
		new_site_cmd = ["cli", "new-site", site_name, "--admin-password", "admin"]

		if os.environ.get("CI"):
			new_site_cmd.extend(["--mariadb-root-password", "travis"])

		subprocess.call(new_site_cmd, cwd=os.path.join(self.clies_path, cli_name))

	def init_cli(self, cli_name, **kwargs):
		self.clies.append(cli_name)
		ragapp_tmp_path = "/tmp/ragapp"

		if not os.path.exists(ragapp_tmp_path):
			exec_cmd(
				f"git clone https://github.com/khulnasoft/ragapp -b {RAGAPP_BRANCH} --depth 1 --origin upstream {ragapp_tmp_path}"
			)

		kwargs.update(
			dict(
				python=sys.executable,
				no_procfile=True,
				no_backups=True,
				ragapp_path=ragapp_tmp_path,
			)
		)

		if not os.path.exists(os.path.join(self.clies_path, cli_name)):
			init(cli_name, **kwargs)
			exec_cmd(
				"git remote set-url upstream https://github.com/khulnasoft/ragapp",
				cwd=os.path.join(self.clies_path, cli_name, "apps", "ragapp"),
			)

	def file_exists(self, path):
		if os.environ.get("CI"):
			return not subprocess.call(["sudo", "test", "-f", path])
		return os.path.isfile(path)

	def get_traceback(self):
		exc_type, exc_value, exc_tb = sys.exc_info()
		trace_list = traceback.format_exception(exc_type, exc_value, exc_tb)
		return "".join(str(t) for t in trace_list)
