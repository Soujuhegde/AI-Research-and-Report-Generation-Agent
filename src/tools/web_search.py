"""
Tavily Web Search Tool - Real-time internet search for the Researcher agent.
"""
from tavily import TavilyClient
from langchain_core.tools import tool
from typing import List, Optional
from src.config.settings import settings
from src.graph.state import SearchResult
from src.utils.logger import app_logger
from src.utils.rate_limiter import RateLimiter

# Rate limit: max 10 searches per minute
rate_limiter = RateLimiter(max_calls=10, period=60.0)

tavily_client = TavilyClient(api_key=settings.tavily_api_key)


def web_search(
    query: str,
    max_results: int = None,
    search_depth: str = "advanced",
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
) -> List[SearchResult]:
    """
    Perform web search using Tavily API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default from settings)
        search_depth: "basic" or "advanced"
        include_domains: List of domains to include
        exclude_domains: List of domains to exclude
    
    Returns:
        List of SearchResult objects
    """
    rate_limiter.wait()
    max_results = max_results or settings.max_search_results

    app_logger.info(f"🔍 Web search: '{query}' (depth={search_depth})")

    try:
        response = tavily_client.search(
            query=query,
            search_depth=search_depth,
            max_results=max_results,
            include_domains=include_domains or [],
            exclude_domains=exclude_domains or [],
            include_answer=True,
            include_raw_content=False,
        )

        results = []
        for r in response.get("results", []):
            results.append(SearchResult(
                url=r.get("url", ""),
                title=r.get("title", ""),
                content=r.get("content", ""),
                score=r.get("score", 0.0),
                published_date=r.get("published_date"),
            ))

        app_logger.info(f"✅ Found {len(results)} results for: '{query}'")
        return results

    except Exception as e:
        app_logger.error(f"❌ Web search failed for '{query}': {e}")
        return []


def search_and_summarize(queries: List[str]) -> tuple[List[SearchResult], str]:
    """
    Run multiple searches and compile all results.
    
    Returns:
        Tuple of (all_results, compiled_text)
    """
    all_results: List[SearchResult] = []

    for query in queries:
        results = web_search(query)
        all_results.extend(results)

    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r.url not in seen_urls:
            seen_urls.add(r.url)
            unique_results.append(r)

    # Compile into readable text
    compiled = []
    for i, r in enumerate(unique_results, 1):
        compiled.append(
            f"[Source {i}] {r.title}\n"
            f"URL: {r.url}\n"
            f"Content: {r.content}\n"
            f"{'='*60}"
        )

    return unique_results, "\n\n".join(compiled)