# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['cars.av.by']
    start_urls = ['https://cars.av.by/audi']

    def parse(self, response):

        # cars = response.xpath('//div[@class="listing-item"]')
        cars = response.css('div.listing-item')

        for car in cars:

            # TITLE
            title = car.xpath('.//div[@class="listing-item__about"]/h3/a/span').get()
            title = title.replace('<span class="link-text">', '').replace('<!-- -->', '').replace('</span>', '').split()

            made = {
                "brand": title[0],
                "model": title[1],
                "submodel": title[2]
            }

            # LINK
            link = car.xpath('.//div[@class="listing-item__about"]/h3/a/@href').get()

            # IMAGE
            image = car.xpath('.//div[@class="listing-item__photo"]/img/@data-src').get()

            # LOCATION
            location = car.xpath('.//div[@class="listing-item__location"]/text()').get()

            # TIME
            time = car.xpath('.//div[@class="listing-item__date"]/text()').get()

            # YEAR
            year = car.xpath('.//div[@class="listing-item__params"]/div[1]/text()').get()
            year = year.replace('г.', '').strip()

            # ENGINE
            engine = car.xpath('.//div[@class="listing-item__params"]/div[2]').get()
            engine = engine.replace('<div>', '').replace('<!-- -->', '').replace('</div>', '').replace('л,', '').replace(',', '').split()

            engine = {
                "transmision": engine[0],
                "volume": float(engine[1]),
                "type": engine[2]
            }

            # MILES
            miles = car.xpath('.//div[@class="listing-item__params"]/div[3]/span/text()').get()
            try:
                miles = miles.replace('км', '')
                miles = miles.split()
                        
                for x in miles:
                    x = int(x)

                miles = miles[0] + miles[1]
                miles = int(miles)
                # print(type(fmiles))
            except:
                miles = 0 


            # PRICE BY
            price_by = car.xpath('.//div[@class="listing-item__price"]/text()').get()
            price_by = price_by.replace('р.', ' ').strip().split()
            try:
                for x in price_by:
                    x = int(x)
                price_by = price_by[0] + price_by[1]
                price_by = int(price_by)
                # print(type(price_ru))
            except:
                price_by = 0

            # PRICE USD
            price_usd = car.xpath('.//div[@class="listing-item__priceusd"]/text()').get()
            price_usd = price_usd.replace('≈', ' ').replace('$', ' ').strip().split()   
            try:
                for x in price_usd:
                    x = int(x)
                price_usd = price_usd[0] + price_usd[1]
                price_usd = int(price_usd)
            except:
                price_usd = 0

            # absolute_url = f"https://cars.av.by{link}"
            absolute_url = response.urljoin(link)

            # yield response.follow(url=link)
            # print(response.follow(url=link))

            yield {
                'made': made,
                'link': absolute_url,
                'image': image,
                'location': location,
                'time': time,
                'year': year,
                'engine': engine,
                'miles': miles,
                'price_by': price_by,
                'price_usd': price_usd,
            }

        # next = response.xpath('//div[@class="paging__button"]/a/@href').get()
        # next_page = response.urljoin(next)
        # print(next_page)

        # if next_page is not None:
        #     yield response.follow(url=next_page, callback=self.parse)

