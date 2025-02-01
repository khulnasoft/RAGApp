import os
import re

import ragapp
from ragapp.database.db_manager import DbManager
from ragapp.utils import cint


def setup_database():
	root_conn = get_root_connection()
	root_conn.commit()
	root_conn.sql("end")
	root_conn.sql(f'DROP DATABASE IF EXISTS "{ragapp.conf.db_name}"')

	# If user exists, just update password
	if root_conn.sql(f"SELECT 1 FROM pg_roles WHERE rolname='{ragapp.conf.db_user}'"):
		root_conn.sql(f"ALTER USER \"{ragapp.conf.db_user}\" WITH PASSWORD '{ragapp.conf.db_password}'")
	else:
		root_conn.sql(f"CREATE USER \"{ragapp.conf.db_user}\" WITH PASSWORD '{ragapp.conf.db_password}'")
	root_conn.sql(f'CREATE DATABASE "{ragapp.conf.db_name}"')
	root_conn.sql(f'GRANT ALL PRIVILEGES ON DATABASE "{ragapp.conf.db_name}" TO "{ragapp.conf.db_user}"')
	if psql_version := root_conn.sql("SHOW server_version_num", as_dict=True):
		semver_version_num = psql_version[0].get("server_version_num") or "140000"
		if cint(semver_version_num) > 150000:
			root_conn.sql(f'ALTER DATABASE "{ragapp.conf.db_name}" OWNER TO "{ragapp.conf.db_user}"')
	root_conn.close()


def bootstrap_database(verbose, source_sql=None):
	ragapp.connect()
	import_db_from_sql(source_sql, verbose)

	ragapp.connect()
	if "tabDefaultValue" not in ragapp.db.get_tables():
		import sys

		from click import secho

		secho(
			"Table 'tabDefaultValue' missing in the restored site. "
			"This happens when the backup fails to restore. Please check that the file is valid\n"
			"Do go through the above output to check the exact error message from MariaDB",
			fg="red",
		)
		sys.exit(1)


def import_db_from_sql(source_sql=None, verbose=False):
	if verbose:
		print("Starting database import...")
	db_name = ragapp.conf.db_name
	if not source_sql:
		source_sql = os.path.join(os.path.dirname(__file__), "framework_postgres.sql")
	DbManager(ragapp.local.db).restore_database(
		verbose, db_name, source_sql, ragapp.conf.db_user, ragapp.conf.db_password
	)
	if verbose:
		print("Imported from database {}".format(source_sql))


def get_root_connection():
	if not ragapp.local.flags.root_connection:
		import sys
		from getpass import getpass

		if not ragapp.flags.root_login:
			ragapp.flags.root_login = (
				ragapp.conf.get("postgres_root_login")
				or ragapp.conf.get("root_login")
				or (sys.__stdin__.isatty() and input("Enter postgres super user [postgres]: "))
				or "postgres"
			)

		if not ragapp.flags.root_password:
			ragapp.flags.root_password = (
				ragapp.conf.get("postgres_root_password")
				or ragapp.conf.get("root_password")
				or getpass("Postgres super user password: ")
			)

		ragapp.local.flags.root_connection = ragapp.database.get_db(
			socket=ragapp.conf.db_socket,
			host=ragapp.conf.db_host,
			port=ragapp.conf.db_port,
			user=ragapp.flags.root_login,
			password=ragapp.flags.root_password,
			cur_db_name=ragapp.flags.root_login,
		)

	return ragapp.local.flags.root_connection


def drop_user_and_database(db_name, db_user):
	root_conn = get_root_connection()
	root_conn.commit()
	root_conn.sql(
		"SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = %s",
		(db_name,),
	)
	root_conn.sql("end")
	root_conn.sql(f"DROP DATABASE IF EXISTS {db_name}")
	root_conn.sql(f"DROP USER IF EXISTS {db_user}")
