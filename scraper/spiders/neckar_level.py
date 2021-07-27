import scrapy
import datetime, time


class NeckarLevelSpider(scrapy.Spider):
    name = 'neckarpegel'
    allowed_domains = ['pegelonline.wsv.de']
    start_urls = ['https://www.pegelonline.wsv.de/gast/pegelinformationen?scrollPosition=0&gewaesser=NECKAR']

    def parse(self, response):
        table = response.xpath('//*[@id="pegelinformation_table"]//tbody/tr')
        for row in table:
            if row.xpath('td[1]//text()').extract_first() == None: continue
            date = row.xpath('td[5]//text()').extract_first().lstrip().rstrip()
            times = row.xpath('td[6]//text()').extract_first().lstrip().rstrip()
            timestamp = datetime.datetime(
                *(time.strptime(f'{date}{times}', "%d.%m.%Y%H:%M")[0:6])).isoformat()
            measurement = {
                'location': row.xpath('td[1]//text()').extract_first(),
                'id': int(row.xpath('td[2]//text()').extract_first()),
                'km': float(row.xpath('td[3]//text()').extract_first()),
                'pnp': float(row.xpath('td[4]//text()').extract_first().lstrip().rstrip()),
                'timestamp': timestamp,
                'rel2pnp_cm': int(row.xpath('td[7]//a//text()').extract_first().replace('cm', '').rstrip().lstrip()),
                'water_level_plus_pnp_over_nhn_m': float(row.xpath('td[8]//a//text()').extract_first().replace('m. ü. NHN', '').lstrip().rstrip()),
            }
            yield measurement
