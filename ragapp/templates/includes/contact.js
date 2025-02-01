// Copyright (c) 2025, KhulnaSoft, Ltd and Contributors
// MIT License. See license.txt

ragapp.ready(function() {

	if(ragapp.utils.get_url_arg('subject')) {
	  $('[name="subject"]').val(ragapp.utils.get_url_arg('subject'));
	}

	$('.btn-send').off("click").on("click", function() {
		var email = $('[name="email"]').val();
		var message = $('[name="message"]').val();

		if(!(email && message)) {
			ragapp.msgprint('{{ _("Please enter both your email and message so that we can get back to you. Thanks!") }}');
			return false;
		}

		if(!validate_email(email)) {
			ragapp.msgprint('{{ _("You seem to have written your name instead of your email. Please enter a valid email address so that we can get back.") }}');
			$('[name="email"]').focus();
			return false;
		}

		$("#contact-alert").toggle(false);
		ragapp.call({
			type: "POST",
			method: "ragapp.www.contact.send_message",
			args: {
				subject: $('[name="subject"]').val(),
				sender: email,
				message: message,
			},
			callback: function(r) {
				if (!r.exc) {
					ragapp.msgprint('{{ _("Thank you for your message") }}', '{{ _("Message Sent") }}');
				}
				$(':input').val('');
			},
		});
	});
});

var msgprint = function(txt) {
	if(txt) $("#contact-alert").html(txt).toggle(true);
}
