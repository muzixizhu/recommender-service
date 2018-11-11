import psycopg2
import psycopg2.extras


class DbCursor:

    # Public IP: 52.183.10.157
    # Private IP: 10.0.1.13

    # host, port = "52.183.10.157", "5432"
    host, port = "10.0.1.13", "5432"

    user, password, dbname = "postgres", "postgres", 'postgres'

    def __init__(self):
        info = "host={0} " \
               "user={1} " \
               "dbname={2} " \
               "password={3} " \
               "port={4}".format(self.host,
                                 self.user,
                                 self.dbname,
                                 self.password,
                                 self.port)

        conn = psycopg2.connect(info)
        print("Connection with DB is set up")
        self.cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get(self, sql):

        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        return res


if __name__ == '__main__':

    db = DbCursor()
    print("OK")
