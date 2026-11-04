import argparse
import csv
import sys
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch user data from a third-party REST API"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of users to retrieve (positive integer)"
    )

    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")

    return args


def fetch_users(limit=None):
    """Fetch users from the external API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        users = response.json()

        if not isinstance(users, list):
            raise ValueError("Expected a list of users")

        if limit is not None:
            users = users[:limit]

        return users

    except requests.exceptions.Timeout:
        print("Error: API request timed out.", file=sys.stderr)

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}", file=sys.stderr)

    except ValueError as error:
        print(f"Invalid API response: {error}", file=sys.stderr)

    return None


def save_to_csv(users, filename="users.csv"):
    """Save user information to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "email", "company"])

        for user in users:
            writer.writerow([
                user["id"],
                user["name"],
                user["email"],
                user["company"]["name"]
            ])


def main():
    args = parse_arguments()

    users = fetch_users(limit=args.limit)

    if users is None:
        return 1

    try:
        print("Users retrieved from API:")

        for user in users:
            print(
                f"ID: {user['id']}, "
                f"Name: {user['name']}, "
                f"Email: {user['email']}"
            )

        save_to_csv(users)

    except (KeyError, TypeError, ValueError) as error:
        print(f"Invalid user data: {error}", file=sys.stderr)
        return 1

    except OSError as error:
        print(f"Failed to write CSV: {error}", file=sys.stderr)
        return 1

    print(f"\nSuccessfully fetched {len(users)} users.")
    print("Data saved to users.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
