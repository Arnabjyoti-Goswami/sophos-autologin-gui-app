import json
import os

home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, "sophos_credentials.json")


def save_credentials_file(data: dict[str, str]) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f)
        print(f"Credentials saved successfully to {file_path}")


def load_credentials() -> dict[str, str] | str:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return "FileNotFoundError"
    except json.decoder.JSONDecodeError:
        return "JSONDecodeError"
    except Exception as e:
        return f"Error: {e}"


# save_credentials_file({"username": "admin", "password": "admin"})
# print(load_credentials())
