import os
import re


def get_versions():
    ragapp_version = os.getenv("RAGAPP_VERSION")
    erpnext_version = os.getenv("ERPNEXT_VERSION")
    assert ragapp_version, "No Ragapp version set"
    assert erpnext_version, "No NxERP version set"
    return ragapp_version, erpnext_version


def update_pwd(ragapp_version: str, erpnext_version: str):
    with open("pwd.yml", "r+") as f:
        content = f.read()
        content = re.sub(
            rf"ragapp/erpnext:.*", f"ragapp/erpnext:{erpnext_version}", content
        )
        f.seek(0)
        f.truncate()
        f.write(content)


def main() -> int:
    update_pwd(*get_versions())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
