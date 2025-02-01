# Copyright (c) 2019, Ragapp Technologies and Contributors
# License: MIT. See LICENSE
import ragapp
import ragapp.cache_manager
from ragapp.tests import IntegrationTestCase, UnitTestCase


class UnitTestMilestoneTracker(UnitTestCase):
	"""
	Unit tests for MilestoneTracker.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestMilestoneTracker(IntegrationTestCase):
	def test_milestone(self):
		ragapp.db.delete("Milestone Tracker")

		ragapp.cache.delete_key("milestone_tracker_map")

		milestone_tracker = ragapp.get_doc(
			doctype="Milestone Tracker", document_type="ToDo", track_field="status"
		).insert()

		todo = ragapp.get_doc(doctype="ToDo", description="test milestone", status="Open").insert()

		milestones = ragapp.get_all(
			"Milestone",
			fields=["track_field", "value", "milestone_tracker"],
			filters=dict(reference_type=todo.doctype, reference_name=todo.name),
		)

		self.assertEqual(len(milestones), 1)
		self.assertEqual(milestones[0].track_field, "status")
		self.assertEqual(milestones[0].value, "Open")

		todo.status = "Closed"
		todo.save()

		milestones = ragapp.get_all(
			"Milestone",
			fields=["track_field", "value", "milestone_tracker"],
			filters=dict(reference_type=todo.doctype, reference_name=todo.name),
			order_by="creation desc",
		)

		self.assertEqual(len(milestones), 2)
		self.assertEqual(milestones[0].track_field, "status")
		self.assertEqual(milestones[0].value, "Closed")

		# cleanup
		ragapp.db.delete("Milestone")
		milestone_tracker.delete()
