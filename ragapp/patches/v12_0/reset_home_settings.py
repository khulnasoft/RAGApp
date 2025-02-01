import ragapp


def execute():
	ragapp.reload_doc("core", "doctype", "user")
	ragapp.db.sql(
		"""
		UPDATE `tabUser`
		SET `home_settings` = ''
		WHERE `user_type` = 'System User'
	"""
	)
