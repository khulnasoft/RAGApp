// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

// for translation
ragapp._ = function (txt, replace, context = null) {
	if (!txt) return txt;
	if (typeof txt != "string") return txt;

	let translated_text = "";

	let key = txt; // txt.replace(/\n/g, "");
	if (context) {
		translated_text = ragapp._messages[`${key}:${context}`];
	}

	if (!translated_text) {
		translated_text = ragapp._messages[key] || txt;
	}

	if (replace && typeof replace === "object") {
		translated_text = $.format(translated_text, replace);
	}
	return translated_text;
};

window.__ = ragapp._;

ragapp.get_languages = function () {
	if (!ragapp.languages) {
		ragapp.languages = [];
		$.each(ragapp.boot.lang_dict, function (lang, value) {
			ragapp.languages.push({ label: lang, value: value });
		});
		ragapp.languages = ragapp.languages.sort(function (a, b) {
			return a.value < b.value ? -1 : 1;
		});
	}
	return ragapp.languages;
};
