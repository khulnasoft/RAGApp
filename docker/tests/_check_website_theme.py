import ragapp


def check_website_theme():
    doc = ragapp.new_doc("Website Theme")
    doc.theme = "test theme"
    doc.insert()


def main() -> int:
    ragapp.connect(site="tests")
    check_website_theme()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
