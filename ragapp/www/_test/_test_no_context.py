import ragapp


# no context object is accepted
def get_context():
	context = ragapp._dict()
	context.body = "Custom Content"
	return context
