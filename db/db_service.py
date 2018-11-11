from tornado import escape
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application
from db.db_utils import get_db_session, UserChampion, VideoTag, UserVideo
from db.datamanager import DataManager
import functools
import multiprocessing as mp
from utils.util import save_pid, logging
import sys


data = DataManager()

if len(sys.argv) == 4:
    period = int(sys.argv[3])
else:
    # every 20 minutes
    period = 20*60*1000


logging(file_name='./db_service.log')


class UserHandler(RequestHandler):

    def post(self):
        global data

        try:
            body = escape.json_decode(self.request.body)
            data.users.put_into_add(UserChampion.from_dict(body))
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})

    def patch(self):
        global data

        user_id = int(self.request.uri.split('/')[-1])

        try:
            body = escape.json_decode(self.request.body)
            body['user']['id'] = user_id
            data.users.put_into_update(UserChampion.from_dict(body))
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})

    def delete(self):
        global data
        user_id = int(self.request.uri.split('/')[-1])

        try:
            data.users.put_into_delete(user_id)
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})


class VideoHandler(RequestHandler):

    def post(self):
        global data

        try:
            body = escape.json_decode(self.request.body)
            data.videos.put_into_add(VideoTag.from_dict(body))
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})

    def patch(self):
        global data
        video_id = int(self.request.uri.split('/')[-1])

        try:
            body = escape.json_decode(self.request.body)
            body['video']['id'] = video_id
            data.videos.put_into_update(VideoTag.from_dict(body))
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})

    def delete(self):
        global data
        video_id = int(self.request.uri.split('/')[-1])

        try:
            data.videos.put_into_delete(video_id)
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.write({'success': True, 'message': ''})


class EventHandler(RequestHandler):

    def post(self):
        # data = self.settings['data_manager']
        global data

        try:
            body = escape.json_decode(self.request.body)
            data.events.put_into_add(UserVideo.from_dict(body))
        except Exception as ex:
            self.set_status(500, reason=str({'success': False, 'message': ex.__repr__()}))
            # self.write({'success': False, 'message': ex.__repr__()})
        else:
            self.set_header("Access-Control-Allow-Origin",
                            "https://morelegends.com, https://morelegends-rc.herokuapp.com/")
            self.write({'success': True, 'message': ''})


def cb(q):
    global data
    data_to_send = data

    if not data_to_send.empty():
        q.put(data_to_send)

    data = DataManager()


def service_get_data(q):

    app = Application([
        (r'/api/users', UserHandler),
        (r'/api/users/\d+', UserHandler),
        (r'/api/videos', VideoHandler),
        (r'/api/videos/\d+', VideoHandler),
        (r'/api/event', EventHandler),
    ], data_manager=data)

    if len(sys.argv) < 2:
        port, address = 8080, 'localhost'
    else:
        port, address = sys.argv[2], sys.argv[1]

    http_server = HTTPServer(app)
    http_server.listen(port, address=address)
    print('DB service is listening on http://{}:{}'.format(address, port))

    callback = functools.partial(cb, q)
    # every time period do callback
    scheduler = PeriodicCallback(callback, period)
    scheduler.start()

    IOLoop.current().start()


def service_save_data(q):
    def save_data(dm):
        session = get_db_session()
        dm.process(session)
        session.close()

    # For initial table creature
    session = get_db_session()
    session.close()

    while True:
        if not q.empty():
            dm = q.get()
            save_data(dm)


if __name__ == '__main__':

    q = mp.Queue(1)

    p1 = mp.Process(target=service_get_data, args=(q,))
    p2 = mp.Process(target=service_save_data, args=(q,))

    p1.start()
    p2.start()

    print("Http server for db: pid = {}".format(p1.pid))
    print("DB service: pid = {}".format(p2.pid))

    save_pid(p1.pid, p2.pid, port=sys.argv[2], file_name='./pid_db_service.json')

    p1.join()
    p2.join()

