import scrapy
from ..items import MovieItem


class ImdbSpider(scrapy.Spider):

    name = 'imdbspider'

    # https://www.imdb.com/search/title/?count=50&groups=top_1000&sort=user_rating
    # start_urls = ['https://www.imdb.com/search/title/?genres=drama']
    start_urls = [
        'https://www.imdb.com/search/title/?count=50&groups=top_1000&sort=user_rating']

    def parse(self, response):
        movies = response.css('.lister-item')

        #第 1 页的 1 - 50 项
        for movie in movies:
            post_url = 'https://www.imdb.com' + \
                movie.css('a::attr(href)').get()

            print("爬取页面列表: ",post_url)
            
            yield scrapy.Request(post_url, callback=self.parse_indetail)

        # 第 1 - 20 页的51 - 550 项
        # number of page
        for i in range(1, 20):
            next_page = 'https://www.imdb.com/search/title/?count=50&groups=top_1000&sort=user_rating&start={}'.format(
                i*50 + 1)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_indetail(self, response):

        item = MovieItem()

        item['title'] = response.xpath('//*[@id="title-overview-widget"]//div[@ class="title_wrapper"]/h1/text()').get() 
        
        item['rating'] = response.xpath('//*[@id="title-overview-widget"]//span[@itemprop="ratingValue"]/text()').get()
        
        item['metascore'] =  response.xpath('//*[@id="title-overview-widget"]//div[@class="titleReviewBarItem"]/a/div/span/text()').get()
        
        # duration 字串需要 pipeline 处理
        item['duration'] = response.css('.subtext').css('time::text').get()
        
        # genres 字串需要 strip 以及合并处理 
        item['genres'] = response.xpath('//*[@id="titleStoryLine"]/div[./h4/text()="Genres:"]/a/text()').getall() 
        
        # summary 字串需要 strip 处理
        item['summary'] = response.xpath('//*[@id="title-overview-widget"]//div[@class="summary_text"]/text()').get()
        
        item['director'] = response.css('.credit_summary_item').css('a::text').get()
        
        # stars 字串需要合并以及抛弃最后一个元素  
        item['stars'] = response.xpath('//*[@id="title-overview-widget"]//div[./h4/text()="Stars:"]/a/text()').getall()
        
        # cwg 需要取第二个元素 
        item['cumulative_worldwide_gross'] = response.xpath('//*[@id="titleDetails"]/div[./h4/text()="Cumulative Worldwide Gross:"]/text()').getall() 

        item['release_date'] = response.xpath('//*[@id="titleYear"]/a/text()').get()
        
        return item
