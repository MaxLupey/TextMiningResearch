import json
import sqlite3
import threading


class SQLiteProvider:
    def __init__(self, db_file):
        self.db_file = db_file
        self.local_storage = threading.local()
        self.check_and_create_tables()

    def get_conn(self):
        if not hasattr(self.local_storage, 'connection'):
            self.local_storage.connection = sqlite3.connect(self.db_file)
        return self.local_storage.connection

    def close_connection(self):
        if hasattr(self.local_storage, 'connection'):
            self.local_storage.connection.close()
            del self.local_storage.connection

    def check_and_create_tables(self):
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                sub TEXT PRIMARY KEY,
                uuid TEXT,
                token TEXT,
                auth_info TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                name TEXT,
                uuid TEXT PRIMARY KEY,
                shared BOOLEAN,
                user_uuid TEXT,
                unique_labels TEXT,
                FOREIGN KEY(user_uuid) REFERENCES users(uuid)
            )
        """)

        conn.commit()

    def add_user(self, uuid, token, google_payload):
        sub = google_payload['sub']
        user = (sub, uuid, token, json.dumps(google_payload))
        sql = ''' INSERT INTO users(sub,uuid,token,auth_info)
                  VALUES(?,?,?,?) '''
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        return {'sub': sub, 'uuid': uuid, 'token': token, 'auth_info': google_payload, 'models': []}

    def update_user(self, token, google_payload):
        sub = google_payload['sub']
        user = (token, json.dumps(google_payload), sub)
        sql = ''' UPDATE users
                  SET token = ?, auth_info = ?
                  WHERE sub = ?'''
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        return self.get_user_by_sub(sub)

    def remove_user(self, uuid):
        sub = self.get_user_by_uuid(uuid)['sub']
        sql = ''' DELETE FROM users WHERE sub = ? '''
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(sql, (sub,))
        conn.commit()
        return None

    def get_user_by_sub(self, sub):
        sql = ''' SELECT * FROM users WHERE sub = ? '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (sub,))
        user = cur.fetchone()
        cur = self.get_conn().cursor()
        uuid = user[1] if user is not None else None
        cur.execute(''' SELECT * FROM models WHERE user_uuid = ? ''', (uuid,))
        models = cur.fetchall()
        if user is not None:
            return {'sub': user[0], 'uuid': user[1], 'token': user[2], 'auth_info': user[3], 'models': models}
        return None

    def get_user_by_uuid(self, uuid):
        sql = ''' SELECT * FROM users WHERE uuid = ? '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (uuid,))
        user = cur.fetchone()
        # get models
        cur = self.get_conn().cursor()
        cur.execute(''' SELECT * FROM models WHERE user_uuid = ? ''', (uuid,))
        models = cur.fetchall()
        if user is not None:
            auth_info = json.loads(user[3])  # now it should not raise JSONDecodeError
            return {'sub': user[0], 'uuid': user[1], 'token': user[2], 'auth_info': auth_info, 'models': models}
        return None

    def add_model(self, uuid, model, name=None, shared=False):
        if name is None:
            name = model

        name = self.if_identify(name, shared, uuid, model)
        model = (name, model, shared, uuid)
        sql = ''' INSERT INTO models(name,uuid,shared,user_uuid)
                  VALUES(?,?,?,?) '''
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(sql, model)
        conn.commit()
        return {'name': name, 'uuid': model, 'shared': shared}

    def remove_model(self, uuid_user, uuid_model):
        sql = ''' DELETE FROM models WHERE uuid = ? AND user_uuid = ? '''
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute(sql, (uuid_model, uuid_user))
        conn.commit()
        return None

    def get_models(self, uuid, use_shared=False):
        cur = self.get_conn().cursor()
        if use_shared:
            sql = ''' SELECT * FROM models WHERE user_uuid = ? OR shared = 1'''
            cur.execute(sql, (uuid,))
        else:
            sql = ''' SELECT * FROM models WHERE user_uuid = ? '''
            cur.execute(sql, (uuid,))
        models = cur.fetchall()
        return [{'name': model[0], 'uuid': model[1], 'shared': model[2]} for model in models]

    def get_model_by_uuid(self, uuid_user, uuid_model):
        sql = ''' SELECT * FROM models WHERE uuid = ? AND user_uuid = ? '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (uuid_model, uuid_user))
        model = cur.fetchone()
        if model is not None:
            print(model)
            return {'name': model[0], 'uuid': model[1], 'shared': True if model[2] == 1 else False}
        return None

    def get_model_by_name(self, uuid_user, name):
        sql = ''' SELECT * FROM models WHERE name = ? AND user_uuid = ? '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (name, uuid_user))
        model = cur.fetchone()
        if model is not None:
            return {'name': model[0], 'uuid': model[1], 'shared': True if model[2] == 1 else False}
        return None

    def model_is_shared(self, sub, uuid):
        sql = ''' SELECT shared FROM models WHERE uuid = ? AND user_uuid = (SELECT uuid FROM users WHERE sub = ?) '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (uuid, sub))
        return cur.fetchone()[0] == 1

    def edit_model(self, uuid_user, uuid_model, name, shared):
        name = self.if_identify(name, shared, uuid_user, uuid_model)
        conn = self.get_conn()
        cur = conn.cursor()
        if name is not None and shared is not None:
            sql = f''' UPDATE models
                  SET name = ?, shared = ?
                  WHERE uuid = ? AND user_uuid = ?'''
            cur.execute(sql, (name, shared, uuid_model, uuid_user))
        elif name is not None:
            sql = f''' UPDATE models
                  SET name = ?
                  WHERE uuid = ? AND user_uuid = ?'''
            cur.execute(sql, (name, uuid_model, uuid_user))
        elif shared is not None:
            sql = f''' UPDATE models
                  SET shared = ?
                  WHERE uuid = ? AND user_uuid = ?'''
            cur.execute(sql, (shared, uuid_model, uuid_user))
        else:
            return None
        conn.commit()
        return self.get_model_by_uuid(uuid_user, uuid_model)

    def if_identify(self, name, shared, uuid_user, uuid_model):
        sql_check_uuid = ''' SELECT * FROM models WHERE uuid = ? AND uuid != ?'''
        cur = self.get_conn().cursor()
        cur.execute(sql_check_uuid, (name, uuid_model))
        if cur.fetchone() is not None:
            return uuid_model

        if shared:
            sql = ''' SELECT * FROM models WHERE name = ? AND shared = ? AND user_uuid != ? '''
        else:
            sql = ''' SELECT * FROM models WHERE name = ? AND shared = ? AND user_uuid = ? '''
        cur = self.get_conn().cursor()
        cur.execute(sql, (name, shared, uuid_user))
        return uuid_model if cur.fetchone() is not None else name
