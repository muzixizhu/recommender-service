import json
from tornado.log import enable_pretty_logging


def save_pid(pid1, pid2, port, file_name):
    data = {'http': pid1, 'service': pid2, 'port': port}
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def logging(file_name):
    import logging

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=file_name, filemode='w', format=FORMAT, level=logging.DEBUG)
    enable_pretty_logging()


if __name__ == '__main__':

    logging(file_name='./test.log')


