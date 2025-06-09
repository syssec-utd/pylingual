import os
from typing import List
import pandas as pd
from .base import BaseDownloader

class MovieLens100KDownLoader(BaseDownloader):
    DOWNLOAD_URL: str = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
    DEFAULT_PATH: str = os.path.join(os.getcwd(), 'ml-100k')

    def read_ratings(self) -> pd.DataFrame:
        ratings_path: str = os.path.join(self.DEFAULT_PATH, 'u.data')
        df_ratings: pd.DataFrame = pd.read_csv(ratings_path, sep='\t', header=None, engine='python').copy()
        df_ratings.columns = ['userId', 'movieId', 'rating', 'timestamp']
        df_ratings['timestamp'] = pd.to_datetime(df_ratings.timestamp, unit='s')
        return df_ratings

    def read_users(self) -> pd.DataFrame:
        users_path: str = os.path.join(self.DEFAULT_PATH, 'u.user')
        df_users: pd.DataFrame = pd.read_csv(users_path, sep='|', header=None, engine='python', names=['userId', 'age', 'gender', 'occupation', 'zipcode'])
        return df_users[['userId', 'gender', 'age', 'occupation', 'zipcode']]

    def _read_genres(self) -> List[str]:
        genres_path: str = os.path.join(self.DEFAULT_PATH, 'ml-100k/u.genre')
        with open(genres_path, 'r') as outfile:
            genres = outfile.read()
            return [pair.split('|')[0] for pair in genres.split('\n')][:-2]

    def read_items(self) -> pd.DataFrame:
        movies_path: str = os.path.join(self.DEFAULT_PATH, 'u.item')
        genres: List[str] = self._read_genres()
        df_items: pd.DataFrame = pd.read_csv(movies_path, sep='|', header=None, encoding='latin-1', engine='python', names=['movieId', 'title', 'release_date', 'video_release_date', 'URL'] + genres)
        df_items['title'] = df_items['title'].str[:-7]
        df_items['release_date'] = pd.to_datetime(df_items.release_date)
        df_items['genres'] = df_items[genres].dot(df_items[genres].columns + '|')
        df_items['genres'] = df_items['genres'].apply(lambda x: x[:-1].split('|'))
        df_items = df_items.drop(columns=genres + ['video_release_date', 'URL'])
        return df_items[['movieId', 'title', 'genres', 'release_date']]