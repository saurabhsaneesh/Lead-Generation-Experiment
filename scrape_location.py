from apify_client import ApifyClient
import csv

client = ApifyClient("apify_api_5bscKydCARkV1xgbJuHYjzPbzB6lUt0gcamT")

run_input = {
    "usernames": [
        "https://www.linkedin.com/in/saurabhsaneesh"
    ],
    "includeEmail": True
}

run = client.actor("apimaestro/linkedin-profile-full-sections-scraper").call(run_input=run_input)

items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"🔍 Found {len(items)} profiles")

with open("linkedin_profiles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "location", "email"])
    writer.writeheader()

    for item in items:
        print("📄 Profile:", item)  # Debug print
        writer.writerow({
            "name": item.get("name", ""),
            "location": item.get("location", ""),
            "email": item.get("email", "")
        })

print("✅ Saved location and email to linkedin_profiles.csv")
