from transformers import pipeline


# ============================================================
# LOAD SENTIMENT MODEL
# ============================================================

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


# ============================================================
# ANALYZE SINGLE TEXT
# ============================================================

def analyze_sentiment(text):

    if not text or not str(text).strip():

        return {
            "sentiment": "Neutral",
            "score": 0.0
        }


    # Convert to string

    text = str(text)


    # Limit input length

    text = text[:512]


    result = sentiment_pipeline(
        text
    )[0]


    label = result["label"].lower()


    # Convert model output to standard labels

    if "positive" in label:

        sentiment = "Positive"

    elif "negative" in label:

        sentiment = "Negative"

    else:

        sentiment = "Neutral"


    return {
        "sentiment": sentiment,
        "score": round(
            result["score"],
            4
        )
    }


# ============================================================
# ANALYZE DATAFRAME
# ============================================================

def analyze_dataframe(df):

    sentiments = []
    scores = []


    for text in df["text"]:

        result = analyze_sentiment(
            text
        )

        sentiments.append(
            result["sentiment"]
        )

        scores.append(
            result["score"]
        )


    df["sentiment"] = sentiments

    df["sentiment_score"] = scores


    return df