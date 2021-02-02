import scrapy


class PricespiderSpider(scrapy.Spider):
    name = 'pricespider'
    # podajemy link do strony początkowej analizy
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/all/views/all/']

    def parse(self, response):
        # określamy na jakich selektorach css / xpath znajdują się interesujące nas informacje
        coin_name = response.css("tr.cmc-table-row > td:nth-child(2) > div:nth-child(1) > a:nth-child(2)::text").extract()
        price = response.xpath('//div[@class = "price___3rj7O "]/a/text()').extract()
        count = 0

        for item in zip(coin_name, price):
            # tworzymy dict do przechowywania zebranych informacji
            scraped_data = {
                'Coin_name': item[0],
                'Price': item[1],
            }
            # zwracamy zebrane informacje
            yield scraped_data

        # w przypadku istnienia button Next page
        next_page = response.css('.a-last a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
