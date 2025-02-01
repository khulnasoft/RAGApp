import click

import ragapp


def execute():
	ragapp.delete_doc_if_exists("DocType", "Chat Message")
	ragapp.delete_doc_if_exists("DocType", "Chat Message Attachment")
	ragapp.delete_doc_if_exists("DocType", "Chat Profile")
	ragapp.delete_doc_if_exists("DocType", "Chat Token")
	ragapp.delete_doc_if_exists("DocType", "Chat Room User")
	ragapp.delete_doc_if_exists("DocType", "Chat Room")
	ragapp.delete_doc_if_exists("Module Def", "Chat")

	click.secho(
		"Chat Module is moved to a separate app and is removed from Ragapp in version-13.\n"
		"Please install the app to continue using the chat feature: https://github.com/khulnasoft/chat",
		fg="yellow",
	)
