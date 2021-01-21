from .basedao import BaseDao


class MovieDao(BaseDao):

    def insertMovieData(self, params):
        sql = "insert into imdb_data (title, rating, metascore, duration, genres, summary, director, stars, cumulative_worldwide_gross, release_date, recommendation, poster_url, poster_localpath) " + \
            "values ( % s, % s, % s, % s, % s, % s, % s, % s,% s,% s,% s,% s,% s)"
        return self.execute(sql, params)


