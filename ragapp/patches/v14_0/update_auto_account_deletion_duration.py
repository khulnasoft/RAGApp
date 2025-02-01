import ragapp


def execute():
	days = ragapp.db.get_single_value("Website Settings", "auto_account_deletion")
	ragapp.db.set_single_value("Website Settings", "auto_account_deletion", days * 24)
