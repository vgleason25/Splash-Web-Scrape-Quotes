import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()

            return {
                html = splash:html(),
                png = splash:png()
            }
        end
    '''
    def start_requests(self):
        yield SplashRequest(url="http://quotes.toscrape.com/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[@class='quote']"):
            yield {
                'Quote Text': currency.xpath(".//span[@class='text']/text()").get(),
                'Author': currency.xpath(".//span/small[@class='author']/text()").get(),
                'Tags': currency.xpath(".//div[@class='tags']/a/text()").getall()
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            absolute_url = f'http://quotes.toscrape.com{next_page}'
            yield  SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })
