from apify_client import ApifyClient
import csv
client = ApifyClient("API_TOKEN")#Enter your API Token here 

# 🔍 Helper to extract company from position
def extract_company(position):
    if not position:
        return "N/A"
    if "@" in position:
        return position.split("@")[1].split("|")[0].strip()
    elif " at " in position.lower():
        return position.lower().split(" at ")[1].split("|")[0].strip()
    elif "-" in position:
        return position.split("-")[1].split("|")[0].strip()

run_input = {
    "posts": [
            ""
        ]  
}

run = client.actor("harvestapi/linkedin-post-comments").call(run_input=run_input)

with open("importedcomments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["linkedinUrl", "name", "company"])
    writer.writeheader()

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        actor = item.get("actor", {})
        name = actor.get("name", "N/A")
        position = actor.get("position", "N/A")
        company = extract_company(position)
        linkedin_url = actor.get("linkedinUrl", "N/A")

        if name == "N/A" or company == "N/A":
            continue  

        print(f"{name} | {company} | {linkedin_url}")
        writer.writerow({
            "linkedinUrl": linkedin_url,
            "name": name,
            "company": company
        })
