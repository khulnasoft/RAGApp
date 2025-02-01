# Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
# License: MIT. See LICENSE

import ragapp
from ragapp.utils import strip_html_tags
from ragapp.utils.html_utils import clean_html

no_cache = 1


def get_context(context):
	message_context = ragapp._dict()
	if hasattr(ragapp.local, "message"):
		message_context["header"] = ragapp.local.message_title
		message_context["title"] = strip_html_tags(ragapp.local.message_title)
		message_context["message"] = ragapp.local.message
		if hasattr(ragapp.local, "message_success"):
			message_context["success"] = ragapp.local.message_success

	elif ragapp.local.form_dict.id:
		message_id = ragapp.local.form_dict.id
		key = f"message_id:{message_id}"
		message = ragapp.cache.get_value(key, expires=True)
		if message:
			message_context.update(message.get("context", {}))
			if message.get("http_status_code"):
				ragapp.local.response["http_status_code"] = message["http_status_code"]

	if not message_context.title:
		message_context.title = clean_html(ragapp.form_dict.title)

	if not message_context.message:
		message_context.message = clean_html(ragapp.form_dict.message)

	return message_context
