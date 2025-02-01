import ragapp


def execute():
	# if current = 0, simply delete the key as it'll be recreated on first entry
	ragapp.db.delete("Series", {"current": 0})

	duplicate_keys = ragapp.db.sql(
		"""
		SELECT name, max(current) as current
		from
			`tabSeries`
		group by
			name
		having count(name) > 1
	""",
		as_dict=True,
	)

	for row in duplicate_keys:
		ragapp.db.delete("Series", {"name": row.name})
		if row.current:
			ragapp.db.sql("insert into `tabSeries`(`name`, `current`) values (%(name)s, %(current)s)", row)
	ragapp.db.commit()

	ragapp.db.sql("ALTER table `tabSeries` ADD PRIMARY KEY IF NOT EXISTS (name)")
