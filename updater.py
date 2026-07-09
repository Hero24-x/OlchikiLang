import json
import urllib.request
import webbrowser

CURRENT_VERSION = "1.0.0"

UPDATE_URL = (
    "https://raw.githubusercontent.com/"
    "Hero24-x/OlChikiLang/main/latest.json"
)

def check_updates():
    try:

        with urllib.request.urlopen(
            UPDATE_URL,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode()
            )

        latest = data.get("version", CURRENT_VERSION)

        if latest != CURRENT_VERSION:

            print("\n━━━━━━━━━━━━━━━━━━━━")
            print("📢 Update Available")
            print(f"Current : {CURRENT_VERSION}")
            print(f"Latest  : {latest}")

            if data.get("message"):
                print(data["message"])

            print("━━━━━━━━━━━━━━━━━━━━")

            choice = input(
                "Open download page? (Y/N): "
            ).strip().lower()

            if choice == "y":

                webbrowser.open(
                    data["download_url"]
                )

    except Exception:
        pass
