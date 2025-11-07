#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻网页爬虫脚本
News Web Scraper Script

这个脚本用于爬取新闻网站的文章内容
This script is used to scrape news articles from news websites
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse

# 常量定义 / Constants
MIN_TITLE_LENGTH = 5  # 最小标题长度 / Minimum title length


class NewsScraper:
    """新闻爬虫类 / News Scraper Class"""
    
    def __init__(self, timeout: int = 10):
        """
        初始化爬虫
        
        Args:
            timeout: 请求超时时间（秒）/ Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _validate_url(self, url: str) -> bool:
        """
        验证URL是否安全
        Validate if URL is safe
        
        Args:
            url: 要验证的URL / URL to validate
            
        Returns:
            是否安全 / Whether the URL is safe
        """
        try:
            parsed = urlparse(url)
            # 只允许HTTP和HTTPS协议 / Only allow HTTP and HTTPS
            if parsed.scheme not in ['http', 'https']:
                return False
            # 阻止访问本地地址 / Block access to local addresses
            if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0'] or \
               (parsed.hostname and parsed.hostname.startswith('192.168.')) or \
               (parsed.hostname and parsed.hostname.startswith('10.')) or \
               (parsed.hostname and parsed.hostname.startswith('172.16.')):
                return False
            return True
        except Exception:
            return False
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        获取网页内容
        Fetch web page content
        
        Args:
            url: 网页URL / Web page URL
            
        Returns:
            网页HTML内容，失败返回None / HTML content, None if failed
        """
        # 验证URL安全性 / Validate URL security
        if not self._validate_url(url):
            print(f"Invalid or unsafe URL: {url}")
            return None
            
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_news_list(self, html: str, base_url: str = "") -> List[Dict[str, str]]:
        """
        解析新闻列表页面
        Parse news list page
        
        Args:
            html: HTML内容 / HTML content
            base_url: 基础URL，用于拼接相对链接 / Base URL for relative links
            
        Returns:
            新闻列表 / List of news items
        """
        soup = BeautifulSoup(html, 'lxml')
        news_items = []
        
        # 通用新闻链接选择器 / Generic news link selectors
        # 这里提供了一个通用的解析示例，实际使用时需要根据具体网站调整
        # This is a generic parsing example, adjust for specific websites
        
        # 查找所有链接 / Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            title = link.get_text(strip=True)
            
            # 过滤有效的新闻链接 / Filter valid news links
            if title and len(title) > MIN_TITLE_LENGTH and href:
                # 处理相对URL / Handle relative URLs
                if href.startswith('/'):
                    href = base_url + href
                elif not href.startswith('http'):
                    continue
                
                news_items.append({
                    'title': title,
                    'url': href
                })
        
        return news_items
    
    def parse_news_article(self, html: str) -> Dict[str, str]:
        """
        解析新闻文章详情
        Parse news article details
        
        Args:
            html: HTML内容 / HTML content
            
        Returns:
            新闻文章信息 / News article information
        """
        soup = BeautifulSoup(html, 'lxml')
        
        article = {
            'title': '',
            'content': '',
            'publish_time': '',
            'author': ''
        }
        
        # 尝试获取标题 / Try to get title
        title_tags = soup.find_all(['h1', 'h2'])
        if title_tags:
            article['title'] = title_tags[0].get_text(strip=True)
        
        # 尝试获取文章内容 / Try to get article content
        # 查找可能包含文章内容的标签 / Find tags that might contain article content
        content_tags = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['content', 'article', 'body', 'text']
        ))
        
        if content_tags:
            article['content'] = content_tags[0].get_text(strip=True, separator='\n')
        else:
            # 如果找不到特定内容区域，获取所有段落 / If no specific content area found, get all paragraphs
            paragraphs = soup.find_all('p')
            article['content'] = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # 尝试获取发布时间 / Try to get publish time
        time_tags = soup.find_all(['time', 'span'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['time', 'date', 'publish']
        ))
        if time_tags:
            article['publish_time'] = time_tags[0].get_text(strip=True)
        
        # 尝试获取作者 / Try to get author
        author_tags = soup.find_all(['span', 'div'], class_=lambda x: x and 'author' in str(x).lower())
        if author_tags:
            article['author'] = author_tags[0].get_text(strip=True)
        
        return article
    
    def scrape_news_list(self, url: str, max_items: int = 10) -> List[Dict[str, str]]:
        """
        爬取新闻列表
        Scrape news list
        
        Args:
            url: 新闻列表页面URL / News list page URL
            max_items: 最大爬取数量 / Maximum number of items to scrape
            
        Returns:
            新闻列表 / List of news items
        """
        print(f"正在爬取新闻列表: {url}")
        print(f"Scraping news list: {url}")
        
        html = self.fetch_page(url)
        if not html:
            return []
        
        # 提取基础URL / Extract base URL
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        news_items = self.parse_news_list(html, base_url)
        
        # 去重 / Remove duplicates
        seen_urls = set()
        unique_items = []
        for item in news_items:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_items.append(item)
                if len(unique_items) >= max_items:
                    break
        
        print(f"找到 {len(unique_items)} 条新闻")
        print(f"Found {len(unique_items)} news items")
        
        return unique_items
    
    def scrape_news_article(self, url: str) -> Dict[str, str]:
        """
        爬取单篇新闻文章
        Scrape a single news article
        
        Args:
            url: 新闻文章URL / News article URL
            
        Returns:
            新闻文章详情 / News article details
        """
        print(f"正在爬取文章: {url}")
        print(f"Scraping article: {url}")
        
        html = self.fetch_page(url)
        if not html:
            return {}
        
        article = self.parse_news_article(html)
        article['url'] = url
        article['scraped_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return article
    
    def save_to_json(self, data: List[Dict], filename: str):
        """
        保存数据到JSON文件
        Save data to JSON file
        
        Args:
            data: 要保存的数据 / Data to save
            filename: 文件名 / Filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {filename}")
            print(f"Data saved to: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
            print(f"Failed to save file: {e}")


def main():
    """主函数 - 示例用法 / Main function - Example usage"""
    
    # 创建爬虫实例 / Create scraper instance
    scraper = NewsScraper(timeout=10)
    
    # 示例：爬取新闻列表 / Example: Scrape news list
    # 注意：这里使用的是示例URL，实际使用时请替换为真实的新闻网站URL
    # Note: This uses an example URL, replace with a real news website URL in actual use
    
    print("=" * 60)
    print("新闻爬虫示例程序 / News Scraper Example Program")
    print("=" * 60)
    print()
    
    # 示例1: 爬取新闻列表 / Example 1: Scrape news list
    example_url = input("请输入新闻列表页面URL (按Enter使用默认示例): ")
    if not example_url.strip():
        example_url = "https://example.com"
        print(f"使用示例URL: {example_url}")
        print("注意: 这是一个示例URL，请替换为真实的新闻网站")
        print("Note: This is an example URL, please replace with a real news website")
    
    print()
    news_list = scraper.scrape_news_list(example_url, max_items=5)
    
    if news_list:
        print("\n" + "=" * 60)
        print("爬取到的新闻列表: / Scraped news list:")
        print("=" * 60)
        for i, news in enumerate(news_list, 1):
            print(f"\n{i}. 标题/Title: {news['title']}")
            print(f"   链接/URL: {news['url']}")
        
        # 示例2: 爬取第一篇新闻的详细内容 / Example 2: Scrape details of the first news article
        if len(news_list) > 0:
            print("\n" + "=" * 60)
            print("爬取第一篇新闻的详细内容...")
            print("Scraping details of the first news article...")
            print("=" * 60)
            
            first_article = scraper.scrape_news_article(news_list[0]['url'])
            
            if first_article:
                print(f"\n标题/Title: {first_article.get('title', 'N/A')}")
                print(f"作者/Author: {first_article.get('author', 'N/A')}")
                print(f"发布时间/Publish Time: {first_article.get('publish_time', 'N/A')}")
                print(f"内容预览/Content Preview: {first_article.get('content', '')[:200]}...")
        
        # 保存结果 / Save results
        scraper.save_to_json(news_list, 'news_list.json')
    else:
        print("未能爬取到新闻数据")
        print("Failed to scrape news data")
    
    print("\n" + "=" * 60)
    print("爬虫程序结束 / Scraper program finished")
    print("=" * 60)


if __name__ == "__main__":
    main()
