import click

import ragapp


def execute():
	doctype = "Data Import Legacy"
	table = ragapp.utils.get_table_name(doctype)

	# delete the doctype record to avoid broken links
	ragapp.delete_doc("DocType", doctype, force=True)

	# leaving table in database for manual cleanup
	click.secho(
		f"`{doctype}` has been deprecated. The DocType is deleted, but the data still"
		" exists on the database. If this data is worth recovering, you may export it"
		f" using\n\n\tcli --site {ragapp.local.site} backup -i '{doctype}'\n\nAfter"
		" this, the table will continue to persist in the database, until you choose"
		" to remove it yourself. If you want to drop the table, you may run\n\n\tcli"
		f" --site {ragapp.local.site} execute ragapp.db.sql --args \"('DROP TABLE IF"
		f" EXISTS `{table}`', )\"\n",
		fg="yellow",
	)
