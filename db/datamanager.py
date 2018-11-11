from db.db_utils import UserChampion, VideoTag, UserVideo
from sqlalchemy import exc
import psycopg2


# This function guarantees right save even if there're repetitions
def bulk_save_objects_into_db(session, objects, class_name):

    try:
        session.bulk_save_objects(objects)
        session.commit()
    except exc.IntegrityError:
        session.rollback()
        save_with_repetitions(session, objects, class_name)
    except psycopg2.IntegrityError:
        session.rollback()
        save_with_repetitions(session, objects, class_name)


def save_with_repetitions(session, to_add, class_name):

    existings = {existing: existing for existing in session.query(class_name).all()}
    updates, addings = {}, {}

    for new in to_add:
        if new in updates:
            updates[new] = new
        else:
            if new in existings:
                updates[new] = new
            else:
                if new in addings:
                    updates[new] = new
                else:
                    addings[new] = new

    # to add
    if addings:
        session.bulk_save_objects(list(addings.values()))
        can_commit = True

    # to update
    if updates:
        news = []
        for update in updates.values():
            to_update = session.query(class_name).filter_by(id=update.id).first()

            if to_update is not None:
                if class_name == UserChampion:
                    to_update.locale = update.locale
                    to_update.favorite_champ = update.favorite_champ
                elif class_name == VideoTag:
                    to_update.champion_ids = update.champion_ids
                    to_update.finders = update.finders
                    to_update.roles = update.roles
                    to_update.champion_types = update.champion_types
                    to_update.video_type = update.video_type
                    to_update.locales = update.locales
            else:
                news.append(to_update)

        if news:
            session.bulk_save_objects(list(set(news)))
        can_commit = True

    if can_commit:
        session.commit()


class Manager:
    def __init__(self):
        self.to_add = []
        self.to_update = []
        self.to_delete = []

    def put_into_add(self, item):
        self.to_add.append(item)

    def put_into_update(self, item):
        self.to_update.append(item)

    def put_into_delete(self, item):
        self.to_delete.append(item)

    def empty(self):
        return self.to_add == [] and self.to_update == [] and self.to_delete == []

    def clear(self):
        self.to_add = []
        self.to_update = []
        self.to_delete = []

    def __repr__(self):
        return '({}\n{}\n{})'.format(self.to_add, self.to_update, self.to_delete)


class UserManager(Manager):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'UserManager:\n{}\n'.format(super().__repr__())

    def process(self, session):
        can_commit = False

        # to add
        if self.to_add:
            # session.bulk_save_objects(self.to_add)
            bulk_save_objects_into_db(session, self.to_add, UserChampion)
            can_commit = True

        # to update
        if self.to_update:
            news = []
            for item in self.to_update:
                to_update = session.query(UserChampion).filter_by(id=item.id).first()
                if to_update is not None:
                    to_update.locale = item.locale
                    to_update.favorite_champ = item.favorite_champ
                else:
                    news.append(item)
            if news:
                session.bulk_save_objects(list(set(news)))
            can_commit = True

        # to delete
        if self.to_delete:
            for Id in self.to_delete:
                session.query(UserChampion).filter_by(id=Id).delete()
            can_commit = True

        if can_commit:
            session.commit()


class VideoManager(Manager):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'VideoManager:\n{}\n'.format(super().__repr__())

    def process(self, session):
        can_commit = False

        # to add
        if self.to_add:
            # session.bulk_save_objects(self.to_add)
            bulk_save_objects_into_db(session, self.to_add, VideoTag)
            can_commit = True

        # to update
        if self.to_update:
            news = []
            for item in self.to_update:
                to_update = session.query(VideoTag).filter_by(id=item.id).first()
                if to_update is not None:
                    to_update.champion_ids = item.champion_ids
                    to_update.finders = item.finders
                    to_update.roles = item.roles
                    to_update.champion_types = item.champion_types
                    to_update.video_type = item.video_type
                    to_update.locales = item.locales
                else:
                    news.append(item)
            if news:
                session.bulk_save_objects(list(set(news)))
            can_commit = True

        # to delete
        if self.to_delete:
            for Id in self.to_delete:
                session.query(VideoTag).filter_by(id=Id).delete()
            can_commit = True

        if can_commit:
            session.commit()


class EventManager(Manager):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'EventManager:\n{}\n'.format(super().__repr__())

    def process(self, session):
        # to add/update
        if self.to_add:

            can_commit = False

            existings = {existing: existing for existing in session.query(UserVideo).all()}
            updates, addings = {}, {}

            for new in self.to_add:
                if new in updates:
                    old = updates[new]
                    if old.percent < new.percent:
                        updates[old] = new
                else:
                    if new in existings:
                        old = existings[new]
                        if old.percent < new.percent:
                            updates[old] = new
                    else:
                        if new in addings:
                            old = addings[new]
                            if old.percent < new.percent:
                                updates[old] = new
                        else:
                            addings[new] = new

            # to add
            if addings:
                session.bulk_save_objects(list(addings.values()))
                can_commit = True

            # to update
            if updates:
                for update in updates.values():
                    to_update = session.query(UserVideo).filter_by(user_id=update.user_id, video_id=update.video_id).first()
                    to_update.percent = update.percent
                can_commit = True

            if can_commit:
                session.commit()


class DataManager:
    def __init__(self):
        self.users = UserManager()
        self.videos = VideoManager()
        self.events = EventManager()

    def process(self, session):
        self.users.process(session)
        self.videos.process(session)
        self.events.process(session)

    def empty(self):
        return self.users.empty() and self.videos.empty() and self.events.empty()

    def clear(self):
        self.users.clear()
        self.videos.clear()
        self.events.clear()

    def __repr__(self):
        return '===================== DataManager:\n {} {} {} =================='\
            .format(self.users, self.videos, self.events)
