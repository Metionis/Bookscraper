import scrapy
from bookscraper.items import BookItem
import random
import csv

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        'FEEDS': {
            'file://C:/Users/Admin/Documents/Book Scraper/bookscraper/raw_data/raw_data.json': {
                'format': 'json',
                'overwrite': True,
            },
        },
    }
    
    
    # user_agent_list = [
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:76.0) Gecko/20100101 Firefox/76.0",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:76.0) Gecko/20100101 Firefox/76.0",
    # ]
    
    
    
    def parse(self, response):
        products = response.css('article.product_pod')

        for product in products:
            relative_url = product.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                product_url = 'https://books.toscrape.com/' + relative_url
            else:
                product_url = 'https://books.toscrape.com/catalogue/' + relative_url
            # yield response.follow(product_url, callback=self.parse_book_page, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
            yield response.follow(product_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            # yield response.follow(next_page_url, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        
        table_rows = response.css('table tr')
        book_item = BookItem()

        book_item['url']= response.url,
        book_item['title']= response.css(".product_main h1::text").get(),
        book_item['upc'] = table_rows[0].css('td ::text').get()
        book_item['product_type']= table_rows[1].css('td ::text').get(),
        book_item['price_excl_tax']= table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax']= table_rows[3].css("td ::text").get(),
        book_item['tax']= table_rows[4].css("td ::text").get(),
        book_item['availability']= table_rows[5].css('td ::text').get(),
        book_item['num_reviews']= table_rows[6].css('td ::text').get(),
        book_item['stars']= response.css('p.star-rating').attrib['class'],
        book_item['category']= response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description']= response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),
            
        yield book_item

    # def start_requests(self):
    #     with open('C:\\Users\\Admin\\Documents\\Book Scraper\\bookscraper\\PROXY_LIST\\Free_Proxy_List.csv', 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             proxy_ip = row['IP']
    #             # You may need to modify the column names based on your CSV structure
    #             yield scrapy.Request(url=self.start_urls[0], callback=self.parse, meta={"proxy": f"http://{proxy_ip}"})

