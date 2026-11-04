
import requests
import csv

API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users():
    try:
        # Step 1: Send HTTP GET request
        response = requests.get(API_URL, timeout=10)

        # Step 2: Check for HTTP errors
        response.raise_for_status()

        # Step 3: Convert JSON response to Python data
        users = response.json()

        if not isinstance(users, list):
            raise ValueError("Expected a list of users")

        # Step 4: Print user information
        print("Users retrieved from API:")

        for user in users:
            print(
                f"ID: {user['id']}, "
                f"Name: {user['name']}, "
                f"Email: {user['email']}"
            )

        # Step 5: Save results to CSV
        with open("users.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write CSV header
            writer.writerow(["id", "name", "email", "company"])

            # Write user records
            for user in users:
                writer.writerow([
                    user["id"],
                    user["name"],
                    user["email"],
                    user["company"]["name"]
                ])

        print(f"\nSuccessfully fetched {len(users)} users.")
        print("Data saved to users.csv")

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")

    except (ValueError, KeyError, TypeError) as error:
        print(f"Data processing error: {error}")

    except OSError as error:
        print(f"File error: {error}")


if __name__ == "__main__":
    fetch_users()
