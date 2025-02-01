ragapp.provide("ragapp.ui.misc");
ragapp.ui.misc.about = function () {
	if (!ragapp.ui.misc.about_dialog) {
		var d = new ragapp.ui.Dialog({ title: __("Ragapp Framework") });

		$(d.body).html(
			repl(
				`<div>
					<p>${__("Open Source Applications for the Web")}</p>
					<p><i class='fa fa-globe fa-fw'></i>
						${__("Website")}:
						<a href='https://ragapp.khulnasoft.com' target='_blank'>https://ragapp.khulnasoft.com</a></p>
					<p><i class='fa fa-github fa-fw'></i>
						${__("Source")}:
						<a href='https://github.com/khulnasoft' target='_blank'>https://github.com/khulnasoft</a></p>
					<p><i class='fa fa-graduation-cap fa-fw'></i>
						Ragapp School: <a href='https://ragapp.school' target='_blank'>https://ragapp.school</a></p>
					<p><i class='fa fa-linkedin fa-fw'></i>
						Linkedin: <a href='https://linkedin.com/company/ragapp-tech' target='_blank'>https://linkedin.com/company/ragapp-tech</a></p>
					<p><i class='fa fa-twitter fa-fw'></i>
						Twitter: <a href='https://twitter.com/ragapptech' target='_blank'>https://twitter.com/ragapptech</a></p>
					<p><i class='fa fa-youtube fa-fw'></i>
						YouTube: <a href='https://www.youtube.com/@ragapptech' target='_blank'>https://www.youtube.com/@ragapptech</a></p>
					<hr>
					<h4>${__("Installed Apps")}</h4>
					<div id='about-app-versions'>${__("Loading versions...")}</div>
					<p>
						<b>
							<a href="/attribution" target="_blank" class="text-muted">
								${__("Dependencies & Licenses")}
							</a>
						</b>
					</p>
					<hr>
					<p class='text-muted'>${__("&copy; Ragapp Technologies Pvt. Ltd. and contributors")} </p>
					</div>`,
				ragapp.app
			)
		);

		ragapp.ui.misc.about_dialog = d;

		ragapp.ui.misc.about_dialog.on_page_show = function () {
			if (!ragapp.versions) {
				ragapp.call({
					method: "ragapp.utils.change_log.get_versions",
					callback: function (r) {
						show_versions(r.message);
					},
				});
			} else {
				show_versions(ragapp.versions);
			}
		};

		var show_versions = function (versions) {
			var $wrap = $("#about-app-versions").empty();
			$.each(Object.keys(versions).sort(), function (i, key) {
				var v = versions[key];
				let text;
				if (v.branch) {
					text = $.format("<p><b>{0}:</b> v{1} ({2})<br></p>", [
						v.title,
						v.branch_version || v.version,
						v.branch,
					]);
				} else {
					text = $.format("<p><b>{0}:</b> v{1}<br></p>", [v.title, v.version]);
				}
				$(text).appendTo($wrap);
			});

			ragapp.versions = versions;
		};
	}

	ragapp.ui.misc.about_dialog.show();
};
