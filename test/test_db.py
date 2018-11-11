from db.db_utils import get_db_session, UserChampion, VideoTag
from db.datamanager import bulk_save_objects_into_db


def test0():
    session = get_db_session()

    objects = [
        UserChampion(0, 'ru', [1, 28]),
        UserChampion(1, 'eu', [3, 4]),
        UserChampion(2, 'eu', [888, 7778])
    ]

    bulk_save_objects_into_db(session, objects, class_name=UserChampion)


def test1():
    session = get_db_session()

    objects = [
        VideoTag(0, [1, 2], ['gpm', 'kda'], ['killer'], ['qwerty'], ['qwerty'], ['ru', 'en']),
        VideoTag(1, [777, 999], ['lats_hit', 'kda'], ['support'], ['abc'], ['123'], ['eu', 'en']),
    ]

    bulk_save_objects_into_db(session, objects, class_name=VideoTag)


if __name__ == '__main__':

    # test0()
    test1()
