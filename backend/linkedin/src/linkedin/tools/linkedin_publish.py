import os
import requests

def linkedin_publish(post_text: str) -> str:
    """
    Publishes `post_text` to LinkedIn.
    Returns the post URL or error message.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    org = os.getenv("LINKEDIN_ORGANIZATION_ID")
    api = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    payload = {
        "author": f"urn:li:organization:{org}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    r = requests.post(api, headers=headers, json=payload)
    if r.status_code == 201:
        urn = r.json().get("id")
        return f"https://www.linkedin.com/feed/update/{urn}"
    else:
        return f"Error {r.status_code}: {r.text}"
