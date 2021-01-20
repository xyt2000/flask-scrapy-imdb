from .basedao import BaseDao


class MovieDao(BaseDao):

    def insertMovieData(self, params):
        sql = "insert into imdb_data (title, rating, metascore, duration, genres, summary, director, stars, cumulative_worldwide_gross, release_date, recommendation) " + \
            "values ( % s, % s, % s, % s, % s, % s, % s, % s,% s,% s,% s)"
        return self.execute(sql, params)

    def getMovies(self):
        sql = "select * from imdb_data"
        self.execute(sql, ret='dict')
        return self.fetchall()

    def getMovieById(self, id):
        sql = "select * from imdb_data where id = %s"
        param = [id]
        result = self.execute(sql, param, ret="dict")
        return self.fetchone()



    pass


