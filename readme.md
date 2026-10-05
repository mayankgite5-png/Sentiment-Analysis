# ConsumerPulse AI

### AI-Powered Consumer Sentiment & Market Intelligence Platform

ConsumerPulse AI is an NLP-powered consumer research platform designed to analyze online conversations and technology content to identify **consumer sentiment, product features, emerging themes, pain points, and actionable market insights**.

The platform brings together consumer opinions from multiple digital sources and converts unstructured text into structured insights that can support **market research, product strategy, competitive intelligence, and consumer experience analysis**.

---

## 📌 Project Overview

Consumers express their opinions across multiple digital platforms such as YouTube, Reddit, X (Twitter), and technology publications.

Traditional market research often requires manually reviewing large volumes of these conversations, making it difficult to identify patterns quickly.

**ConsumerPulse AI** addresses this challenge by collecting and analyzing digital content and transforming it into a structured research framework.

The platform can answer questions such as:

* What are consumers saying about a product?
* Which product features are driving positive sentiment?
* Which features are creating dissatisfaction?
* What are the most frequently discussed themes?
* How do opinions differ across platforms?
* What are technology publications saying about the product?
* What specific consumer comments support each finding?
* What actions could brands consider based on these insights?

---

# 🎯 Business Objective

The primary objective of ConsumerPulse AI is to transform unstructured online consumer conversations into **actionable market intelligence**.

The platform is designed to help researchers and business teams:

* Understand consumer perception
* Identify product strengths and weaknesses
* Detect feature-level sentiment
* Discover recurring consumer themes
* Compare opinions across digital sources
* Identify potential product improvement areas
* Support product positioning and strategy
* Generate evidence-backed consumer insights

---

# 🔎 Data Sources

ConsumerPulse AI analyzes content from multiple sources.

## 1. YouTube Consumer Voice

YouTube comments are analyzed to understand direct consumer opinions surrounding a product or topic.

The platform retrieves:

* Video titles
* Video URLs
* Video comments
* Comment authors
* Comment dates
* Comment likes

The dashboard also displays the videos used as research sources.

---

## 2. Technology Magazines

ConsumerPulse AI searches technology publications to provide a professional/editorial perspective alongside consumer opinions.

The platform can analyze articles from sources such as:

* CNET
* ZDNET
* PCMag
* PCWorld
* TechRadar
* Tom's Guide
* Tom's Hardware

Technology articles provide additional context around product performance, specifications, usability, and competitive positioning.

---

## 3. Reddit

Reddit discussions are analyzed as a separate source of consumer and community opinions.

Reddit can provide:

* Product experiences
* Complaints
* Recommendations
* Use cases
* Feature discussions
* Community opinions

---

## 4. X (Twitter)

X posts can be analyzed to capture shorter-form, real-time public conversations around a product or topic.

This source can help identify:

* Immediate reactions
* Positive/negative opinions
* Product complaints
* Feature discussions
* Emerging conversations

---

# 🧠 NLP & Sentiment Analysis

ConsumerPulse AI uses Natural Language Processing (NLP) to classify consumer opinions.

The primary sentiment model is:

**CardiffNLP Twitter RoBERTa Sentiment Model**

The model classifies text into:

* Positive
* Negative
* Neutral

Each analyzed text receives a sentiment classification and confidence score.

The application also includes a fallback sentiment approach to maintain functionality when the NLP model is unavailable.

---

# ⚙️ Feature-Level Analysis

One of the key capabilities of ConsumerPulse AI is **feature-level consumer sentiment analysis**.

Instead of only measuring overall product sentiment, the platform identifies sentiment around specific product features.

For technology products, example features include:

* Display
* Battery Life
* Processor
* Portability
* Keyboard
* Performance
* Camera
* Design
* Build Quality
* Software
* Connectivity
* Price

This enables a more useful research question:

> "What exactly is driving consumer satisfaction or dissatisfaction?"

For example:

### Positive themes

* Good display
* Fast processor
* Excellent battery
* Lightweight design
* Comfortable keyboard

### Negative themes

* Poor display
* Slow processor
* Short battery life
* Heavy design
* Uncomfortable keyboard

---

# 📊 Theme Analysis

ConsumerPulse AI converts feature-level sentiment into structured themes.

Themes are categorized into:

### Positive Themes

Examples:

* Good Display
* Fast Processor
* Long Battery Life
* Lightweight Design

### Negative Themes

Examples:

* Poor Display
* Slow Processor
* Short Battery Life
* Heavy Design

### Neutral Themes

Examples:

* Display specifications
* Processor specifications
* Battery capacity
* Keyboard layout

Theme percentages are presented in the dashboard to make the findings easier to interpret.

---

# 💬 Consumer Verbatims

ConsumerPulse AI provides supporting verbatims for identified themes.

This is important from a market research perspective because quantitative findings should be supported by actual consumer language.

For example:

**Theme: Good Display**

> "The display looks fantastic and is very bright."

**Theme: Poor Battery Life**

> "Battery drains much faster than I expected."

Verbatims allow researchers to understand the context behind the quantitative results.

---

# 📈 Dashboard

The application is built using **Streamlit** and provides an interactive research dashboard.

The dashboard is divided into separate research sections.

---

## ▶ YouTube Consumer Voice

This section focuses on consumer conversations from YouTube.

It provides:

* Videos analyzed
* Consumer sentiment
* Feature-level sentiment
* Theme percentages
* Consumer verbatims
* Source links
* Executive summary
* Consultative insights

---

## 📰 Technology Magazines

This section provides an editorial/technology publication perspective.

It includes:

* Relevant technology articles
* Article titles
* Publication/source
* Publication dates
* Article links
* Article summaries
* Product-related themes

This section is kept separate from consumer-generated content to avoid mixing **consumer voice** with **professional editorial opinions**.

---

## 💬 Forums & Social

This section analyzes social and community conversations.

It contains separate views for:

### Reddit

Analysis of Reddit discussions around the selected topic.

### X (Twitter)

Analysis of X posts around the selected topic.

The section provides:

* Source-specific sentiment
* Feature/theme analysis
* Positive and negative percentages
* Consumer verbatims
* Source comparison
* Research source library

This separation allows researchers to compare how opinions differ between platforms.

---

# 📊 Key Metrics

ConsumerPulse AI provides several research-oriented metrics.

Examples include:

* Total content analyzed
* Positive sentiment %
* Negative sentiment %
* Neutral sentiment %
* Feature sentiment %
* Theme distribution
* Platform-level sentiment
* Source-level comparisons

The dashboard focuses on **percentages and proportions** rather than only raw counts, making results easier to interpret from a market research perspective.

---

# 💡 Consultative Insights

ConsumerPulse AI goes beyond descriptive analytics by generating research-oriented interpretations.

For example:

### Finding

Battery-related conversations show a high proportion of negative sentiment.

### Consumer Signal

Consumers repeatedly mention short battery life and frequent charging.

### Potential Business Implication

Battery performance may represent a product experience weakness that could affect overall consumer satisfaction.

### Recommended Consideration

The brand could investigate battery optimization, charging experience, and communication of expected battery performance.

---

# 🏗️ System Architecture

The simplified workflow is:

```text
                    ConsumerPulse AI
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     YouTube            Reddit             X/Twitter
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                    Data Collection
                           │
                           ▼
                     Text Cleaning
                           │
                           ▼
                  Sentiment Analysis
                           │
                           ▼
                 Feature Identification
                           │
                           ▼
                    Theme Detection
                           │
                           ▼
                 Percentage Calculation
                           │
                           ▼
                    Verbatim Analysis
                           │
                           ▼
                 Consultative Insights
                           │
                           ▼
                  Streamlit Dashboard
```

Technology magazine content follows a separate research pipeline:

```text
Technology Publications
          │
          ▼
     Article Search
          │
          ▼
    Relevant Articles
          │
          ▼
   Article Information
          │
          ▼
 Technology Magazine View
```

---

# 🛠️ Technology Stack

## Programming Language

* Python

## Dashboard

* Streamlit

## Data Processing

* Pandas
* NumPy

## Data Visualization

* Plotly

## NLP

* Hugging Face Transformers
* CardiffNLP RoBERTa Sentiment Model
* PyTorch

## APIs

* YouTube Data API v3
* X API

## Web/Data Retrieval

* Requests
* RSS / Google News feeds

## Environment Management

* python-dotenv

---

# 📁 Project Structure

The final project structure should look similar to:

```text
ConsumerPulse/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── data/
    └── comments_sample.csv
```

### File Description

| File                       | Purpose                                                   |
| -------------------------- | --------------------------------------------------------- |
| `app.py`                   | Main Streamlit application                                |
| `requirements.txt`         | Python dependencies                                       |
| `README.md`                | Project documentation                                     |
| `.gitignore`               | Prevents secrets and temporary files from being committed |
| `.env.example`             | Template for required API credentials                     |
| `data/comments_sample.csv` | Optional sanitized sample dataset                         |

> If the final version of `app.py` imports separate modules such as `sentiment.py`, `youtube_api.py`, `analysis.py`, or `tech_articles.py`, those modules should also be included in the repository. Do not commit unused duplicate versions of the code.

---

# 🔐 API Configuration

ConsumerPulse AI uses API credentials for external data sources.

Create a `.env` file in the project root:

```text
YOUTUBE_API_KEY=your_youtube_api_key_here
X_BEARER_TOKEN=your_x_bearer_token_here
```

The actual `.env` file **must not be uploaded to GitHub**.

Instead, create:

```text
.env.example
```

with:

```text
YOUTUBE_API_KEY=your_youtube_api_key_here
X_BEARER_TOKEN=your_x_bearer_token_here
```

This allows other users to understand which credentials are required without exposing your private keys.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd ConsumerPulse
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure API credentials

Create a `.env` file:

```text
YOUTUBE_API_KEY=your_youtube_api_key
X_BEARER_TOKEN=your_x_bearer_token
```

---

## 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📋 Example Research Workflow

A typical analysis can follow this process:

### Step 1 — Enter a product/topic

Example:

```text
iPhone 17
```

### Step 2 — Collect consumer conversations

ConsumerPulse AI retrieves relevant:

* YouTube videos/comments
* Reddit discussions
* X posts

### Step 3 — Analyze sentiment

The NLP pipeline classifies content as:

* Positive
* Negative
* Neutral

### Step 4 — Identify product features

The system searches for feature-related discussions such as:

* Display
* Battery
* Processor
* Design
* Portability
* Keyboard

### Step 5 — Generate themes

Examples:

```text
Good Display
Fast Processor
Poor Battery Life
Lightweight Design
```

### Step 6 — Calculate percentages

The dashboard presents the distribution of positive, negative, and neutral themes.

### Step 7 — Review verbatims

Researchers can inspect actual consumer comments supporting each theme.

### Step 8 — Generate business implications

The findings can then be interpreted from a product and market strategy perspective.

---

# 📌 Example Business Questions

ConsumerPulse AI can support questions such as:

### Consumer Experience

* What do consumers like most about the product?
* What are the biggest pain points?

### Product Development

* Which features need improvement?
* Which features are driving satisfaction?

### Competitive Intelligence

* How does consumer perception compare across products?
* Which product attributes are frequently discussed?

### Brand Strategy

* What product strengths should be emphasized?
* Which weaknesses may require better communication?

### Market Research

* What themes are emerging in consumer conversations?
* Are professional reviews aligned with consumer opinions?

---

# ⚠️ Limitations

ConsumerPulse AI is a research prototype and results should be interpreted with appropriate methodological caution.

Potential limitations include:

* Online conversations may not represent the entire target population.
* Platform users may differ from the broader consumer population.
* Sentiment models can misinterpret sarcasm, slang, or context.
* Feature-level sentiment detection may not perfectly understand complex sentences.
* API availability and quotas can affect data collection.
* Search results may not capture every relevant conversation.
* Social media content can contain spam, duplicated content, or biased opinions.

Therefore, ConsumerPulse AI should be used as a **consumer intelligence and exploratory research tool**, rather than as a replacement for representative primary research.

---

# 🔮 Future Enhancements

Potential future improvements include:

* Aspect-based sentiment analysis
* Sentence-level feature attribution
* Topic modeling
* Emotion detection
* Competitive product comparison
* Consumer persona segmentation
* Time-series sentiment tracking
* Automated trend detection
* Price/value perception analysis
* Geographic sentiment analysis
* Advanced semantic search
* SQL-based analytical storage
* Automated research reports
* LLM-powered executive summaries
* Power BI integration
* Cloud deployment
* Scheduled data collection

---

# 🎓 Skills Demonstrated

This project demonstrates practical skills across:

### Data Analytics

* Data collection
* Data cleaning
* Exploratory analysis
* Percentage-based analysis
* Data visualization

### NLP

* Text classification
* Sentiment analysis
* Feature extraction
* Theme detection
* Consumer verbatim analysis

### APIs

* REST API integration
* Authentication
* JSON data processing
* External data collection

### Dashboard Development

* Streamlit
* Interactive filters
* KPI design
* Charts
* Research-oriented UX

### Market Research

* Consumer voice analysis
* Theme identification
* Verbatim analysis
* Insight generation
* Business recommendations

---

# 📈 Project Value

ConsumerPulse AI demonstrates how traditional market research concepts can be combined with modern data analytics and NLP techniques.

Instead of simply answering:

> "Is the product sentiment positive or negative?"

the platform attempts to answer the more useful business question:

> **"Why do consumers feel this way, which product features are driving that perception, what evidence supports the finding, and what could the business consider doing next?"**

This makes ConsumerPulse AI a practical example of combining **market research + data analytics + NLP + AI + interactive dashboards**.

---

# 👨‍💻 Author

**Mayank Gite**

Consumer Research & Data Analytics Project

---

# 📄 Disclaimer

This project is intended for educational, analytical, and demonstration purposes.

Data retrieved from third-party platforms remains subject to the respective platform's terms of service, API policies, and usage restrictions.

API keys and other sensitive credentials should never be committed to the public repository.
