from surprise import SVD, Dataset, Reader, NormalPredictor
from surprise.model_selection import cross_validate
import time
import pandas as pd


def test1():
    # Load the movielens-100k dataset (download it if needed).
    data = Dataset.load_builtin('ml-100k')

    # Use the famous SVD algorithm.
    algo = SVD()
    # Run 5-fold cross-validation and print results.
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


def test0():
    # Load the movielens-100k dataset (download it if needed),
    start = time.time()
    data = Dataset.load_builtin('ml-100k').build_full_trainset()
    print('Data time: %d' % (time.time() - start))

    start = time.time()
    algo = SVD()
    print('SVD time: %d' % (time.time() - start))

    start = time.time()
    # cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    algo.fit(data)
    print('Fit/Validation time: %d' % (time.time() - start))

    start = time.time()
    predictions = algo.test(data.build_testset())
    print('Test time: %d' % (time.time() - start))

    print("Predictions: \n", predictions[0:10])


def test2():
    videos = {'user_id': [1, 2, 3, 4, 5],
              'video_id': [1, 2, 3, 4, 5],
              'percent': [0, 10, 45, 55, 90]}

    df = pd.DataFrame(videos)

    reader = Reader(rating_scale=(0, 100))
    data = Dataset.load_from_df(df[['user_id', 'video_id', 'percent']], reader)

    data = data.build_full_trainset()

    algo = SVD()
    algo.fit(data)

    test_data = data.build_testset()
    # print('Test data: {}'.format(test_data))

    for Id in [1, 2, 3, 4, 5]:
        pred = algo.predict(uid=2, iid=Id, r_ui=None, verbose=True)
        print('Predict result is {}'.format(pred.est))

    # predictions = algo.test(test_data)
    # print('Predictions: {}'.format(predictions))


if __name__ == '__main__':

    test2()
