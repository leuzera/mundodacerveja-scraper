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
#        'https://www.mundodacerveja.com/pesquisa/2/8',
#        'https://www.mundodacerveja.com/pesquisa/3/8',
#        'https://www.mundodacerveja.com/pesquisa/4/8',
#        'https://www.mundodacerveja.com/pesquisa/5/8',
#        'https://www.mundodacerveja.com/pesquisa/6/8',
#        'https://www.mundodacerveja.com/pesquisa/7/8',
#        'https://www.mundodacerveja.com/pesquisa/8/8',
##        'https://www.mundodacerveja.com/pesquisa/10/8',
#        'https://www.mundodacerveja.com/pesquisa/11/8',
#        'https://www.mundodacerveja.com/pesquisa/12/8',
#        'https://www.mundodacerveja.com/pesquisa/13/8',
#        'https://www.mundodacerveja.com/pesquisa/14/8',
#        'https://www.mundodacerveja.com/pesquisa/15/8',
#        'https://www.mundodacerveja.com/pesquisa/16/8',
#        'https://www.mundodacerveja.com/pesquisa/17/8',
#        'https://www.mundodacerveja.com/pesquisa/18/8',
#        'https://www.mundodacerveja.com/pesquisa/19/8',
#        'https://www.mundodacerveja.com/pesquisa/20/8',
#        'https://www.mundodacerveja.com/pesquisa/21/8',
#        'https://www.mundodacerveja.com/pesquisa/22/8',
#        'https://www.mundodacerveja.com/pesquisa/23/8',
#        'https://www.mundodacerveja.com/pesquisa/24/8',
#        'https://www.mundodacerveja.com/pesquisa/25/8',
#        'https://www.mundodacerveja.com/pesquisa/26/8',
#        'https://www.mundodacerveja.com/pesquisa/27/8',
#        'https://www.mundodacerveja.com/pesquisa/28/8',
#        'https://www.mundodacerveja.com/pesquisa/29/8',
#        'https://www.mundodacerveja.com/pesquisa/30/8',
#        'https://www.mundodacerveja.com/pesquisa/31/8',
#        'https://www.mundodacerveja.com/pesquisa/32/8',
##        'https://www.mundodacerveja.com/pesquisa/34/8',
#        'https://www.mundodacerveja.com/pesquisa/35/8',
#        'https://www.mundodacerveja.com/pesquisa/36/8',
#        'https://www.mundodacerveja.com/pesquisa/37/8',
#        'https://www.mundodacerveja.com/pesquisa/38/8',
#        'https://www.mundodacerveja.com/pesquisa/39/8',
#        'https://www.mundodacerveja.com/pesquisa/40/8',
#        'https://www.mundodacerveja.com/pesquisa/41/8',
#        'https://www.mundodacerveja.com/pesquisa/42/8',
#        'https://www.mundodacerveja.com/pesquisa/43/8',
#        'https://www.mundodacerveja.com/pesquisa/44/8',
#        'https://www.mundodacerveja.com/pesquisa/45/8',
#        'https://www.mundodacerveja.com/pesquisa/46/8',
#        'https://www.mundodacerveja.com/pesquisa/47/8',
#        'https://www.mundodacerveja.com/pesquisa/48/8',
#        'https://www.mundodacerveja.com/pesquisa/49/8',
#        'https://www.mundodacerveja.com/pesquisa/50/8',
#        'https://www.mundodacerveja.com/pesquisa/51/8',
#        'https://www.mundodacerveja.com/pesquisa/52/8',
#        'https://www.mundodacerveja.com/pesquisa/53/8',
#        'https://www.mundodacerveja.com/pesquisa/54/8',
#        'https://www.mundodacerveja.com/pesquisa/55/8',
#        'https://www.mundodacerveja.com/pesquisa/56/8',
#        'https://www.mundodacerveja.com/pesquisa/57/8',
#        'https://www.mundodacerveja.com/pesquisa/58/8',
#        'https://www.mundodacerveja.com/pesquisa/59/8',
#        'https://www.mundodacerveja.com/pesquisa/60/8',
#        'https://www.mundodacerveja.com/pesquisa/61/8',
#        'https://www.mundodacerveja.com/pesquisa/62/8',
#        'https://www.mundodacerveja.com/pesquisa/63/8',
#        'https://www.mundodacerveja.com/pesquisa/64/8',
#        'https://www.mundodacerveja.com/pesquisa/65/8',
#        'https://www.mundodacerveja.com/pesquisa/66/8',
#        'https://www.mundodacerveja.com/pesquisa/67/8',
#        'https://www.mundodacerveja.com/pesquisa/68/8',
#        'https://www.mundodacerveja.com/pesquisa/69/8',
#        'https://www.mundodacerveja.com/pesquisa/70/8',
#        'https://www.mundodacerveja.com/pesquisa/71/8',
#        'https://www.mundodacerveja.com/pesquisa/72/8',
#        'https://www.mundodacerveja.com/pesquisa/73/8',
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
