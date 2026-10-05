import os
import requests

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


YOUTUBE_API_KEY = os.getenv(
    "YOUTUBE_API_KEY"
)


BASE_URL = (
    "https://www.googleapis.com/youtube/v3"
)


# ============================================================
# CHECK API KEY
# ============================================================

if not YOUTUBE_API_KEY:

    print(
        "WARNING: YOUTUBE_API_KEY not found."
    )


# ============================================================
# SEARCH YOUTUBE VIDEOS
# ============================================================

def search_videos(
    query,
    max_results=10
):

    url = (
        f"{BASE_URL}/search"
    )


    params = {

        "part": "snippet",

        "q": query,

        "type": "video",

        # Focus search on United States
        "regionCode": "US",

        "maxResults": max_results,

        "key": YOUTUBE_API_KEY
    }


    response = requests.get(
        url,
        params=params,
        timeout=30
    )


    response.raise_for_status()


    return response.json()


# ============================================================
# GET YOUTUBE COMMENTS
# ============================================================

def get_comments(
    video_id,
    max_results=100
):

    url = (
        f"{BASE_URL}/commentThreads"
    )


    params = {

        "part": "snippet",

        "videoId": video_id,

        "maxResults": min(
            max_results,
            100
        ),

        "textFormat": "plainText",

        "key": YOUTUBE_API_KEY
    }


    response = requests.get(
        url,
        params=params,
        timeout=30
    )


    # Some videos do not allow comments

    if response.status_code != 200:

        return []


    data = response.json()


    comments = []


    for item in data.get(
        "items",
        []
    ):

        try:

            comment = (
                item[
                    "snippet"
                ][
                    "topLevelComment"
                ][
                    "snippet"
                ]
            )


            comments.append({

                "comment_id":
                    item["id"],

                "author":
                    comment.get(
                        "authorDisplayName"
                    ),

                "text":
                    comment.get(
                        "textDisplay"
                    ),

                "published_at":
                    comment.get(
                        "publishedAt"
                    ),

                "likes":
                    comment.get(
                        "likeCount",
                        0
                    ),

                "video_id":
                    video_id

            })

        except KeyError:

            continue


    return comments

