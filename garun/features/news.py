"""
Garun AI Assistant - News Service
===================================
Provides news headlines using free RSS feeds
"""

import feedparser
from datetime import datetime


class NewsService:
    """Provides news headlines from RSS feeds"""
    
    def __init__(self):
        # Free RSS feeds organized by category
        self.feeds = {
            "general": [
                "https://feeds.bbci.co.uk/news/rss.xml",  # BBC World News
                "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",  # NY Times
            ],
            "technology": [
                "https://feeds.feedburner.com/TechCrunch/",  # TechCrunch
                "https://www.theverge.com/rss/index.xml",  # The Verge
            ],
            "business": [
                "https://feeds.bbci.co.uk/news/business/rss.xml",  # BBC Business
            ],
            "sports": [
                "https://feeds.bbci.co.uk/sport/rss.xml",  # BBC Sports
            ],
            "india": [
                "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",  # TOI
                "https://www.thehindu.com/feeder/default.rss",  # The Hindu
            ]
        }
    
    def get_news(self, category="general", count=5):
        """
        Get news headlines for a category.
        
        Args:
            category: News category (general, technology, business, sports, india)
            count: Number of headlines to return
            
        Returns:
            Formatted news string
        """
        category = category.lower()
        
        # Get appropriate feeds
        if category in self.feeds:
            feed_urls = self.feeds[category]
        else:
            feed_urls = self.feeds["general"]
            category = "general"
        
        all_entries = []
        
        # Fetch from all feeds in category
        for url in feed_urls:
            try:
                feed = feedparser.parse(url)
                if feed.entries:
                    all_entries.extend(feed.entries[:count])
            except Exception as e:
                print(f"[Garun News] Error fetching {url}: {e}")
                continue
        
        if not all_entries:
            return "I couldn't fetch the news right now. Please try again later."
        
        # Sort by published date if available
        def get_date(entry):
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            return datetime.min
        
        all_entries.sort(key=get_date, reverse=True)
        
        # Take top entries
        top_entries = all_entries[:count]
        
        # Format response
        category_title = category.title()
        response = f"📰 Top {category_title} Headlines:\n\n"
        
        for i, entry in enumerate(top_entries, 1):
            title = entry.get('title', 'No title')
            # Clean up title
            title = title.strip()
            if len(title) > 100:
                title = title[:97] + "..."
            
            response += f"{i}. {title}\n"
        
        return response.strip()
    
    def get_headline(self, category="general"):
        """
        Get a single top headline.
        
        Args:
            category: News category
            
        Returns:
            Single headline string
        """
        category = category.lower()
        
        if category in self.feeds:
            feed_urls = self.feeds[category]
        else:
            feed_urls = self.feeds["general"]
        
        for url in feed_urls:
            try:
                feed = feedparser.parse(url)
                if feed.entries:
                    entry = feed.entries[0]
                    title = entry.get('title', 'No headline available')
                    return f"Top headline: {title}"
            except:
                continue
        
        return "I couldn't fetch the latest headline right now."
    
    def search_news(self, query, count=5):
        """
        Search for news on a specific topic.
        Note: This searches within cached feeds, not a full search.
        
        Args:
            query: Search query
            count: Number of results
            
        Returns:
            Matching headlines
        """
        query_lower = query.lower()
        matching = []
        
        # Search all feeds
        for category, feed_urls in self.feeds.items():
            for url in feed_urls:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries:
                        title = entry.get('title', '').lower()
                        summary = entry.get('summary', '').lower()
                        
                        if query_lower in title or query_lower in summary:
                            matching.append(entry)
                except:
                    continue
        
        if not matching:
            return f"I couldn't find any news about '{query}'."
        
        # Take top matches
        top_matches = matching[:count]
        
        response = f"📰 News about '{query}':\n\n"
        for i, entry in enumerate(top_matches, 1):
            title = entry.get('title', 'No title')[:100]
            response += f"{i}. {title}\n"
        
        return response.strip()
