import scrapy
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from mundo_da_cerveja.items import MundoDaCervejaItem


class LinksRotulosSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['mundodacerveja.com']

    start_urls = [
        'https://www.mundodacerveja.com/pesquisa/1/8',
    ]

    def parse(self, response):
        base_url = get_base_url(response)

        for cerveja in Selector(response).xpath('//div[@class="boxItens"]'):
            name = cerveja.xpath('a/p[@class="prodDesc"]/text()').extract_first(),
            image_urls = cerveja.xpath('a/span[@class="wrapImg"]/center/img/@src').extract()
            image_full_urls = [urljoin_rfc(base_url, x).decode() for x in image_urls]

            yield MundoDaCervejaItem(name=name, image_urls=image_full_urls)

        next = response.xpath('//a[@class="btnSeta"]/@href').extract()
        if next[1] is not None:
            yield scrapy.Request(next[1], callback=self.parse)
