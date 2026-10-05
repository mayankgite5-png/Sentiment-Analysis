import re
from collections import Counter

import pandas as pd


# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = {
    "the", "and", "for", "that", "this", "with", "from",
    "have", "has", "are", "was", "were", "will", "you",
    "your", "they", "their", "but", "not", "very", "can",
    "its", "it's", "into", "about", "than", "then", "also",
    "just", "more", "less", "too", "really", "would",
    "could", "should", "been", "being", "what", "when",
    "where", "which", "while", "there", "here", "some",
    "much", "many", "only", "over", "under", "our", "out",
    "all", "one", "two", "get", "got", "use", "used",
    "using", "device", "product"
}


# ============================================================
# PRODUCT FEATURES
# ============================================================

FEATURES = {

    "Display": [
        "display",
        "screen",
        "oled",
        "amoled",
        "lcd",
        "brightness",
        "resolution",
        "refresh rate",
        "panel"
    ],

    "Battery Life": [
        "battery",
        "battery life",
        "battery backup",
        "charging",
        "charge",
        "charger",
        "runtime"
    ],

    "Processor": [
        "processor",
        "cpu",
        "chip",
        "snapdragon",
        "intel",
        "amd",
        "apple silicon",
        "mediatek",
        "performance",
        "processing"
    ],

    "Portability": [
        "portable",
        "portability",
        "weight",
        "lightweight",
        "thin",
        "thickness",
        "compact"
    ],

    "Keyboard": [
        "keyboard",
        "keys",
        "key travel",
        "typing",
        "trackpad",
        "touchpad"
    ],

    "Camera": [
        "camera",
        "cameras",
        "photo",
        "photos",
        "video",
        "selfie",
        "lens",
        "megapixel"
    ],

    "Audio": [
        "audio",
        "speaker",
        "speakers",
        "sound",
        "bass",
        "treble",
        "microphone"
    ],

    "Build Quality": [
        "build",
        "build quality",
        "chassis",
        "durability",
        "materials",
        "aluminum",
        "metal",
        "plastic"
    ],

    "Design": [
        "design",
        "look",
        "looks",
        "appearance",
        "style",
        "aesthetic"
    ],

    "Connectivity": [
        "wifi",
        "wi-fi",
        "bluetooth",
        "usb",
        "usb-c",
        "thunderbolt",
        "hdmi",
        "ports",
        "connectivity",
        "ethernet"
    ],

    "Storage": [
        "storage",
        "ssd",
        "hard drive",
        "memory",
        "ram",
        "capacity"
    ],

    "Price": [
        "price",
        "pricing",
        "cost",
        "expensive",
        "cheap",
        "affordable",
        "value"
    ]
}


# ============================================================
# SENTIMENT VOCABULARY
# ============================================================

POSITIVE_WORDS = {
    "good", "great", "excellent", "strong", "fast",
    "smooth", "impressive", "amazing", "beautiful",
    "bright", "responsive", "reliable", "premium",
    "solid", "comfortable", "powerful", "clear",
    "long", "efficient", "affordable", "outstanding",
    "fantastic", "useful", "capable", "sharp",
    "vibrant", "quick", "durable"
}


NEGATIVE_WORDS = {
    "bad", "poor", "slow", "weak", "terrible",
    "disappointing", "expensive", "heavy", "dim",
    "limited", "average", "noisy", "uncomfortable",
    "short", "overpriced", "problem", "problems",
    "issue", "issues", "flaw", "flaws", "lacks",
    "lack", "difficult", "awkward", "poorly",
    "mediocre", "weakness", "hot", "heating"
}


# ============================================================
# THEME LABELS
# ============================================================

POSITIVE_ADJECTIVES = {

    "Display": "Good",
    "Battery Life": "Long-lasting",
    "Processor": "Fast",
    "Portability": "Portable",
    "Keyboard": "Responsive",
    "Camera": "Clear",
    "Audio": "Excellent",
    "Build Quality": "Premium",
    "Design": "Attractive",
    "Connectivity": "Good",
    "Storage": "Ample",
    "Price": "Affordable"
}


NEGATIVE_ADJECTIVES = {

    "Display": "Poor",
    "Battery Life": "Short",
    "Processor": "Slow",
    "Portability": "Heavy",
    "Keyboard": "Poor",
    "Camera": "Poor",
    "Audio": "Weak",
    "Build Quality": "Poor",
    "Design": "Unappealing",
    "Connectivity": "Limited",
    "Storage": "Limited",
    "Price": "Expensive"
}


# ============================================================
# CLEANING
# ============================================================

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# KEYWORDS
# ============================================================

def extract_keywords(
    df,
    text_column="text",
    top_n=20
):

    counter = Counter()

    for text in df[text_column].fillna(""):

        words = re.findall(
            r"\b[a-zA-Z][a-zA-Z\-']+\b",
            str(text).lower()
        )

        words = [
            word
            for word in words
            if word not in STOPWORDS
            and len(word) > 2
        ]

        counter.update(words)

    return pd.DataFrame(
        counter.most_common(top_n),
        columns=[
            "keyword",
            "count"
        ]
    )


# ============================================================
# OVERALL SENTIMENT
# ============================================================

def sentiment_summary(df):

    if df.empty:

        return pd.DataFrame(
            columns=[
                "sentiment",
                "count",
                "percentage"
            ]
        )

    result = (
        df["sentiment"]
        .value_counts()
        .rename_axis("sentiment")
        .reset_index(
            name="count"
        )
    )

    result["percentage"] = (
        result["count"]
        / result["count"].sum()
        * 100
    ).round(1)

    return result


# ============================================================
# FEATURE DETECTION
# ============================================================

def find_feature_mentions(text):

    text = clean_text(
        text
    ).lower()

    mentions = []

    for feature, keywords in FEATURES.items():

        if any(
            keyword.lower() in text
            for keyword in keywords
        ):

            mentions.append(
                feature
            )

    return mentions


# ============================================================
# FEATURE MENTION SUMMARY
# ============================================================

def feature_mention_summary(df):

    counts = Counter()

    for text in df["text"].fillna(""):

        mentions = find_feature_mentions(
            text
        )

        for feature in mentions:
            counts[feature] += 1

    result = pd.DataFrame(
        counts.items(),
        columns=[
            "Feature",
            "Mentions"
        ]
    )

    if result.empty:

        return pd.DataFrame(
            columns=[
                "Feature",
                "Mentions"
            ]
        )

    return (
        result
        .sort_values(
            "Mentions",
            ascending=False
        )
        .reset_index(drop=True)
    )


# ============================================================
# FEATURE SENTIMENT
# ============================================================

def detect_feature_sentiment(
    text,
    feature
):

    text = clean_text(
        text
    ).lower()

    keywords = FEATURES.get(
        feature,
        []
    )

    positions = []

    for keyword in keywords:

        for match in re.finditer(
            re.escape(
                keyword.lower()
            ),
            text
        ):

            positions.append(
                match.start()
            )

    if not positions:

        return "Neutral"

    positive_score = 0
    negative_score = 0

    for position in positions:

        context = text[
            max(
                0,
                position - 120
            ):
            min(
                len(text),
                position + 180
            )
        ]

        words = set(
            re.findall(
                r"\b[a-zA-Z]+\b",
                context
            )
        )

        positive_score += len(
            words & POSITIVE_WORDS
        )

        negative_score += len(
            words & NEGATIVE_WORDS
        )

    if positive_score > negative_score:

        return "Positive"

    if negative_score > positive_score:

        return "Negative"

    return "Neutral"


# ============================================================
# FEATURE SENTIMENT ANALYSIS
# ============================================================

def feature_sentiment_analysis(df):

    rows = []

    if df.empty:
        return pd.DataFrame()

    total_documents = len(df)

    for feature in FEATURES:

        feature_df = df[
            df["text"]
            .fillna("")
            .apply(
                lambda x:
                feature in find_feature_mentions(x)
            )
        ]

        if feature_df.empty:
            continue

        sentiments = []

        for text in feature_df["text"]:

            sentiments.append(
                detect_feature_sentiment(
                    text,
                    feature
                )
            )

        counts = Counter(
            sentiments
        )

        total = len(
            sentiments
        )

        # Percentage is based on the documents/comments
        # that actually mention this feature.
        positive_pct = (
            counts.get(
                "Positive",
                0
            )
            / total
            * 100
        )

        neutral_pct = (
            counts.get(
                "Neutral",
                0
            )
            / total
            * 100
        )

        negative_pct = (
            counts.get(
                "Negative",
                0
            )
            / total
            * 100
        )

        rows.append({

            "Feature":
                feature,

            "Mentions":
                total,

            "Positive":
                counts.get(
                    "Positive",
                    0
                ),

            "Neutral":
                counts.get(
                    "Neutral",
                    0
                ),

            "Negative":
                counts.get(
                    "Negative",
                    0
                ),

            "Positive %":
                round(
                    positive_pct,
                    1
                ),

            "Neutral %":
                round(
                    neutral_pct,
                    1
                ),

            "Negative %":
                round(
                    negative_pct,
                    1
                )
        })

    return (
        pd.DataFrame(rows)
        .sort_values(
            "Mentions",
            ascending=False
        )
        .reset_index(drop=True)
    )


# ============================================================
# THEMES
# ============================================================

def generate_feature_themes(
    feature_sentiment
):

    rows = []

    for _, row in feature_sentiment.iterrows():

        feature = row[
            "Feature"
        ]

        rows.append({

            "Feature":
                feature,

            "Positive Theme":
                f"{POSITIVE_ADJECTIVES.get(feature, 'Good')} {feature}",

            "Positive %":
                row["Positive %"],

            "Neutral Theme":
                f"Mixed {feature}",

            "Neutral %":
                row["Neutral %"],

            "Negative Theme":
                f"{NEGATIVE_ADJECTIVES.get(feature, 'Poor')} {feature}",

            "Negative %":
                row["Negative %"]
        })

    return pd.DataFrame(
        rows
    )


# ============================================================
# CONSULTATIVE INSIGHTS
# ============================================================

def generate_consultative_insights(
    feature_sentiment,
    source_type="data"
):

    if feature_sentiment.empty:

        return {
            "headline":
                "Insufficient feature-level evidence.",
            "strengths": [],
            "watchouts": [],
            "opportunities": []
        }

    df = feature_sentiment.copy()

    highest_volume = df.loc[
        df["Mentions"].idxmax()
    ]

    strongest_positive = df.loc[
        df["Positive %"].idxmax()
    ]

    strongest_negative = df.loc[
        df["Negative %"].idxmax()
    ]

    strengths = [

        (
            f"{strongest_positive['Feature']} shows "
            f"{strongest_positive['Positive %']:.0f}% "
            f"positive sentiment among "
            f"{int(strongest_positive['Mentions'])} "
            f"relevant mentions."
        )
    ]

    watchouts = [

        (
            f"{strongest_negative['Feature']} has "
            f"{strongest_negative['Negative %']:.0f}% "
            f"negative sentiment among its relevant mentions."
        )
    ]

    opportunities = [

        (
            f"{highest_volume['Feature']} is the most discussed "
            f"product attribute, making it an important area "
            f"for deeper qualitative review."
        )
    ]

    headline = (

        f"{highest_volume['Feature']} generates the highest "
        f"volume of feature-level discussion in the "
        f"{source_type.lower()} data."
    )

    return {

        "headline":
            headline,

        "strengths":
            strengths,

        "watchouts":
            watchouts,

        "opportunities":
            opportunities
    }


# ============================================================
# FEATURE COMMENTS / ARTICLES
# ============================================================

def get_feature_comments(
    df,
    feature
):

    if df.empty:

        return df.copy()

    mask = df[
        "text"
    ].fillna("").apply(

        lambda text:
        feature in find_feature_mentions(
            text
        )
    )

    return df[
        mask
    ].copy()


# ============================================================
# STRUCTURED VERBATIMS
# ============================================================

def get_theme_verbatims(
    df,
    feature,
    sentiment=None,
    max_verbatims=5
):

    if df.empty:

        return pd.DataFrame()

    rows = []

    feature_data = get_feature_comments(
        df,
        feature
    )

    for _, row in feature_data.iterrows():

        text = clean_text(
            row.get(
                "text",
                ""
            )
        )

        if not text:
            continue

        detected_sentiment = detect_feature_sentiment(
            text,
            feature
        )

        if (
            sentiment is not None
            and detected_sentiment != sentiment
        ):
            continue

        # Keep the most useful portion of the text.
        verbatim = text

        if len(verbatim) > 500:

            verbatim = (
                verbatim[:497]
                + "..."
            )

        rows.append({

            "Theme":
                feature,

            "Sentiment":
                detected_sentiment,

            "Verbatim":
                verbatim,

            "Source":
                row.get(
                    "source",
                    "Unknown"
                ),

            "Source Type":
                row.get(
                    "source_type",
                    "Unknown"
                ),

            "Video / Article":
                row.get(
                    "video_title",
                    row.get(
                        "title",
                        ""
                    )
                ),

            "Evidence URL":
                row.get(
                    "video_url",
                    row.get(
                        "url",
                        ""
                    )
                )
        })

        if len(rows) >= max_verbatims:
            break

    return pd.DataFrame(
        rows
    )


# ============================================================
# SOURCE-SPECIFIC THEME TABLE
# ============================================================

def create_theme_verbatim_table(
    df,
    feature_sentiment,
    max_verbatims_per_theme=3
):

    rows = []

    if df.empty:
        return pd.DataFrame()

    for _, feature_row in feature_sentiment.iterrows():

        feature = feature_row[
            "Feature"
        ]

        for sentiment in [
            "Positive",
            "Neutral",
            "Negative"
        ]:

            verbatims = get_theme_verbatims(
                df,
                feature,
                sentiment=sentiment,
                max_verbatims=max_verbatims_per_theme
            )

            if verbatims.empty:
                continue

            for _, verbatim_row in verbatims.iterrows():

                rows.append(
                    verbatim_row.to_dict()
                )

    return pd.DataFrame(
        rows
    )


# ============================================================
# SOURCE-SPECIFIC SUMMARY
# ============================================================

def source_feature_summary(df):

    feature_sentiment = (
        feature_sentiment_analysis(
            df
        )
    )

    if feature_sentiment.empty:
        return feature_sentiment

    return feature_sentiment[
        [
            "Feature",
            "Mentions",
            "Positive %",
            "Neutral %",
            "Negative %"
        ]
    ]


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def sentiment_by_keyword(df):

    result = feature_sentiment_analysis(
        df
    )

    if result.empty:

        return pd.DataFrame(
            columns=[
                "Feature",
                "Positive",
                "Neutral",
                "Negative"
            ]
        )

    return result[
        [
            "Feature",
            "Positive",
            "Neutral",
            "Negative"
        ]
    ]