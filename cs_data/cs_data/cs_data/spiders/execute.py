import scrapy


class QuotesSpider(scrapy.Spider):
    name = "csgo"

    custom_settings = {
        'CONCURRENT_REQUESTS': '1'
    }

    def start_requests(self):
        urls = [
            # 'https://www.hltv.org/team/5973/liquid'
            'https://www.hltv.org/team/8825/andes',
            'https://www.hltv.org/team/8366/evilvice'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):
        yield{
            "TeamName":response.css("div.profile-team-name::text").extract()
        }
        players = response.xpath('//a[contains(@href, "pla")]/@href').extract()
        for player in players:
            player = 'https://www.hltv.org/stats' + player
            player = player.replace("player","players")
            yield scrapy.Request(url=player,callback=self.player_extract)

    def player_extract(self,response):
        stats = response.css("div.stats-row")
        yield{
            "player":response.css("h1.statsPlayerName::text").extract()
        }
        for stat in stats:
            title =  stat.xpath(".//span/text()")[0].extract()
            number =  stat.xpath(".//span/text()")[1].extract()
            yield{
                title:number
            }
