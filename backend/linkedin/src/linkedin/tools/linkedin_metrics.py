import os
import requests

def linkedin_metrics(post_urn: str) -> dict:
    """
    Given a LinkedIn post URN (the final segment of the URL),
    returns a dict with 'views', 'likes', and 'shares'.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    api_base = "https://api.linkedin.com/v2"
    headers = {"Authorization": f"Bearer {token}"}


    sa_resp = requests.get(f"{api_base}/socialActions/{post_urn}", headers=headers)
    if sa_resp.status_code != 200:
        return {"views": 0, "likes": 0, "shares": 0}

    data = sa_resp.json()
    return {
        "views": data.get("viewerCount", 0),
        "likes": data.get("likesSummary", {}).get("totalLikes", 0),
        "shares": data.get("shareStatistics", {}).get("shareCount", 0)
    }
