import ragapp


def execute():
	"""
	Deprecate Feedback Trigger and Rating. This feature was not customizable.
	Now can be achieved via custom Web Forms
	"""
	ragapp.delete_doc("DocType", "Feedback Trigger")
	ragapp.delete_doc("DocType", "Feedback Rating")
