import ragapp


class MaxFileSizeReachedError(ragapp.ValidationError):
	pass


class FolderNotEmpty(ragapp.ValidationError):
	pass


class FileTypeNotAllowed(ragapp.ValidationError):
	pass


from ragapp.exceptions import *
