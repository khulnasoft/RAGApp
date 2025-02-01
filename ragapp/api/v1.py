import json

from werkzeug.routing import Rule

import ragapp
from ragapp import _
from ragapp.utils.data import sbool


def document_list(doctype: str):
	if ragapp.form_dict.get("fields"):
		ragapp.form_dict["fields"] = json.loads(ragapp.form_dict["fields"])

	# set limit of records for ragapp.get_list
	ragapp.form_dict.setdefault(
		"limit_page_length",
		ragapp.form_dict.limit or ragapp.form_dict.limit_page_length or 20,
	)

	# convert strings to native types - only as_dict and debug accept bool
	for param in ["as_dict", "debug"]:
		param_val = ragapp.form_dict.get(param)
		if param_val is not None:
			ragapp.form_dict[param] = sbool(param_val)

	# evaluate ragapp.get_list
	return ragapp.call(ragapp.client.get_list, doctype, **ragapp.form_dict)


def handle_rpc_call(method: str):
	import ragapp.handler

	method = method.split("/")[0]  # for backward compatiblity

	ragapp.form_dict.cmd = method
	return ragapp.handler.handle()


def create_doc(doctype: str):
	data = get_request_form_data()
	data.pop("doctype", None)
	return ragapp.new_doc(doctype, **data).insert()


def update_doc(doctype: str, name: str):
	data = get_request_form_data()

	doc = ragapp.get_doc(doctype, name, for_update=True)
	if "flags" in data:
		del data["flags"]

	doc.update(data)
	doc.save()

	# check for child table doctype
	if doc.get("parenttype"):
		ragapp.get_doc(doc.parenttype, doc.parent).save()

	return doc


def delete_doc(doctype: str, name: str):
	# TODO: child doc handling
	ragapp.delete_doc(doctype, name, ignore_missing=False)
	ragapp.response.http_status_code = 202
	return "ok"


def read_doc(doctype: str, name: str):
	# Backward compatiblity
	if "run_method" in ragapp.form_dict:
		return execute_doc_method(doctype, name)

	doc = ragapp.get_doc(doctype, name)
	doc.check_permission("read")
	doc.apply_fieldlevel_read_permissions()
	return doc


def execute_doc_method(doctype: str, name: str, method: str | None = None):
	method = method or ragapp.form_dict.pop("run_method")
	doc = ragapp.get_doc(doctype, name)
	doc.is_whitelisted(method)

	if ragapp.request.method == "GET":
		doc.check_permission("read")
		return doc.run_method(method, **ragapp.form_dict)

	elif ragapp.request.method == "POST":
		doc.check_permission("write")
		return doc.run_method(method, **ragapp.form_dict)


def get_request_form_data():
	if ragapp.form_dict.data is None:
		data = ragapp.safe_decode(ragapp.request.get_data())
	else:
		data = ragapp.form_dict.data

	try:
		return ragapp.parse_json(data)
	except ValueError:
		return ragapp.form_dict


url_rules = [
	Rule("/method/<path:method>", endpoint=handle_rpc_call),
	Rule("/resource/<doctype>", methods=["GET"], endpoint=document_list),
	Rule("/resource/<doctype>", methods=["POST"], endpoint=create_doc),
	Rule("/resource/<doctype>/<path:name>/", methods=["GET"], endpoint=read_doc),
	Rule("/resource/<doctype>/<path:name>/", methods=["PUT"], endpoint=update_doc),
	Rule("/resource/<doctype>/<path:name>/", methods=["DELETE"], endpoint=delete_doc),
	Rule("/resource/<doctype>/<path:name>/", methods=["POST"], endpoint=execute_doc_method),
]
