# flask-scrapy-imdb
基于scrapy爬虫实现对imdb数据的采集，输入到mysql数据库 并使用flask进行展示

基于echarts绘制图表 



### Scrapy IMDB

2021/1/21 Updates:

1. 修改爬虫，爬取电影海报，海报图片存放在 imdb/posters/full 

2. 在数据库表 imdb_data 中添加 poster_url 和 poster_localpath 字段，分别存储电影海报图片的地址和路径

3. 含有图片地址和路径的新的数据库脚本:

   [Dump20210121.sql](./Dump20210121.sql)

