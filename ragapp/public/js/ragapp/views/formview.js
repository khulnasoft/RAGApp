// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

ragapp.provide("ragapp.views.formview");

ragapp.views.FormFactory = class FormFactory extends ragapp.views.Factory {
	make(route) {
		var doctype = route[1],
			doctype_layout = ragapp.router.doctype_layout || doctype;

		if (!ragapp.views.formview[doctype_layout]) {
			ragapp.model.with_doctype(doctype, () => {
				this.page = ragapp.container.add_page(doctype_layout);
				ragapp.views.formview[doctype_layout] = this.page;
				this.make_and_show(doctype, route);
			});
		} else {
			this.show_doc(route);
		}

		this.setup_events();
	}

	make_and_show(doctype, route) {
		if (ragapp.router.doctype_layout) {
			ragapp.model.with_doc("DocType Layout", ragapp.router.doctype_layout, () => {
				this.make_form(doctype);
				this.show_doc(route);
			});
		} else {
			this.make_form(doctype);
			this.show_doc(route);
		}
	}

	make_form(doctype) {
		this.page.frm = new ragapp.ui.form.Form(
			doctype,
			this.page,
			true,
			ragapp.router.doctype_layout
		);
	}

	setup_events() {
		if (!this.initialized) {
			$(document).on("page-change", function () {
				ragapp.ui.form.close_grid_form();
			});
		}
		this.initialized = true;
	}

	show_doc(route) {
		var doctype = route[1],
			doctype_layout = ragapp.router.doctype_layout || doctype,
			name = route.slice(2).join("/");

		if (ragapp.model.new_names[name]) {
			// document has been renamed, reroute
			name = ragapp.model.new_names[name];
			ragapp.set_route("Form", doctype_layout, name);
			return;
		}

		const doc = ragapp.get_doc(doctype, name);
		if (
			doc &&
			ragapp.model.get_docinfo(doctype, name) &&
			(doc.__islocal || ragapp.model.is_fresh(doc))
		) {
			// is document available and recent?
			this.render(doctype_layout, name);
		} else {
			this.fetch_and_render(doctype, name, doctype_layout);
		}
	}

	fetch_and_render(doctype, name, doctype_layout) {
		ragapp.model.with_doc(doctype, name, (name, r) => {
			if (r && r["403"]) return; // not permitted

			if (!(locals[doctype] && locals[doctype][name])) {
				if (name && name.substr(0, 3) === "new") {
					this.render_new_doc(doctype, name, doctype_layout);
				} else {
					ragapp.show_not_found();
				}
				return;
			}
			this.render(doctype_layout, name);
		});
	}

	render_new_doc(doctype, name, doctype_layout) {
		const new_name = ragapp.model.make_new_doc_and_get_name(doctype, true);
		if (new_name === name) {
			this.render(doctype_layout, name);
		} else {
			ragapp.route_flags.replace_route = true;
			ragapp.set_route("Form", doctype_layout, new_name);
		}
	}

	render(doctype_layout, name) {
		ragapp.container.change_to(doctype_layout);
		ragapp.views.formview[doctype_layout].frm.refresh(name);
	}
};
