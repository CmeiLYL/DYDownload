#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3
import json


class DataBase(object):
    def __init__(self):
        import os
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 从apiproxy/douyin目录回到项目根目录，然后进入settings目录
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        db_path = os.path.join(project_root, 'settings', 'data.db')
        
        # 确保settings目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_user_post_table()
        self.create_user_like_table()
        self.create_mix_table()
        self.create_music_table()

    def create_user_post_table(self):
        sql = """CREATE TABLE if not exists t_user_post (
                        id integer primary key autoincrement,
                        sec_uid varchar(200),
                        aweme_id integer unique, 
                        rawdata json
                    );"""

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            pass

    def get_user_post(self, sec_uid: str, aweme_id: int):
        sql = """select id, sec_uid, aweme_id, rawdata from t_user_post where sec_uid=? and aweme_id=?;"""

        try:
            self.cursor.execute(sql, (sec_uid, aweme_id))
            self.conn.commit()
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            pass

    def insert_user_post(self, sec_uid: str, aweme_id: int, data: dict):
        insertsql = """insert into t_user_post (sec_uid, aweme_id, rawdata) values(?,?,?);"""

        try:
            self.cursor.execute(insertsql, (sec_uid, aweme_id, json.dumps(data)))
            self.conn.commit()
        except Exception as e:
            pass

    def create_user_like_table(self):
        sql = """CREATE TABLE if not exists t_user_like (
                        id integer primary key autoincrement,
                        sec_uid varchar(200),
                        aweme_id integer unique,
                        rawdata json
                    );"""

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            pass

    def get_user_like(self, sec_uid: str, aweme_id: int):
        sql = """select id, sec_uid, aweme_id, rawdata from t_user_like where sec_uid=? and aweme_id=?;"""

        try:
            self.cursor.execute(sql, (sec_uid, aweme_id))
            self.conn.commit()
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            pass

    def insert_user_like(self, sec_uid: str, aweme_id: int, data: dict):
        insertsql = """insert into t_user_like (sec_uid, aweme_id, rawdata) values(?,?,?);"""

        try:
            self.cursor.execute(insertsql, (sec_uid, aweme_id, json.dumps(data)))
            self.conn.commit()
        except Exception as e:
            pass

    def create_mix_table(self):
        sql = """CREATE TABLE if not exists t_mix (
                        id integer primary key autoincrement,
                        sec_uid varchar(200),
                        mix_id varchar(200),
                        aweme_id integer,
                        rawdata json
                    );"""

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            pass

    def get_mix(self, sec_uid: str, mix_id: str, aweme_id: int):
        sql = """select id, sec_uid, mix_id, aweme_id, rawdata from t_mix where sec_uid=? and  mix_id=? and aweme_id=?;"""

        try:
            self.cursor.execute(sql, (sec_uid, mix_id, aweme_id))
            self.conn.commit()
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            pass

    def insert_mix(self, sec_uid: str, mix_id: str, aweme_id: int, data: dict):
        insertsql = """insert into t_mix (sec_uid, mix_id, aweme_id, rawdata) values(?,?,?,?);"""

        try:
            self.cursor.execute(insertsql, (sec_uid, mix_id, aweme_id, json.dumps(data)))
            self.conn.commit()
        except Exception as e:
            pass

    def create_music_table(self):
        sql = """CREATE TABLE if not exists t_music (
                        id integer primary key autoincrement,
                        music_id varchar(200),
                        aweme_id integer unique,
                        rawdata json
                    );"""

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            pass

    def get_music(self, music_id: str, aweme_id: int):
        sql = """select id, music_id, aweme_id, rawdata from t_music where music_id=? and aweme_id=?;"""

        try:
            self.cursor.execute(sql, (music_id, aweme_id))
            self.conn.commit()
            res = self.cursor.fetchone()
            return res
        except Exception as e:
            pass

    def insert_music(self, music_id: str, aweme_id: int, data: dict):
        insertsql = """insert into t_music (music_id, aweme_id, rawdata) values(?,?,?);"""

        try:
            self.cursor.execute(insertsql, (music_id, aweme_id, json.dumps(data)))
            self.conn.commit()
        except Exception as e:
            pass


if __name__ == '__main__':
    pass
