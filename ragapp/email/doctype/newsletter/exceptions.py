# Copyright (c) 2021, Ragapp Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE

from ragapp.exceptions import ValidationError


class NewsletterAlreadySentError(ValidationError):
	pass


class NoRecipientFoundError(ValidationError):
	pass


class NewsletterNotSavedError(ValidationError):
	pass
