#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻爬虫脚本
Test script for news scraper
"""

from news_scraper import NewsScraper


def test_scraper_initialization():
    """测试爬虫初始化 / Test scraper initialization"""
    scraper = NewsScraper(timeout=10)
    assert scraper.timeout == 10
    assert 'User-Agent' in scraper.headers
    print("✓ 爬虫初始化测试通过 / Scraper initialization test passed")


def test_parse_html():
    """测试HTML解析 / Test HTML parsing"""
    scraper = NewsScraper()
    
    # 测试HTML示例 / Test HTML example
    html = """
    <html>
        <head><title>Test News</title></head>
        <body>
            <h1>Test Article Title</h1>
            <div class="article-content">
                <p>This is the first paragraph of the article.</p>
                <p>This is the second paragraph of the article.</p>
            </div>
            <span class="author">Test Author</span>
            <time>2024-01-01</time>
        </body>
    </html>
    """
    
    article = scraper.parse_news_article(html)
    
    assert article['title'] == 'Test Article Title'
    assert len(article['content']) > 0
    print("✓ HTML解析测试通过 / HTML parsing test passed")


def test_news_list_parsing():
    """测试新闻列表解析 / Test news list parsing"""
    scraper = NewsScraper()
    
    html = """
    <html>
        <body>
            <a href="/news/article1">First News Article</a>
            <a href="/news/article2">Second News Article</a>
            <a href="https://example.com/news/article3">Third News Article</a>
        </body>
    </html>
    """
    
    news_items = scraper.parse_news_list(html, "https://example.com")
    
    assert len(news_items) > 0
    assert all('title' in item and 'url' in item for item in news_items)
    print("✓ 新闻列表解析测试通过 / News list parsing test passed")


def run_all_tests():
    """运行所有测试 / Run all tests"""
    print("=" * 60)
    print("开始运行测试... / Starting tests...")
    print("=" * 60)
    print()
    
    try:
        test_scraper_initialization()
        test_parse_html()
        test_news_list_parsing()
        
        print()
        print("=" * 60)
        print("所有测试通过! / All tests passed!")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ 测试失败 / Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 测试出错 / Test error: {e}")
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
