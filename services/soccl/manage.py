import getpass
import sys

from werkzeug.security import generate_password_hash


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "hash-password":
        raise SystemExit("Usage: python manage.py hash-password")
    first = getpass.getpass("Dashboard password: ")
    second = getpass.getpass("Repeat password: ")
    if not first or first != second:
        raise SystemExit("Passwords did not match or were empty")
    print(generate_password_hash(first))


if __name__ == "__main__":
    main()
