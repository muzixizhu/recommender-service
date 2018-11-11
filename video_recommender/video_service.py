from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
import multiprocessing as mp
import schedule
from video_recommender.analysis import fit_and_predict, get_video_by, random
from utils.util import save_pid, logging
import sys
from db.db_utils import DbCursor


q = mp.Queue(1)

if len(sys.argv) == 4:
    period = int(sys.argv[3])
else:
    # every 20 minutes
    period = 20*60*1000


logging(file_name='./recommend_service.log')


class RecommenderHandler(RequestHandler):

    def get(self):

        recommends = self.settings['data']

        if not q.empty():
            recommends = q.get()
            self.settings['data'] = recommends

        try:
            user_id = self.get_argument("user_id", None, True)
            locale = self.get_argument("locale", None, True)

        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:

            try:
                db = self.settings['db']
                videos = video_analysis(user_id, locale, recommends, db)

            except Exception as ex:
                info = 'Bad in recommendations: {}'.format(repr(ex))
                self.set_status(500, reason=str({'success': False, 'message': info}))
                # self.write({'success': False, 'message': info})
            else:
                self.write({'success': True, 'message': '',
                            'video_recommends': [{"video_id": Id} for Id in videos]})


def service_recommender():

    recommends = fit_and_predict()
    db = DbCursor()

    app = Application([
        (r'/api/videos/recommendations', RecommenderHandler),
    ], data=recommends, db=db)

    if len(sys.argv) < 2:
        port, address = 8081, 'localhost'
    else:
        port, address = sys.argv[2], sys.argv[1]

    http_server = HTTPServer(app)
    http_server.listen(port, address=address)
    print('Service of video recommends is listening on http://{}:{}'.format(address, port))
    IOLoop.current().start()


def video_analysis(user_id, locale, recommends, db):

    videos1 = simple_analysis(user_id=user_id, locale=locale, db=db)
    videos2 = basic_analysis(recommends, user_id=user_id)

    videos = []
    videos.extend(videos1)
    videos.extend(videos2)

    return random.sample(videos, min(20, len(videos)))


def simple_analysis(user_id, locale, db):
    return get_video_by(user_id, locale, db)


def basic_analysis(recommends, user_id):

    try:
        videos = [int(Id) for Id, _r in recommends[int(user_id)]]
    except Exception as ex:
        videos = []
    finally:
        return videos


def service_analysis():

    def train_recommender():
        q.put(fit_and_predict())

    schedule.every(period).minutes.do(train_recommender)
    # schedule.every().day.at("2:00").do(train_recommender)

    while True:
        schedule.run_pending()


if __name__ == '__main__':

    p1 = mp.Process(target=service_recommender)
    p2 = mp.Process(target=service_analysis)

    p1.start()
    p2.start()

    print("Http server for video recommend: pid = {}".format(p1.pid))
    print("Service analysis pid: = {}".format(p2.pid))

    save_pid(p1.pid, p2.pid, port=sys.argv[2], file_name='./pid_recommend_service.json')

    p1.join()
    p2.join()

