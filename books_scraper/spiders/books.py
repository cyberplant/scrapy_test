import scrapy
from books_scraper.items import BookItem

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BookItem()
            item["title"] = book.css("h3 a::attr(title)").get()
            item["price"] = book.css("p.price_color::text").get()
            rating_class = book.css("p.star-rating::attr(class)").get()
            word = rating_class.split()[-1] if rating_class else ""
            item["rating"] = RATING_MAP.get(word, 0)
            item["availability"] = book.css("p.availability::text").getall()
            item["availability"] = " ".join(
                t.strip() for t in item["availability"] if t.strip()
            )
            item["url"] = response.urljoin(book.css("h3 a::attr(href)").get())
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
