from apify_client import ApifyClient
import csv
client = ApifyClient("apify_api_5bscKydCARkV1xgbJuHYjzPbzB6lUt0gcamT")

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
                "https://www.linkedin.com/posts/hikmat-beaini_genius-marketing-idea-imagine-your-business-activity-7375777218003742720-y67i?utm_source=share&utm_medium=member_desktop&rcm=ACoAAF_I4q8BZ3hwpD8CoEHpoJCfZSO1nAQIdIg",
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
