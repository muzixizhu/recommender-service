from db.db_utils import DbCursor
from surprise import SVD, Dataset, Reader, NormalPredictor
from collections import defaultdict
import pandas as pd
import random


def get_video_by(user_id, locale, db=None):

    videos = []
    if db is None:
        return videos
    else:
        if user_id is not None:
            sql = 'select favorite_champ, locale from user_champion where id = {}'.format(user_id)

            res = db.get(sql)

            if not res:
                return videos

            res = res[0]

            favorite_champs = res['favorite_champ']
            locale = res['locale']

            for Id in favorite_champs:
                sql = 'select id from video_tag where {}  = ANY(champion_ids)'.format(Id)
                for video in db.get(sql):
                    videos.append(video['id'])

        sql = 'select id from video_tag where \'{}\' = ANY(locales);'.format(locale)
        for video in db.get(sql):
            videos.append(video['id'])

        return random.sample(videos, min(10, len(videos)))


def get_top_n(predictions, n=10):
    '''
        Return the top-N recommendation for each user from a set of predictions.

        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.

        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def fit_and_predict():

    try:
        db = DbCursor()
    except Exception as ex:
        return []
    else:
        sql = 'select * from user_video'
        user_videos = db.get(sql)

        if user_videos.__len__()>0:

            df = pd.DataFrame(user_videos)

            reader = Reader(rating_scale=(0, 100))
            data = Dataset.load_from_df(df[['user_id', 'video_id', 'percent']], reader)

            train_set = data.build_full_trainset()
            algo = SVD()
            algo.fit(train_set)

            test_set = train_set.build_anti_testset()
            predictions = algo.test(test_set)

            top_n = get_top_n(predictions, n=10)

            return top_n
        else:
            return []


if __name__ == "__main__":

    # print(get_video_by(user_id=2, locale='eu'))
    print(get_video_by(user_id=None, locale='eu'))



