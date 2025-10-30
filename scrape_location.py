from apify_client import ApifyClient
import csv

client = ApifyClient("API_TOKEN")#Enter your API Token here 

run_input = {
    "url":  "", # Enter Post URL here 
    "start": 19, #no to start from
    "iterations": 9, # no of iterations to run
    "type": "likers" # likers or commenters
}

run = client.actor("scraping_solutions/linkedin-posts-engagers-likers-and-commenters-no-cookies").call(run_input=run_input)

with open("importedlikers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "url_profile", "company"])
    writer.writeheader()

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if item.get("type") == "likers":
            name = item.get("name", "N/A")
            profile = item.get("url_profile", "N/A")
            subtitle = item.get("subtitle", "")

            writer.writerow({
                "name": name,
                "url_profile": profile,
                "company": subtitle
            })

print("Likers with company info saved to importedlikers.csv")
