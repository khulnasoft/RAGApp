ragapp.provide("ragapp.model");
ragapp.provide("ragapp.utils");

/**
 * Opens the Website Meta Tag form if it exists for {route}
 * or creates a new doc and opens the form
 */
ragapp.utils.set_meta_tag = function (route) {
	ragapp.db.exists("Website Route Meta", route).then((exists) => {
		if (exists) {
			ragapp.set_route("Form", "Website Route Meta", route);
		} else {
			// new doc
			const doc = ragapp.model.get_new_doc("Website Route Meta");
			doc.__newname = route;
			ragapp.set_route("Form", doc.doctype, doc.name);
		}
	});
};
