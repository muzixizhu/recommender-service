import schedule
import time
import datetime
import multiprocessing as mp

q = mp.Queue()


def job():
    now = datetime.datetime.now()
    print("Got time {}".format(now))
    q.put(now)


def create_resource():

    schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        # time.sleep(1)


def get_resources():

    while True:
        while not q.empty():
            print('Received: {}'.format(q.get()))


if __name__ == '__main__':

    p1 = mp.Process(target=create_resource, args=())
    p1.start()

    p2 = mp.Process(target=get_resources, args=())
    p2.start()

    p1.join()
    p2.join()
