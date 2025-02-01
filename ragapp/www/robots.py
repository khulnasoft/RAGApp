import ragapp

base_template_path = "www/robots.txt"


def get_context(context):
	robots_txt = (
		ragapp.db.get_single_value("Website Settings", "robots_txt")
		or (ragapp.local.conf.robots_txt and ragapp.read_file(ragapp.local.conf.robots_txt))
		or ""
	)

	return {"robots_txt": robots_txt}
