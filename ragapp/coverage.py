# Copyright (c) 2021, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE
"""
ragapp.coverage
~~~~~~~~~~~~~~~~

Coverage settings for ragapp
"""

STANDARD_INCLUSIONS = ["*.py"]

STANDARD_EXCLUSIONS = [
	"*.js",
	"*.xml",
	"*.pyc",
	"*.css",
	"*.less",
	"*.scss",
	"*.vue",
	"*.html",
	"*/test_*",
	"*/node_modules/*",
	"*/doctype/*/*_dashboard.py",
	"*/patches/*",
]

# tested via commands' test suite
TESTED_VIA_CLI = [
	"*/ragapp/installer.py",
	"*/ragapp/utils/install.py",
	"*/ragapp/utils/scheduler.py",
	"*/ragapp/utils/doctor.py",
	"*/ragapp/build.py",
	"*/ragapp/database/__init__.py",
	"*/ragapp/database/db_manager.py",
	"*/ragapp/database/**/setup_db.py",
]

RAGAPP_EXCLUSIONS = [
	"*/tests/*",
	"*/commands/*",
	"*/ragapp/change_log/*",
	"*/ragapp/exceptions*",
	"*/ragapp/desk/page/setup_wizard/setup_wizard.py",
	"*/ragapp/coverage.py",
	"*ragapp/setup.py",
	"*/doctype/*/*_dashboard.py",
	"*/patches/*",
	*TESTED_VIA_CLI,
]


class CodeCoverage:
	"""
	Context manager for handling code coverage.

	This class sets up code coverage measurement for a specific app,
	applying the appropriate inclusion and exclusion patterns.
	"""

	def __init__(self, with_coverage, app, outfile="coverage.xml"):
		self.with_coverage = with_coverage
		self.app = app or "ragapp"
		self.outfile = outfile

	def __enter__(self):
		if self.with_coverage:
			import os

			from coverage import Coverage

			from ragapp.utils import get_cli_path

			# Generate coverage report only for app that is being tested
			source_path = os.path.join(get_cli_path(), "apps", self.app)
			omit = STANDARD_EXCLUSIONS[:]

			if self.app == "ragapp":
				omit.extend(RAGAPP_EXCLUSIONS)

			self.coverage = Coverage(source=[source_path], omit=omit, include=STANDARD_INCLUSIONS)
			self.coverage.start()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if self.with_coverage:
			self.coverage.stop()
			self.coverage.save()
			self.coverage.xml_report(outfile=self.outfile)
			print("Saved Coverage")
