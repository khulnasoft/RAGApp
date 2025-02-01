import ragapp


def execute():
	ragapp.reload_doctype("Translation")
	ragapp.db.sql(
		"UPDATE `tabTranslation` SET `translated_text`=`target_name`, `source_text`=`source_name`, `contributed`=0"
	)
