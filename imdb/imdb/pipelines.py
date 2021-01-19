# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from imdb.dao.moviedao import MovieDao


class ImdbPipeline:
    def process_item(self, item, spider):
        movieDao = MovieDao()

        # title 处理
        item['title'] = item['title'].replace(u'\xa0',u'')

        # duration 处理
        item['duration'] = item['duration'].strip()
        
        # genres 处理
        temp_genres = []
        if item['genres']:
            for genre in item['genres']:
                temp_genres.append(genre.strip())
            item['genres'] = ','.join(temp_genres)
        
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
            temp_cwg = float(temp_cwg.replace(',',''))
            item['cumulative_worldwide_gross'] = temp_cwg
        else:
            item['cumulative_worldwide_gross'] = 0
        

        print('参数:',item)

        params = [item['title'], item['rating'], item['metascore'],
                  item['duration'], item['genres'], item['director'], item['stars'],
                  item['cumulative_worldwide_gross'],item['release_date']]

        result = movieDao.insertMovieData(params)
        if result > 0:
            print("数据写入成功")

        movieDao.commit()
        movieDao.close()

        return item
