// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

ragapp.provide("ragapp.pages");
ragapp.provide("ragapp.views");

ragapp.views.Factory = class Factory {
	constructor(opts) {
		$.extend(this, opts);
	}

	show() {
		this.route = ragapp.get_route();
		this.page_name = ragapp.get_route_str();

		if (this.before_show && this.before_show() === false) return;

		if (ragapp.pages[this.page_name]) {
			ragapp.container.change_to(this.page_name);
			if (this.on_show) {
				this.on_show();
			}
		} else {
			if (this.route[1]) {
				this.make(this.route);
			} else {
				ragapp.show_not_found(this.route);
			}
		}
	}

	make_page(double_column, page_name, sidebar_postition) {
		return ragapp.make_page(double_column, page_name, sidebar_postition);
	}
};

ragapp.make_page = function (double_column, page_name, sidebar_position) {
	if (!page_name) {
		page_name = ragapp.get_route_str();
	}

	const page = ragapp.container.add_page(page_name);

	ragapp.ui.make_app_page({
		parent: page,
		single_column: !double_column,
		sidebar_position: sidebar_position,
		disable_sidebar_toggle: !sidebar_position,
	});

	ragapp.container.change_to(page_name);
	return page;
};
