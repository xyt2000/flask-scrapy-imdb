# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    metascore = scrapy.Field() 
    duration = scrapy.Field()
    genres = scrapy.Field()
    summary = scrapy.Field()
    director = scrapy.Field()
    stars = scrapy.Field()
    cumulative_worldwide_gross = scrapy.Field()
    release_date = scrapy.Field()
    recommendation = scrapy.Field()


    # number_of_vote = scrapy.Field()
    # About = scrapy.Field()
    # Writers = scrapy.Field()
    # recommendation = scrapy.Field()
