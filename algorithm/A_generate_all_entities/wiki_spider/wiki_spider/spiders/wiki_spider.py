# -*- coding:utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from algorithm.A_generate_all_entities.wiki_spider.wiki_spider.items import WikiSpiderItem


class WikiSpider(scrapy.Spider):
    name = 'wiki_spider'
    allowed_domains = ['en.wikipedia.org']

    def __init__(self):
        self.base_url = 'http://en.wikipedia.org'
        # 课程名
        self.class_name = 'Algorithms_and_data_structures'
        # 已经爬取的主题列表 不重复爬取
        self.crawled_topics = []

    def start_requests(self):
        # 访问课程的category页面，发出请求
        url = 'http://en.wikipedia.org/wiki/Category:' + self.class_name
        yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        # subcategories
        subcategories = soup.find('div', id='mw-subcategories')
        if subcategories != None:
            # 获取item
            category_items = subcategories.find_all('div', class_='CategoryTreeItem')
            # 依次解析所有的category
            for ci in category_items:
                a = ci.find('a')
                yield scrapy.Request(url=self.base_url + a['href'], callback=self.parse_category)
        # subpages
        pages = soup.find('div', id='mw-pages')
        if pages != None:
            # 获取item
            page_items = pages.find_all('a')
            for pi in page_items:
                topic_name = pi.string
                yield scrapy.Request(url=self.base_url + pi['href'], callback=self.parse_page,
                                     meta={'topic_name': topic_name})

    def parse_page(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        topic_name = response.meta['topic_name']
        # 判断是否爬过
        if topic_name not in self.crawled_topics:
            self.crawled_topics.append(topic_name)
            items = WikiSpiderItem()
            items['class_name'] = self.class_name
            items['topic'] = topic_name
            contents = soup.find('div', id='toc')
            if contents != None:
                lis = contents.find_all('li', class_=True)
                facets = []
                for li in lis:
                    li_class = li['class']
                    level_string = li_class[0][9:]
                    facet = li.find('span', class_='toctext').text
                    facets.append(level_string + ' ' + facet)
                items['facets'] = facets
            else:
                items['facets'] = []
            yield items
