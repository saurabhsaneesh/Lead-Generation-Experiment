from apify_client import ApifyClient
import csv

client = ApifyClient("apify_api_5bscKydCARkV1xgbJuHYjzPbzB6lUt0gcamT")


with open("importedposts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["post_url"])
    writer.writeheader()

    run_input = {
        "keyword": 'gitex marketing',
        "sort_type": "relevance",
        "limit":50,
        "page_numbe": 1,
        "date_filter": "past-week"
    }

    run = client.actor("apimaestro/linkedin-posts-search-scraper-no-cookies").call(run_input=run_input)

    with open("importedposts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["post_url"])
        writer.writeheader()

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            comments = item.get("stats", {}).get("comments", 0)
            if comments < 4:
                continue

            writer.writerow({
                "post_url": item.get("post_url", ""),
            })

print("Post filtered to importedposts.csv")
