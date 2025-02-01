// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

if (ragapp.require) {
	ragapp.require("file_uploader.bundle.js");
} else {
	ragapp.ready(function () {
		ragapp.require("file_uploader.bundle.js");
	});
}
