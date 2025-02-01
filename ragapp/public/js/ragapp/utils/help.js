// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

ragapp.provide("ragapp.help");

ragapp.help.youtube_id = {};

ragapp.help.has_help = function (doctype) {
	return ragapp.help.youtube_id[doctype];
};

ragapp.help.show = function (doctype) {
	if (ragapp.help.youtube_id[doctype]) {
		ragapp.help.show_video(ragapp.help.youtube_id[doctype]);
	}
};

ragapp.help.show_video = function (youtube_id, title) {
	if (ragapp.utils.is_url(youtube_id)) {
		const expression =
			'(?:youtube.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu.be/)([^"&?\\s]{11})';
		youtube_id = youtube_id.match(expression)[1];
	}

	// (ragapp.help_feedback_link || "")
	let dialog = new ragapp.ui.Dialog({
		title: title || __("Help"),
		size: "large",
	});

	let video = $(
		`<div class="video-player" data-plyr-provider="youtube" data-plyr-embed-id="${youtube_id}"></div>`
	);
	video.appendTo(dialog.body);

	dialog.show();
	dialog.$wrapper.addClass("video-modal");

	let plyr;
	ragapp.utils.load_video_player().then(() => {
		plyr = new ragapp.Plyr(video[0], {
			hideControls: true,
			resetOnEnd: true,
		});
	});

	dialog.onhide = () => {
		plyr?.destroy();
	};
};

$("body").on("click", "a.help-link", function () {
	var doctype = $(this).attr("data-doctype");
	doctype && ragapp.help.show(doctype);
});
