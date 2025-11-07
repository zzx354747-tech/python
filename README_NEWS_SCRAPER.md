# 新闻爬虫脚本 / News Web Scraper

一个用于爬取新闻网站的Python爬虫脚本。

A Python web scraper script for crawling news websites.

## 功能特性 / Features

- 🌐 通用新闻网站爬虫
- 📰 支持新闻列表爬取
- 📄 支持新闻文章详情爬取
- 💾 数据保存为JSON格式
- 🔧 可自定义解析规则
- 🛡️ 包含错误处理和超时机制

- 🌐 Generic news website scraper
- 📰 Support for news list scraping
- 📄 Support for news article detail scraping
- 💾 Save data in JSON format
- 🔧 Customizable parsing rules
- 🛡️ Error handling and timeout mechanism

## 安装依赖 / Installation

```bash
pip install -r requirements.txt
```

## 使用方法 / Usage

### 基本使用 / Basic Usage

```bash
python3 news_scraper.py
```

运行后会提示输入新闻列表页面的URL。

After running, you will be prompted to enter the URL of the news list page.

### 在代码中使用 / Use in Code

```python
from news_scraper import NewsScraper

# 创建爬虫实例 / Create scraper instance
scraper = NewsScraper(timeout=10)

# 爬取新闻列表 / Scrape news list
news_list = scraper.scrape_news_list('https://example.com/news', max_items=10)

# 爬取单篇文章 / Scrape single article
article = scraper.scrape_news_article('https://example.com/news/article1')

# 保存数据 / Save data
scraper.save_to_json(news_list, 'news_list.json')
```

## API 说明 / API Documentation

### NewsScraper 类 / NewsScraper Class

#### 初始化 / Initialization

```python
scraper = NewsScraper(timeout=10)
```

参数 / Parameters:
- `timeout` (int): 请求超时时间（秒），默认10秒 / Request timeout in seconds, default 10

#### 主要方法 / Main Methods

##### fetch_page(url)
获取网页内容 / Fetch web page content

参数 / Parameters:
- `url` (str): 网页URL / Web page URL

返回 / Returns:
- `str` or `None`: HTML内容，失败返回None / HTML content, None if failed

##### scrape_news_list(url, max_items=10)
爬取新闻列表 / Scrape news list

参数 / Parameters:
- `url` (str): 新闻列表页面URL / News list page URL
- `max_items` (int): 最大爬取数量，默认10 / Maximum number of items, default 10

返回 / Returns:
- `List[Dict]`: 新闻列表 / List of news items

##### scrape_news_article(url)
爬取单篇新闻文章 / Scrape a single news article

参数 / Parameters:
- `url` (str): 新闻文章URL / News article URL

返回 / Returns:
- `Dict`: 新闻文章详情 / News article details

##### save_to_json(data, filename)
保存数据到JSON文件 / Save data to JSON file

参数 / Parameters:
- `data` (List[Dict]): 要保存的数据 / Data to save
- `filename` (str): 文件名 / Filename

## 运行测试 / Run Tests

```bash
python3 test_news_scraper.py
```

## 注意事项 / Notes

1. ⚠️ 使用爬虫时请遵守网站的robots.txt规则
2. ⚠️ 不要过于频繁地请求，建议添加适当的延迟
3. ⚠️ 不同网站的HTML结构不同，可能需要调整解析规则
4. ⚠️ 建议仅用于学习和研究目的

1. ⚠️ Please follow the website's robots.txt rules when using the scraper
2. ⚠️ Don't make requests too frequently, add appropriate delays
3. ⚠️ Different websites have different HTML structures, parsing rules may need adjustment
4. ⚠️ Recommended for learning and research purposes only

## 自定义解析 / Customize Parsing

如果需要爬取特定的新闻网站，可以继承`NewsScraper`类并重写解析方法：

If you need to scrape a specific news website, you can inherit the `NewsScraper` class and override the parsing methods:

```python
class CustomNewsScraper(NewsScraper):
    def parse_news_list(self, html, base_url=""):
        # 自定义解析逻辑 / Custom parsing logic
        soup = BeautifulSoup(html, 'lxml')
        # ... your custom code ...
        return news_items
    
    def parse_news_article(self, html):
        # 自定义文章解析 / Custom article parsing
        soup = BeautifulSoup(html, 'lxml')
        # ... your custom code ...
        return article
```

## 示例输出 / Example Output

新闻列表 JSON 格式 / News list JSON format:

```json
[
  {
    "title": "示例新闻标题",
    "url": "https://example.com/news/article1"
  },
  {
    "title": "另一条新闻",
    "url": "https://example.com/news/article2"
  }
]
```

文章详情 JSON 格式 / Article details JSON format:

```json
{
  "title": "文章标题",
  "content": "文章内容...",
  "author": "作者名称",
  "publish_time": "2024-01-01",
  "url": "https://example.com/news/article1",
  "scraped_time": "2024-01-01 12:00:00"
}
```

## 依赖项 / Dependencies

- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交问题和拉取请求！

Issues and pull requests are welcome!
