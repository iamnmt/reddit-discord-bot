import requests

from reddit.utils.constants import REDDIT_PREFIX_URL

REQUESTS_PARAMS_LIMIT = 25


def fetch_img(headers, subs_to_category, limit=1):
    result_image_urls = dict()

    for sub in subs_to_category.keys():
        for category in subs_to_category[sub]:
            print(f"Fetching images frome /r/{sub}/{category}...")

            res = requests.get(
                f"{REDDIT_PREFIX_URL}/r/{sub}/{category}",
                headers=headers,
                params={"limit": REQUESTS_PARAMS_LIMIT},
            )

            if not res.ok:
                print(f"Failed to fetch /r/{sub}/{category}")
                continue

            if sub not in result_image_urls:
                result_image_urls[sub] = dict()
            for post_info in res.json()["data"]["children"]:
                post_data = post_info["data"]
                if post_data.get("post_hint", False) == "image":
                    if category not in result_image_urls[sub]:
                        result_image_urls[sub][category] = list()
                    result_image_urls[sub][category].append(
                        {
                            "title": post_data["title"],
                            "url": post_data["url_overridden_by_dest"]
                        }
                    )
                if len(result_image_urls[sub]) >= limit:
                    break

    return result_image_urls
