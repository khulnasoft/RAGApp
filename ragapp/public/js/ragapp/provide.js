// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

// provide a namespace
if (!window.ragapp) window.ragapp = {};

ragapp.provide = function (namespace) {
	// docs: create a namespace //
	var nsl = namespace.split(".");
	var parent = window;
	for (var i = 0; i < nsl.length; i++) {
		var n = nsl[i];
		if (!parent[n]) {
			parent[n] = {};
		}
		parent = parent[n];
	}
	return parent;
};

ragapp.provide("locals");
ragapp.provide("ragapp.flags");
ragapp.provide("ragapp.settings");
ragapp.provide("ragapp.utils");
ragapp.provide("ragapp.ui.form");
ragapp.provide("ragapp.modules");
ragapp.provide("ragapp.templates");
ragapp.provide("ragapp.test_data");
ragapp.provide("ragapp.utils");
ragapp.provide("ragapp.model");
ragapp.provide("ragapp.user");
ragapp.provide("ragapp.session");
ragapp.provide("ragapp._messages");
ragapp.provide("locals.DocType");

// for listviews
ragapp.provide("ragapp.listview_settings");
ragapp.provide("ragapp.tour");
ragapp.provide("ragapp.listview_parent_route");

// constants
window.NEWLINE = "\n";
window.TAB = 9;
window.UP_ARROW = 38;
window.DOWN_ARROW = 40;

// proxy for user globals defined in desk.js

// API globals
window.cur_frm = null;
