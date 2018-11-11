from tornado import httpclient
import multiprocessing as mp
from db.db_service import service_get_data


def client():
    http_client = httpclient.HTTPClient()
    try:
        for _ in range(int(1)):
            response = http_client.fetch("http://localhost:8080/add")
    except httpclient.HTTPError as e:
        print("Error: " + str(e))
    except Exception as e:
        print("Error: " + str(e))


if __name__ == '__main__':

    clients = []

    for _ in range(2):
        p = mp.Process(target=client)
        clients.append(p)
        p.start()

    for client in clients:
        client.join()

