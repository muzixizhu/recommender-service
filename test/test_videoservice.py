from tornado import escape
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from db.db_utils import get_db_session, VideoTag
import schedule
import datetime
import multiprocessing as mp

q = mp.Queue(1)
session = get_db_session()
info = 'Old data'


class VideoHandler(RequestHandler):

    def get(self):
        # data = escape.json_decode(self.request.body)
        if not q.empty():
            global info
            info = 'Actual data: {}\n'.format(q.get())

        self.write(info)

    def post(self):
        pass


def load_data_service():
    def load_data():
        data = session.query(VideoTag).all()[0]
        q.put(data.__repr__() + '; time: ' + str(datetime.datetime.now()))
        # q.put(datetime.datetime.now())

    schedule.every(10).seconds.do(load_data)
    # schedule.every().day.at("23:59").do(load_data)
    # schedule.every().day.at("11:59").do(load_data)

    while True:
        schedule.run_pending()


def video_service():
    app = Application([
        ('/video', VideoHandler),
    ])
    port, address = 8081, 'localhost'
    http_server = HTTPServer(app)
    http_server.listen(port, address=address)
    print('Listening on http://{}:{}'.format(address, port))
    IOLoop.current().start()


def video_service_run():
    p1 = mp.Process(target=video_service, args=())
    p1.start()

    p2 = mp.Process(target=load_data_service, args=())
    p2.start()

    p1.join()
    p2.join()


if __name__ == '__main__':
    print('OK')

