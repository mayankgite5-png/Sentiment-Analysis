import os
import re
import html
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from transformers import pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ConsumerPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

MAGAZINES = {
    "CNET": "cnet.com",
    "ZDNET": "zdnet.com",
    "PCMag": "pcmag.com",
    "PCWorld": "pcworld.com",
    "TechRadar": "techradar.com",
    "Tom's Guide": "tomsguide.com",
    "Tom's Hardware": "tomshardware.com",
}


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
        "panel",
    ],
    "Battery Life": [
        "battery",
        "battery life",
        "battery backup",
        "charging",
        "charge",
        "fast charging",
    ],
    "Processor": [
        "processor",
        "cpu",
        "chip",
        "snapdragon",
        "intel",
        "amd",
        "apple silicon",
        "m chip",
        "mediatek",
        "performance",
    ],
    "Portability": [
        "portable",
        "portability",
        "lightweight",
        "light",
        "heavy",
        "weight",
        "thin",
        "thickness",
    ],
    "Keyboard": [
        "keyboard",
        "key",
        "typing",
        "trackpad",
        "touchpad",
    ],
    "Camera": [
        "camera",
        "webcam",
        "photo",
        "photos",
        "video quality",
    ],
    "Audio": [
        "speaker",
        "speakers",
        "audio",
        "sound",
        "microphone",
        "mic",
    ],
    "Build Quality": [
        "build",
        "durability",
        "durable",
        "hinge",
        "chassis",
        "material",
        "quality",
    ],
    "Design": [
        "design",
        "look",
        "looks",
        "appearance",
        "style",
        "beautiful",
        "ugly",
    ],
    "Connectivity": [
        "wifi",
        "wi-fi",
        "bluetooth",
        "usb",
        "thunderbolt",
        "hdmi",
        "port",
        "ports",
        "connectivity",
    ],
    "Storage": [
        "storage",
        "ssd",
        "hard drive",
        "memory",
        "ram",
    ],
    "Price": [
        "price",
        "pricing",
        "cost",
        "expensive",
        "cheap",
        "value",
        "worth",
    ],
}


POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "amazing",
    "awesome",
    "fast",
    "quick",
    "smooth",
    "beautiful",
    "bright",
    "clear",
    "strong",
    "premium",
    "impressive",
    "solid",
    "responsive",
    "comfortable",
    "lightweight",
    "portable",
    "long",
    "reliable",
    "affordable",
    "value",
    "worth",
    "powerful",
    "efficient",
    "sharp",
    "fantastic",
    "love",
    "lovely",
    "best",
    "superb",
    "clean",
    "easy",
    "helpful",
}


NEGATIVE_WORDS = {
    "bad",
    "poor",
    "terrible",
    "awful",
    "slow",
    "laggy",
    "lag",
    "dim",
    "dark",
    "weak",
    "expensive",
    "overpriced",
    "heavy",
    "bulky",
    "uncomfortable",
    "disappointing",
    "disappointed",
    "problem",
    "problems",
    "issue",
    "issues",
    "bug",
    "bugs",
    "noisy",
    "hot",
    "heating",
    "limited",
    "lacking",
    "worst",
    "hate",
    "difficult",
    "hard",
    "poorly",
    "short",
    "drain",
    "drains",
}


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
    "Price": "Affordable",
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
    "Price": "Expensive",
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.15);
}

.hero {
    padding: 28px 30px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        rgba(70, 80, 160, 0.16),
        rgba(70, 160, 150, 0.10)
    );
    border: 1px solid rgba(128,128,128,0.16);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 36px;
    font-weight: 750;
    margin-bottom: 6px;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.72;
    line-height: 1.5;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 3px;
}

.section-subtitle {
    font-size: 14px;
    opacity: 0.65;
    margin-bottom: 16px;
}

.metric-card {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.16);
    background: rgba(128,128,128,0.035);
    min-height: 110px;
}

.metric-label {
    font-size: 13px;
    opacity: 0.65;
}

.metric-value {
    font-size: 27px;
    font-weight: 700;
    margin-top: 6px;
}

.insight-card {
    padding: 16px 18px;
    border-radius: 13px;
    border: 1px solid rgba(128,128,128,0.15);
    background: rgba(128,128,128,0.035);
    margin-bottom: 10px;
}

.insight-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 5px;
}

.insight-text {
    font-size: 14px;
    line-height: 1.45;
    opacity: 0.78;
}

.theme-positive {
    border-left: 4px solid #2e8b57;
}

.theme-negative {
    border-left: 4px solid #c94c4c;
}

.theme-neutral {
    border-left: 4px solid #888888;
}

.evidence-card {
    padding: 13px 15px;
    border-radius: 11px;
    border: 1px solid rgba(128,128,128,0.13);
    margin-bottom: 9px;
    background: rgba(128,128,128,0.025);
}

.evidence-text {
    font-size: 14px;
    line-height: 1.5;
}

.evidence-source {
    font-size: 12px;
    opacity: 0.6;
    margin-top: 7px;
}

.source-card {
    padding: 14px 16px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.14);
    margin-bottom: 9px;
}

.small-note {
    font-size: 12px;
    opacity: 0.55;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.14);
    padding: 12px;
    border-radius: 12px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SENTIMENT MODEL
# ============================================================

@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    )


def analyze_sentiment(text):
    if text is None:
        return "Neutral", 0.0

    text = str(text).strip()

    if not text:
        return "Neutral", 0.0

    try:
        model = load_sentiment_model()

        result = model(text[:512])[0]

        label = result["label"].lower()
        score = float(result["score"])

        if "positive" in label:
            return "Positive", score

        if "negative" in label:
            return "Negative", score

        return "Neutral", score

    except Exception:
        return heuristic_sentiment(text)


def heuristic_sentiment(text):
    words = re.findall(r"\b[a-zA-Z]+\b", str(text).lower())

    positive = sum(word in POSITIVE_WORDS for word in words)
    negative = sum(word in NEGATIVE_WORDS for word in words)

    if positive > negative:
        return "Positive", min(0.5 + positive * 0.05, 0.99)

    if negative > positive:
        return "Negative", min(0.5 + negative * 0.05, 0.99)

    return "Neutral", 0.5


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_text(text):
    if text is None:
        return ""

    text = html.unescape(str(text))
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def percentage(value, total):
    if total == 0:
        return 0.0

    return round((value / total) * 100, 1)


def shorten_text(text, limit=240):
    text = clean_text(text)

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


def extract_words(text):
    return re.findall(r"\b[a-zA-Z][a-zA-Z0-9'-]+\b", text.lower())


# ============================================================
# YOUTUBE API
# ============================================================

def search_youtube_videos(query, max_results=10):

    if not YOUTUBE_API_KEY:
        return []

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "regionCode": "US",
        "key": YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        videos = []

        for item in data.get("items", []):

            video_id = item.get("id", {}).get("videoId")

            if not video_id:
                continue

            snippet = item.get("snippet", {})

            videos.append(
                {
                    "video_id": video_id,
                    "title": snippet.get("title", "Untitled"),
                    "channel": snippet.get(
                        "channelTitle",
                        "Unknown channel",
                    ),
                    "published_at": snippet.get(
                        "publishedAt",
                        "",
                    ),
                    "thumbnail": (
                        f"https://img.youtube.com/vi/"
                        f"{video_id}/mqdefault.jpg"
                    ),
                    "url": (
                        f"https://www.youtube.com/watch?v="
                        f"{video_id}"
                    ),
                }
            )

        return videos

    except Exception as error:
        st.error(f"YouTube search failed: {error}")
        return []


def get_youtube_comments(video_id, max_results=100):

    if not YOUTUBE_API_KEY:
        return []

    url = (
        "https://www.googleapis.com/youtube/v3/"
        "commentThreads"
    )

    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": min(max_results, 100),
        "textFormat": "plainText",
        "key": YOUTUBE_API_KEY,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        if response.status_code != 200:
            return []

        data = response.json()

        comments = []

        for item in data.get("items", []):

            try:

                comment = (
                    item["snippet"]
                    ["topLevelComment"]
                    ["snippet"]
                )

                comments.append(
                    {
                        "text": clean_text(
                            comment.get("textDisplay", "")
                        ),
                        "author": comment.get(
                            "authorDisplayName",
                            "Unknown",
                        ),
                        "published_at": comment.get(
                            "publishedAt",
                            "",
                        ),
                        "likes": comment.get(
                            "likeCount",
                            0,
                        ),
                        "source": "YouTube",
                        "source_type": "YouTube Comment",
                        "video_title": "",
                        "video_url": (
                            f"https://www.youtube.com/watch?v="
                            f"{video_id}"
                        ),
                    }
                )

            except Exception:
                continue

        return comments

    except Exception:
        return []


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def add_sentiment(df):

    if df.empty:
        return df

    sentiments = []
    scores = []

    for text in df["text"]:

        sentiment, score = analyze_sentiment(text)

        sentiments.append(sentiment)
        scores.append(round(score, 4))

    result = df.copy()

    result["sentiment"] = sentiments
    result["sentiment_score"] = scores

    return result


def sentiment_summary(df):

    if df.empty:
        return {
            "Positive": 0,
            "Neutral": 0,
            "Negative": 0,
            "Positive %": 0,
            "Neutral %": 0,
            "Negative %": 0,
        }

    total = len(df)

    counts = df["sentiment"].value_counts()

    positive = int(counts.get("Positive", 0))
    neutral = int(counts.get("Neutral", 0))
    negative = int(counts.get("Negative", 0))

    return {
        "Positive": positive,
        "Neutral": neutral,
        "Negative": negative,
        "Positive %": percentage(positive, total),
        "Neutral %": percentage(neutral, total),
        "Negative %": percentage(negative, total),
    }


# ============================================================
# FEATURE ANALYSIS
# ============================================================

def feature_matches(text, feature):

    text = clean_text(text).lower()

    terms = FEATURES[feature]

    return any(term in text for term in terms)


def get_feature_context(text, feature):

    text = clean_text(text)

    lower_text = text.lower()

    positions = []

    for term in FEATURES[feature]:

        start = 0

        while True:

            position = lower_text.find(term, start)

            if position == -1:
                break

            positions.append(position)

            start = position + len(term)

    if not positions:
        return text[:350]

    position = positions[0]

    start = max(0, position - 130)

    end = min(
        len(text),
        position + 230,
    )

    return text[start:end]


def classify_feature_context(context):

    words = extract_words(context)

    positive = sum(
        word in POSITIVE_WORDS
        for word in words
    )

    negative = sum(
        word in NEGATIVE_WORDS
        for word in words
    )

    if positive > negative:
        return "Positive"

    if negative > positive:
        return "Negative"

    return "Neutral"


def feature_analysis(df):

    rows = []

    if df.empty:
        return pd.DataFrame(
            columns=[
                "Feature",
                "Mentions",
                "Positive",
                "Neutral",
                "Negative",
                "Positive %",
                "Neutral %",
                "Negative %",
            ]
        )

    for feature in FEATURES:

        feature_rows = []

        for _, row in df.iterrows():

            text = clean_text(row.get("text", ""))

            if feature_matches(text, feature):

                context = get_feature_context(
                    text,
                    feature,
                )

                sentiment = classify_feature_context(
                    context
                )

                feature_rows.append(
                    sentiment
                )

        mentions = len(feature_rows)

        if mentions == 0:
            continue

        positive = feature_rows.count("Positive")
        neutral = feature_rows.count("Neutral")
        negative = feature_rows.count("Negative")

        rows.append(
            {
                "Feature": feature,
                "Mentions": mentions,
                "Positive": positive,
                "Neutral": neutral,
                "Negative": negative,
                "Positive %": percentage(
                    positive,
                    mentions,
                ),
                "Neutral %": percentage(
                    neutral,
                    mentions,
                ),
                "Negative %": percentage(
                    negative,
                    mentions,
                ),
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "Feature",
                "Mentions",
                "Positive",
                "Neutral",
                "Negative",
                "Positive %",
                "Neutral %",
                "Negative %",
            ]
        )

    return pd.DataFrame(rows).sort_values(
        "Mentions",
        ascending=False,
    )


# ============================================================
# THEME GENERATION
# ============================================================

def generate_themes(df):

    themes = []

    feature_df = feature_analysis(df)

    if feature_df.empty:
        return themes

    for _, row in feature_df.iterrows():

        feature = row["Feature"]

        positive_pct = row["Positive %"]
        negative_pct = row["Negative %"]

        if positive_pct > 40:

            themes.append(
                {
                    "theme": (
                        f"{POSITIVE_ADJECTIVES[feature]} "
                        f"{feature}"
                    ),
                    "sentiment": "Positive",
                    "feature": feature,
                    "percentage": positive_pct,
                }
            )

        if negative_pct > 40:

            themes.append(
                {
                    "theme": (
                        f"{NEGATIVE_ADJECTIVES[feature]} "
                        f"{feature}"
                    ),
                    "sentiment": "Negative",
                    "feature": feature,
                    "percentage": negative_pct,
                }
            )

    return themes


# ============================================================
# VERBATIM EVIDENCE
# ============================================================

def get_verbatims(df, feature, sentiment=None, limit=5):

    if df.empty:
        return []

    results = []

    for _, row in df.iterrows():

        text = clean_text(row.get("text", ""))

        if not feature_matches(text, feature):
            continue

        context = get_feature_context(
            text,
            feature,
        )

        detected_sentiment = classify_feature_context(
            context
        )

        if (
            sentiment is not None
            and detected_sentiment != sentiment
        ):
            continue

        results.append(
            {
                "text": context,
                "sentiment": detected_sentiment,
                "source": row.get(
                    "source",
                    "",
                ),
                "title": row.get(
                    "video_title",
                    row.get("title", ""),
                ),
                "url": row.get(
                    "video_url",
                    row.get("url", ""),
                ),
            }
        )

        if len(results) >= limit:
            break

    return results


# ============================================================
# CONSULTATIVE INSIGHTS
# ============================================================

def generate_insights(df, source_name):

    insights = []

    if df.empty:
        return insights

    summary = sentiment_summary(df)

    if summary["Positive %"] >= 50:

        insights.append(
            {
                "title": "Strong Positive Momentum",
                "text": (
                    f"{summary['Positive %']}% of the "
                    f"analysed {source_name.lower()} content "
                    "is classified as positive. This indicates "
                    "a generally favourable consumer conversation."
                ),
            }
        )

    elif summary["Negative %"] >= 50:

        insights.append(
            {
                "title": "Negative Consumer Signal",
                "text": (
                    f"{summary['Negative %']}% of the "
                    f"analysed {source_name.lower()} content "
                    "is classified as negative. The key feature "
                    "themes below can help identify the drivers."
                ),
            }
        )

    else:

        insights.append(
            {
                "title": "Mixed Consumer Conversation",
                "text": (
                    "The conversation contains a combination "
                    "of positive, neutral and negative signals. "
                    "Feature-level analysis helps identify where "
                    "the strongest opportunities or friction points sit."
                ),
            }
        )

    feature_df = feature_analysis(df)

    if not feature_df.empty:

        strongest_positive = feature_df.loc[
            feature_df["Positive %"].idxmax()
        ]

        strongest_negative = feature_df.loc[
            feature_df["Negative %"].idxmax()
        ]

        insights.append(
            {
                "title": "Positive Feature Signal",
                "text": (
                    f"{strongest_positive['Feature']} has "
                    f"{strongest_positive['Positive %']}% "
                    "positive sentiment among its mentions."
                ),
            }
        )

        insights.append(
            {
                "title": "Potential Friction Point",
                "text": (
                    f"{strongest_negative['Feature']} has "
                    f"{strongest_negative['Negative %']}% "
                    "negative sentiment among its mentions."
                ),
            }
        )

    return insights


# ============================================================
# CHARTS
# ============================================================

def sentiment_donut(summary):

    labels = [
        "Positive",
        "Neutral",
        "Negative",
    ]

    values = [
        summary["Positive"],
        summary["Neutral"],
        summary["Negative"],
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.68,
                textinfo="label+percent",
                hovertemplate=(
                    "%{label}: %{value}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        height=330,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10,
        ),
        showlegend=False,
    )

    return fig


def feature_chart(feature_df):

    if feature_df.empty:
        return go.Figure()

    chart_df = feature_df.sort_values(
        "Mentions",
        ascending=True,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=chart_df["Feature"],
            x=chart_df["Positive %"],
            name="Positive",
            orientation="h",
            text=[
                f"{x:.1f}%"
                for x in chart_df["Positive %"]
            ],
            textposition="inside",
        )
    )

    fig.add_trace(
        go.Bar(
            y=chart_df["Feature"],
            x=chart_df["Neutral %"],
            name="Neutral",
            orientation="h",
            text=[
                f"{x:.1f}%"
                for x in chart_df["Neutral %"]
            ],
            textposition="inside",
        )
    )

    fig.add_trace(
        go.Bar(
            y=chart_df["Feature"],
            x=chart_df["Negative %"],
            name="Negative",
            orientation="h",
            text=[
                f"{x:.1f}%"
                for x in chart_df["Negative %"]
            ],
            textposition="inside",
        )
    )

    fig.update_layout(
        barmode="stack",
        height=max(380, len(chart_df) * 42),
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=15,
        ),
        xaxis_title="Sentiment %",
        yaxis_title="",
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
        ),
        xaxis=dict(
            range=[0, 100],
            ticksuffix="%",
        ),
    )

    return fig


# ============================================================
# TECHNOLOGY MAGAZINES
# ============================================================

def search_magazine_articles(device, max_articles=20):

    all_articles = []

    for magazine, domain in MAGAZINES.items():

        query = quote_plus(
            f"{device} site:{domain}"
        )

        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={query}&hl=en-US&gl=US&ceid=US:en"
        )

        try:

            response = requests.get(
                rss_url,
                timeout=20,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64)"
                    )
                },
            )

            response.raise_for_status()

            root = ET.fromstring(
                response.content
            )

            for item in root.findall(".//item"):

                title = item.findtext(
                    "title",
                    default="",
                )

                link = item.findtext(
                    "link",
                    default="",
                )

                published = item.findtext(
                    "pubDate",
                    default="",
                )

                source_element = item.find(
                    "source"
                )

                source_name = (
                    source_element.text
                    if source_element is not None
                    else magazine
                )

                title_clean = clean_text(title)

                if not title_clean:
                    continue

                all_articles.append(
                    {
                        "title": title_clean,
                        "url": link,
                        "published_at": published,
                        "magazine": magazine,
                        "source": source_name,
                    }
                )

        except Exception:
            continue

    if not all_articles:
        return pd.DataFrame(
            columns=[
                "title",
                "url",
                "published_at",
                "magazine",
                "source",
                "text",
            ]
        )

    articles_df = pd.DataFrame(
        all_articles
    ).drop_duplicates(
        subset=["title", "url"]
    )

    articles_df = articles_df.head(
        max_articles
    )

    # Use article title as the analysis text.
    # This keeps the application dependency-light.
    articles_df["text"] = (
        articles_df["title"]
        .apply(clean_text)
    )

    return articles_df


# ============================================================
# UI HELPERS
# ============================================================

def section_header(title, subtitle=None):

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )

    if subtitle:

        st.markdown(
            f'<div class="section-subtitle">'
            f'{subtitle}</div>',
            unsafe_allow_html=True,
        )


def metric_card(label, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insights(df, source_name):

    insights = generate_insights(
        df,
        source_name,
    )

    if not insights:
        return

    section_header(
        "Consultative Insights",
        "Business-oriented interpretation of the consumer conversation.",
    )

    columns = st.columns(
        min(3, len(insights))
    )

    for index, insight in enumerate(insights):

        with columns[
            index % len(columns)
        ]:

            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-title">
                        {insight["title"]}
                    </div>
                    <div class="insight-text">
                        {insight["text"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_verbatims(df):

    feature_df = feature_analysis(df)

    if feature_df.empty:

        st.info(
            "No feature-specific evidence was detected."
        )

        return

    feature_options = feature_df["Feature"].tolist()

    selected_feature = st.selectbox(
        "Select feature",
        feature_options,
        key=f"feature_{id(df)}",
    )

    sentiment_filter = st.selectbox(
        "Evidence type",
        [
            "All",
            "Positive",
            "Negative",
            "Neutral",
        ],
        key=f"sentiment_{id(df)}",
    )

    selected_sentiment = (
        None
        if sentiment_filter == "All"
        else sentiment_filter
    )

    evidence = get_verbatims(
        df,
        selected_feature,
        selected_sentiment,
        limit=8,
    )

    if not evidence:

        st.info(
            "No evidence found for this selection."
        )

        return

    for item in evidence:

        sentiment_class = (
            "theme-positive"
            if item["sentiment"] == "Positive"
            else "theme-negative"
            if item["sentiment"] == "Negative"
            else "theme-neutral"
        )

        st.markdown(
            f"""
            <div class="evidence-card {sentiment_class}">
                <div class="evidence-text">
                    “{html.escape(item["text"])}”
                </div>
                <div class="evidence-source">
                    {html.escape(str(item["source"]))}
                    {" · " + html.escape(str(item["title"])) if item["title"] else ""}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if item["url"]:

            st.markdown(
                f"[Open source ↗]({item['url']})"
            )


def render_youtube_sources(videos):

    if not videos:
        st.info(
            "No YouTube videos were found."
        )
        return

    for video in videos:

        st.markdown(
            f"""
            <div class="source-card">
                <strong>{html.escape(video["title"])}</strong>
                <br>
                <span class="small-note">
                    {html.escape(video["channel"])}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"[Watch on YouTube ↗]({video['url']})"
        )


def render_magazine_sources(article_df):

    if article_df.empty:

        st.info(
            "No technology magazine articles were found."
        )

        return

    for _, article in article_df.iterrows():

        st.markdown(
            f"""
            <div class="source-card">
                <strong>
                    {html.escape(article["title"])}
                </strong>
                <br>
                <span class="small-note">
                    {html.escape(article["magazine"])}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if article["url"]:

            st.markdown(
                f"[Read article ↗]({article['url']})"
            )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            📊 ConsumerPulse AI
        </div>
        <div class="hero-subtitle">
            Consumer intelligence from YouTube conversations
            and technology media — transforming unstructured
            content into sentiment, features, themes and
            actionable insights.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ConsumerPulse AI")

    st.caption(
        "Consumer intelligence workspace"
    )

    st.divider()

    device = st.text_input(
        "Product / Device",
        placeholder="e.g. MacBook Air M4",
    )

    youtube_videos = st.slider(
        "YouTube videos",
        min_value=1,
        max_value=10,
        value=5,
    )

    comments_per_video = st.slider(
        "Comments per video",
        min_value=20,
        max_value=100,
        value=50,
        step=10,
    )

    magazine_articles = st.slider(
        "Magazine articles",
        min_value=5,
        max_value=30,
        value=15,
        step=5,
    )

    st.divider()

    analyze_button = st.button(
        "🔍 Run Consumer Analysis",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.caption(
        "Sources analysed"
    )

    st.markdown(
        """
        • YouTube consumer comments  
        • CNET  
        • ZDNET  
        • PCMag  
        • PCWorld  
        • TechRadar  
        • Tom's Guide  
        • Tom's Hardware
        """
    )


# ============================================================
# SESSION STATE
# ============================================================

if "youtube_df" not in st.session_state:
    st.session_state.youtube_df = pd.DataFrame()

if "youtube_videos" not in st.session_state:
    st.session_state.youtube_videos = []

if "magazine_df" not in st.session_state:
    st.session_state.magazine_df = pd.DataFrame()

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    if not device.strip():

        st.warning(
            "Please enter a product or device first."
        )

        st.stop()

    if not YOUTUBE_API_KEY:

        st.error(
            "YOUTUBE_API_KEY was not found in your .env file."
        )

        st.info(
            "Add your YouTube API key as "
            "YOUTUBE_API_KEY=YOUR_KEY"
        )

        st.stop()

    progress = st.progress(
        0,
        text="Starting analysis...",
    )

    # --------------------------------------------------------
    # YouTube
    # --------------------------------------------------------

    progress.progress(
        10,
        text="Finding relevant YouTube videos...",
    )

    videos = search_youtube_videos(
        device,
        youtube_videos,
    )

    all_comments = []

    total_videos = max(len(videos), 1)

    for index, video in enumerate(videos):

        progress.progress(
            10 + int(
                ((index + 1) / total_videos) * 40
            ),
            text=(
                f"Collecting comments from "
                f"video {index + 1} of {total_videos}..."
            ),
        )

        comments = get_youtube_comments(
            video["video_id"],
            comments_per_video,
        )

        for comment in comments:

            comment["video_title"] = video[
                "title"
            ]

            comment["video_url"] = video[
                "url"
            ]

        all_comments.extend(
            comments
        )

    youtube_df = pd.DataFrame(
        all_comments
    )

    if not youtube_df.empty:

        youtube_df = add_sentiment(
            youtube_df
        )

    # --------------------------------------------------------
    # Magazines
    # --------------------------------------------------------

    progress.progress(
        60,
        text="Finding technology magazine coverage...",
    )

    magazine_df = search_magazine_articles(
        device,
        magazine_articles,
    )

    if not magazine_df.empty:

        magazine_df = add_sentiment(
            magazine_df
        )

    progress.progress(
        100,
        text="Analysis complete.",
    )

    st.session_state.youtube_df = youtube_df

    st.session_state.youtube_videos = videos

    st.session_state.magazine_df = magazine_df

    st.session_state.analysis_done = True

    progress.empty()

    st.success(
        "Consumer analysis completed successfully."
    )


# ============================================================
# ANALYSIS WORKSPACE
# ============================================================

if st.session_state.analysis_done:

    youtube_df = st.session_state.youtube_df

    magazine_df = st.session_state.magazine_df

    youtube_videos = st.session_state.youtube_videos

    # --------------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------

    section_header(
        "Executive Summary",
        "A compact view of the consumer conversation.",
    )

    total_youtube = len(
        youtube_df
    )

    total_articles = len(
        magazine_df
    )

    yt_summary = sentiment_summary(
        youtube_df
    )

    mag_summary = sentiment_summary(
        magazine_df
    )

    summary_columns = st.columns(4)

    with summary_columns[0]:
        metric_card(
            "YouTube Comments",
            f"{total_youtube:,}",
        )

    with summary_columns[1]:
        metric_card(
            "Technology Articles",
            f"{total_articles:,}",
        )

    with summary_columns[2]:
        metric_card(
            "YouTube Positive",
            f"{yt_summary['Positive %']}%",
        )

    with summary_columns[3]:
        metric_card(
            "YouTube Negative",
            f"{yt_summary['Negative %']}%",
        )

    st.write("")

    # --------------------------------------------------------
    # SOURCE TABS
    # --------------------------------------------------------

    youtube_tab, magazine_tab = st.tabs(
        [
            "▶ YouTube Consumer Voice",
            "📰 Technology Magazines",
        ]
    )

    # ========================================================
    # YOUTUBE SECTION
    # ========================================================

    with youtube_tab:

        if youtube_df.empty:

            st.warning(
                "No YouTube comments were collected."
            )

        else:

            section_header(
                "YouTube Consumer Voice",
                "Analysis of consumer comments from the selected videos.",
            )

            kpi_columns = st.columns(3)

            with kpi_columns[0]:

                st.metric(
                    "Positive",
                    f"{yt_summary['Positive %']}%",
                )

            with kpi_columns[1]:

                st.metric(
                    "Neutral",
                    f"{yt_summary['Neutral %']}%",
                )

            with kpi_columns[2]:

                st.metric(
                    "Negative",
                    f"{yt_summary['Negative %']}%",
                )

            st.write("")

            chart_col, insight_col = st.columns(
                [1, 1.5]
            )

            with chart_col:

                section_header(
                    "Sentiment Distribution"
                )

                st.plotly_chart(
                    sentiment_donut(
                        yt_summary
                    ),
                    use_container_width=True,
                )

            with insight_col:

                render_insights(
                    youtube_df,
                    "YouTube",
                )

            st.divider()

            section_header(
                "Feature Analysis",
                "Sentiment percentages are calculated within each feature's mentions.",
            )

            yt_feature_df = feature_analysis(
                youtube_df
            )

            if yt_feature_df.empty:

                st.info(
                    "No technical features were detected."
                )

            else:

                st.plotly_chart(
                    feature_chart(
                        yt_feature_df
                    ),
                    use_container_width=True,
                )

                with st.expander(
                    "View detailed feature percentages"
                ):

                    display_df = yt_feature_df[
                        [
                            "Feature",
                            "Mentions",
                            "Positive %",
                            "Neutral %",
                            "Negative %",
                        ]
                    ].copy()

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                    )

            st.divider()

            section_header(
                "Themes & Verbatim Evidence",
                "Explore the actual consumer language behind each feature.",
            )

            render_verbatims(
                youtube_df
            )

            st.divider()

            section_header(
                "Video Sources",
                "YouTube videos used for the consumer analysis.",
            )

            render_youtube_sources(
                youtube_videos
            )

    # ========================================================
    # TECHNOLOGY MAGAZINES SECTION
    # ========================================================

    with magazine_tab:

        if magazine_df.empty:

            st.warning(
                "No technology magazine coverage was found."
            )

        else:

            section_header(
                "Technology Magazines",
                "Separate analysis of technology media coverage for the selected device.",
            )

            magazine_kpis = st.columns(4)

            with magazine_kpis[0]:

                st.metric(
                    "Articles",
                    f"{total_articles:,}",
                )

            with magazine_kpis[1]:

                st.metric(
                    "Positive",
                    f"{mag_summary['Positive %']}%",
                )

            with magazine_kpis[2]:

                st.metric(
                    "Neutral",
                    f"{mag_summary['Neutral %']}%",
                )

            with magazine_kpis[3]:

                st.metric(
                    "Negative",
                    f"{mag_summary['Negative %']}%",
                )

            st.write("")

            chart_col, insight_col = st.columns(
                [1, 1.5]
            )

            with chart_col:

                section_header(
                    "Media Sentiment"
                )

                st.plotly_chart(
                    sentiment_donut(
                        mag_summary
                    ),
                    use_container_width=True,
                )

            with insight_col:

                render_insights(
                    magazine_df,
                    "Technology Magazine",
                )

            st.divider()

            section_header(
                "Feature Analysis",
                "Feature-level sentiment from technology media coverage.",
            )

            magazine_feature_df = feature_analysis(
                magazine_df
            )

            if magazine_feature_df.empty:

                st.info(
                    "No technical features were detected in the article results."
                )

            else:

                st.plotly_chart(
                    feature_chart(
                        magazine_feature_df
                    ),
                    use_container_width=True,
                )

                with st.expander(
                    "View detailed feature percentages"
                ):

                    display_df = magazine_feature_df[
                        [
                            "Feature",
                            "Mentions",
                            "Positive %",
                            "Neutral %",
                            "Negative %",
                        ]
                    ].copy()

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                    )

            st.divider()

            section_header(
                "Themes & Verbatim Evidence",
                "Explore article evidence associated with each feature.",
            )

            render_verbatims(
                magazine_df
            )

            st.divider()

            section_header(
                "Technology Magazine Sources",
                "Articles discovered across the selected technology publications.",
            )

            render_magazine_sources(
                magazine_df


            )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.markdown(
        """
        <div style="
            padding: 60px 20px;
            text-align: center;
            opacity: 0.72;
        ">
            <div style="font-size: 48px;">🔎</div>
            <h2>Start your consumer research</h2>
            <p>
                Enter a product or device in the sidebar,
                then run the analysis to explore consumer
                sentiment, technical features, themes,
                verbatims and technology media coverage.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ConsumerPulse AI · Consumer sentiment & feature intelligence"
)
