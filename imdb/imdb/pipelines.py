# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from imdb.dao.moviedao import MovieDao
from scrapy.pipelines.images import ImagesPipeline


class ImdbPipeline(ImagesPipeline):
    
    # 获取图片
    def get_media_requests(self, item, info):
        if item['poster_url']:
            yield scrapy.Request(item['poster_url'])

    # 获取图像后处理 item
    def item_completed(self, results, item, info):
        movieDao = MovieDao()

        # title 处理
        item['title'] = item['title'].replace(u'\xa0', u'')

        # duration 处理
        item['duration'] = item['duration'].strip()

        # genres 处理
        temp_genres = []
        if item['genres']:
            for genre in item['genres']:
                temp_genres.append(genre.strip())
            item['genres'] = ','.join(temp_genres)

        # summary 处理
        if item['summary']:
            item['summary'] = item['summary'].strip()

        # stars 处理
        temp_stars = []
        if item['stars']:
            if item['stars'][-1] == 'See full cast & crew':
                item['stars'].pop()
            for star in item['stars']:
                temp_stars.append(star.strip())
            item['stars'] = ','.join(temp_stars)

        # cumulative_worldwide_gross 处理
        if item['cumulative_worldwide_gross']:
            temp_cwg = item['cumulative_worldwide_gross'][-1].strip('$ ')
            temp_cwg = float(temp_cwg.replace(',', ''))
            item['cumulative_worldwide_gross'] = temp_cwg
        else:
            item['cumulative_worldwide_gross'] = 0

        # recommendation 处理
        if item['genres'] or item['director'] or item['stars'] or item['summary']:
            temp_recommendation = [
                item['genres'], item['director'], item['stars'], item['summary']]
            item['recommendation'] = '\n'.join(temp_recommendation)

        # poster_process_result 处理
        # Sample Result for [result['path'] for success, result in results if success][0] : 'full/c49df2c02681d20cb689f44a8ea5f70eb532c240.jpg'
        poster_localpath = "imdb/" +[result['path'] for success, result in results if success][0]
        
        

        # if item['poster_process_result'] and item['poster_process_result'][0]:
        #     poster_localpath = 'imdb/' + item['poster_process_result'][0]['path']
        #     item['poster_url'] = item['poster_process_result'][0]['url']
        

        # print('参数:',item)

        params = [item['title'], item['rating'], item['metascore'], item['duration'], item['genres'],
                  item['summary'], item['director'], item['stars'], item['cumulative_worldwide_gross'],
                  item['release_date'], item['recommendation'], item['poster_url'], poster_localpath]

        result = movieDao.insertMovieData(params)
        if result > 0:
            print("数据写入成功")

        movieDao.commit()
        movieDao.close()

        return item
