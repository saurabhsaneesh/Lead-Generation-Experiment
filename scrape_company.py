from apify_client import ApifyClient
import csv
import os

# Apify API Token
client = ApifyClient("")

input_file = "importedcomments.csv"
output_file = "importedcompany.csv"

# Output file with headers if not exists
file_exists = os.path.isfile(output_file)
with open(output_file, "a", newline="", encoding="utf-8") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=["name", "company", "location", "profileUrl"])
    if not file_exists:
        writer.writeheader()

    # Read input CSV
    with open(input_file, "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)

        for row in reader:
            profile_url = row.get("username")
            if not profile_url:
                continue

            print(f"Processing: {profile_url}")

            # Correct Apify Actor + Correct Input format
            run_input = {
                "urls": [profile_url],
                "maxConnectionsPerCrawl": 1,
                "enhanceProfiles": True
            }

            run = client.actor("apimaestro/linkedin-profile-detail").call(
                run_input=run_input
            )

            # Read dataset results
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():

                basic = item.get("basic_info", {})

                writer.writerow({
                    "name": basic.get("fullname", "N/A"),
                    "company": basic.get("current_company", "N/A"),
                    "location": basic.get("location", {}).get("full", "N/A"),
                    "profileUrl": profile_url
                })

print("✅ Data saved to importedcompany.csv")
