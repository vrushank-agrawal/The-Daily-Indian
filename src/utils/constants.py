WEBSITE = "https://theindiastory.vercel.app"

# Model for sentiment analysis
MODEL_SENTIMENT_ANALYSIS = "ProsusAI/finbert"

# Model for sentence similarity
MODEL_SENTENCE_SIMILARITY = "sentence-transformers/all-mpnet-base-v2"

# Maximum number of API calls to make in a 15 minute window
MAX_CALLS_PER_15_MIN = 30

# Number of API calls made in a day
DAILY_API_LIMIT = 200

# Time window to fetch articles in minutes
TIME_WINDOW = 1440
TIME_WINDOW_MONDAY = 2880

# Time diff between time of available news and curr time
# The news is data is 12 hours behind UTC
# Use EST because datetime is timezone aware
START_TIME_DELAY =  8 * 60 + TIME_WINDOW # (hours * 60) + TIME_BLOCK in minutes
START_TIME_DELAY_MONDAY =  8 * 60 + TIME_WINDOW_MONDAY # (hours * 60) + TIME_BLOCK in minutes

# Domains to exclude
EXCLUDE_DOMAINS = (
    "theweek.in,"
    "washingtontimes.com,"
    "firstpost.com"
)

# Domains to fetch articles from
INCLUDE_DOMAINS = (
    "business-standard.com,"
    "thehindu.com,"
    "indiatvnews.com,"
    "zeenews.india.com"
)

# Columns to clean from the raw API data
# These columns are mostly null or irrelevant
COLS_TO_CLEAN = [
    'ai_tag',
    'ai_region',
    'ai_org',
    'article_id',
    'content',
    'country',
    'creator',
    'image_url',
    'keywords',
    'language',
    'pubDateTZ',
    'sentiment_stats',
    'source_icon',
    'source_id',
    'source_priority',
    'source_url',
    'video_url',
]

# Columns to remove from the dataframe after ML analysis
# Once ML analysis is done, these columns are not needed
COLS_TO_NOT_SELECT = [
    'category',
    'duplicate',
    'pubDate',
    'sentiment',
    'sentiment_score',
    # 'source_name',
]

# These categories are displayed in the newsletter
DISPLAY_CATEGORIES = [
    'business',
    'entertainment',
    'top',
    'technology',
    'sports',
    'top_news'
]