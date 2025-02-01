import os
import shutil
import subprocess
import unittest

from cli.app import App
from cli.cli import Cli
from cli.exceptions import InvalidRemoteException
from cli.utils import is_valid_ragapp_branch


class TestUtils(unittest.TestCase):
	def test_app_utils(self):
		git_url = "https://github.com/khulnasoft/ragapp"
		branch = "main"
		app = App(name=git_url, branch=branch, cli=Cli("."))
		self.assertTrue(
			all(
				[
					app.name == git_url,
					app.branch == branch,
					app.tag == branch,
					app.is_url is True,
					app.on_disk is False,
					app.org == "ragapp",
					app.url == git_url,
				]
			)
		)

	def test_is_valid_ragapp_branch(self):
		with self.assertRaises(InvalidRemoteException):
			is_valid_ragapp_branch(
				"https://github.com/khulnasoft/ragapp.git", ragapp_branch="random-branch"
			)
			is_valid_ragapp_branch(
				"https://github.com/random/random.git", ragapp_branch="random-branch"
			)

		is_valid_ragapp_branch(
			"https://github.com/khulnasoft/ragapp.git", ragapp_branch="main"
		)
		is_valid_ragapp_branch(
			"https://github.com/khulnasoft/ragapp.git", ragapp_branch="v13.29.0"
		)

	def test_app_states(self):
		cli_dir = "./sandbox"
		sites_dir = os.path.join(cli_dir, "sites")

		if not os.path.exists(sites_dir):
			os.makedirs(sites_dir)

		fake_cli = Cli(cli_dir)

		self.assertTrue(hasattr(fake_cli.apps, "states"))

		fake_cli.apps.states = {
			"ragapp": {
				"resolution": {"branch": "main", "commit_hash": "234rwefd"},
				"version": "14.0.0-dev",
			}
		}
		fake_cli.apps.update_apps_states()

		self.assertEqual(fake_cli.apps.states, {})

		ragapp_path = os.path.join(cli_dir, "apps", "ragapp")

		os.makedirs(os.path.join(ragapp_path, "ragapp"))

		subprocess.run(["git", "init"], cwd=ragapp_path, capture_output=True, check=True)

		with open(os.path.join(ragapp_path, "ragapp", "__init__.py"), "w+") as f:
			f.write("__version__ = '11.0'")

		subprocess.run(["git", "add", "."], cwd=ragapp_path, capture_output=True, check=True)
		subprocess.run(
			["git", "config", "user.email", "cli-test_app_states@gha.com"],
			cwd=ragapp_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "config", "user.name", "App States Test"],
			cwd=ragapp_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "commit", "-m", "temp"], cwd=ragapp_path, capture_output=True, check=True
		)

		fake_cli.apps.update_apps_states(app_name="ragapp")

		self.assertIn("ragapp", fake_cli.apps.states)
		self.assertIn("version", fake_cli.apps.states["ragapp"])
		self.assertEqual("11.0", fake_cli.apps.states["ragapp"]["version"])

		shutil.rmtree(cli_dir)

	def test_ssh_ports(self):
		app = App("git@github.com:22:khulnasoft/ragapp")
		self.assertEqual(
			(app.use_ssh, app.org, app.repo, app.app_name), (True, "ragapp", "ragapp", "ragapp")
		)
