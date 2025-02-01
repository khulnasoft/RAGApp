ragapp.pages["backups"].on_page_load = function (wrapper) {
	var page = ragapp.ui.make_app_page({
		parent: wrapper,
		title: __("Download Backups"),
		single_column: true,
	});

	page.add_inner_button(__("Set Number of Backups"), function () {
		ragapp.set_route("Form", "System Settings");
	});

	page.add_inner_button(__("Download Files Backup"), function () {
		ragapp.call({
			method: "ragapp.desk.page.backups.backups.schedule_files_backup",
			args: { user_email: ragapp.session.user_email },
		});
	});

	page.add_inner_button(__("Get Backup Encryption Key"), function () {
		if (ragapp.user.has_role("System Manager")) {
			ragapp.verify_password(function () {
				ragapp.call({
					method: "ragapp.utils.backups.get_backup_encryption_key",
					callback: function (r) {
						ragapp.msgprint({
							title: __("Backup Encryption Key"),
							message: __(r.message),
							indicator: "blue",
						});
					},
				});
			});
		} else {
			ragapp.msgprint({
				title: __("Error"),
				message: __("System Manager privileges required."),
				indicator: "red",
			});
		}
	});

	ragapp.breadcrumbs.add("Setup");

	$(ragapp.render_template("backups")).appendTo(page.body.addClass("no-border"));
};
