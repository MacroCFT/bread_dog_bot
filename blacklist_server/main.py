import sqlite3
import traceback

from json import dumps
from flask import Flask, request

tokens = ["test"]


class sql:
    def __init__(self, path):
        self.cur = None
        self.conn = None
        self.path = path

    def execute_sql(self, s: str):
        try:
            self.conn = sqlite3.connect(self.path)
            self.cur = self.conn.cursor()
            self.cur.execute(s)
            sql_return_result = self.cur.fetchall()
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return True, sql_return_result
        except sqlite3.OperationalError as e:
            traceback.print_exc()
            return False, f"数据库处理时出错:{e}"

    def detect(self, token, qq):
        if token in tokens:
            s, r = self.execute_sql(f"select * from black_list")
            if s:
                return True, r
            else:
                return False, r
        else:
            return False, "token不正确"

    def add(self, token, qq, group, reason):
        if token in tokens:
            print(qq)
            s, r = self.execute_sql(f"INSERT INTO black_list VALUES('{qq}','{group}','{reason}')")
            if s:
                return True, "数据加入成功"
            else:
                return False, r
        else:
            return False, "token不正确"

    def delete(self, token, qq):
        if token in tokens:
            print(qq)
            s, r = self.execute_sql(f"delete from black_list where qq = '{qq}'")
            if s:
                return True, "数据删除成功"
            else:
                return False, r
        else:
            return False, "token不正确"


bl_sql = sql("black_list.db")
bl = Flask(__name__)


@bl.route("/blacklist/", methods=["GET"])
def blacklist():
    try:
        s, r = bl_sql.detect(request.args.get("token"), request.args.get("qq"))
        if s:
            print(r)
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc()
        return dumps({"msg": e}), 403


@bl.route("/blacklist/add/", methods=["GET"])
def add_blacklist():
    try:
        s, r = bl_sql.add(request.args.get("token"), request.args.get("QQ"), request.args.get("groupID"), request.args.get("reason"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc()
        return dumps({"msg": e}), 403


@bl.route("/blacklist/delete/", methods=["GET"])
def del_blacklist():
    try:
        s, r = bl_sql.delete(request.args.get("token"), request.args.get("QQ"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc()
        return dumps({"msg": e}), 403


if __name__ == "__main__":
    bl.run(host="0.0.0.0", port=5432)
else:
    raise ImportError("此文件不可被引入")
