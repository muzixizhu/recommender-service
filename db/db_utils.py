from sqlalchemy import Column, Integer, Float, String
import sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import psycopg2
import psycopg2.extras


Base = declarative_base()


class UserVideo(Base):

    __tablename__ = 'user_video'

    user_id = Column(Integer, primary_key=True)
    video_id = Column(Integer, primary_key=True)
    percent = Column(Integer)

    def __init__(self, user_id, video_id, percent):
        self.user_id = user_id
        self.video_id = video_id
        self.percent = percent

    @staticmethod
    def from_dict(data):
        event = data['event']  # only video event on date 27.09
        return UserVideo(event['user_id'], event['video_id'], event['percent'])

    def __repr__(self):
        return "UserVideo: {}, {}, {}".format(self.user_id, self.video_id, self.percent)

    def __eq__(self, other):
        return self.user_id == other.user_id and self.video_id == other.video_id

    def __hash__(self):
        return hash((self.user_id, self.video_id))


class UserChampion(Base):

    __tablename__ = 'user_champion'

    id = Column(Integer, primary_key=True)
    locale = Column(String)
    favorite_champ = Column(ARRAY(Integer))

    def __init__(self, id, locale, favorite_champ):
        self.id = id
        self.locale = locale
        self.favorite_champ = favorite_champ

    @staticmethod
    def from_dict(data):
        user = data["user"]
        return UserChampion(user['id'], user['locale'], user['favorite_champion_ids'])

    def __repr__(self):
        return "UserChampion: {}, {}, {}".format(self.id, self.locale, self.favorite_champ)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class VideoTag(Base):

    __tablename__ = 'video_tag'

    id = Column(Integer, primary_key=True)
    champion_ids = Column(ARRAY(Integer))
    finders = Column(ARRAY(String))
    roles = Column(ARRAY(String))
    champion_types = Column(ARRAY(String))
    video_type = Column(String)
    locales = Column(ARRAY(String))

    def __init__(self, id, champion_ids, finders, roles, champion_types, video_type, locales):
        self.id = id
        self.champion_ids = champion_ids
        self.finders = finders
        self.roles = roles
        self.champion_types = champion_types
        self.video_type = video_type
        self.locales = locales

    @staticmethod
    def from_dict(data):
        video = data['video']
        return VideoTag(video['id'], video['champion_ids'], video['finders'], video['roles'],
                        video['champion_types'], video['video_type'], video['locales'])

    def __repr__(self):
        return "Video: {}, {}, {}, {}, {}, {}, {}"\
            .format(self.id,
                    self.champion_ids,
                    self.finders,
                    self.roles,
                    self.champion_types,
                    self.video_type,
                    self.locales)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Counter(Base):

    __tablename__ = 'counter'

    count = Column(Integer, primary_key=True)

    def __init__(self, count):
        self.count = count

    def __repr__(self):
        return "Row of VideoTag: {}".format(self.count)


class DbCursor:

    host, port = "localhost", "5432"
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
        # print("Connection with DB is set up")
        self.cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get(self, sql):

        self.cursor.execute(sql)
        res = self.cursor.fetchall()

        return res


def get_db_session():

    engine = create_engine('postgresql://postgres:postgres@localhost:5432', echo=False)

    Base.metadata.create_all(engine, tables=[UserVideo.__table__,
                                             UserChampion.__table__,
                                             VideoTag.__table__])

    Session = scoped_session(sessionmaker(bind=engine))

    return Session()


if __name__ == '__main__':

    session = get_db_session()
    print('OK')

