import sqlite3
import traceback
import time

from sys import stderr
from json import dumps, loads
from flask import Flask, request


log = open(fr'./logs/log-{time.strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w')


def write_log(l: str):
    log.write(f'''[{time.strftime("%x %X")}] {l}\n''')
    log.flush()


write_log("开始导入配置文件...")
try:
    with open("config.json") as w:
        cfg = loads(w.read())
        host = cfg["host"]
        port = cfg["port"]
        tokens = cfg["token"]
except Exception as e:
    traceback.print_exc(file=log)
    traceback.print_exc()
    write_log(f"配置文件导入出错！{e}")


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
            write_log(f"数据库处理结果:{sql_return_result}")
            return True, sql_return_result
        except sqlite3.OperationalError as e:
            traceback.print_exc()
            write_log(f"数据库处理出错:{e}")
            return False, f"数据库处理时出错:{e}"

    def detect(self, token):
        write_log(f"请求云黑用户的信息...token={token}")
        if token in tokens:
            s, r = self.execute_sql(f"select * from black_list")
            if s:
                return True, r
            else:
                return False, r
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"

    def add(self, token, qq, group, reason):
        write_log(f"添加云黑...token={token}, qq={qq}, group={group}, reason={reason}")
        if token in tokens:
            s, r = self.execute_sql(f"INSERT INTO black_list VALUES('{qq}','{group}','{reason}')")
            if s:
                return True, "数据加入成功"
            else:
                return False, r
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"

    def delete(self, token, qq):
        write_log(f"删除云黑...token={token}, qq={qq}")
        if token in tokens:
            print(qq)
            s, r = self.execute_sql(f"delete from black_list where qq = '{qq}'")
            if s:
                return True, "数据删除成功"
            else:
                return False, r
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"


bl_sql = sql("black_list.db")
bl = Flask(__name__)


@bl.route("/blacklist/", methods=["GET"])
def blacklist():
    try:
        s, r = bl_sql.detect(request.args.get("token"))
        if s:
            print(f"Debug: 获取的数据:{r}")
            write_log(f"获取的云黑用户元数据:{r}")
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc(file=log)
        traceback.print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


@bl.route("/blacklist/add/", methods=["GET"])
def add_blacklist():
    try:
        print("接受到添加云黑请求：QQ:{0}, 群组:{1}，理由:{2}".format(request.args.get("QQ"), request.args.get("groupID"), request.args.get("reason")))
        s, r = bl_sql.add(request.args.get("token"), request.args.get("QQ"), request.args.get("groupID"), request.args.get("reason"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc(file=log)
        traceback.print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


@bl.route("/blacklist/delete/", methods=["GET"])
def del_blacklist():
    try:
        print("接受到删除云黑请求：QQ:{0}".format(request.args.get("QQ")))
        s, r = bl_sql.delete(request.args.get("token"), request.args.get("QQ"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        traceback.print_exc(file=log)
        traceback.print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


if __name__ == "__main__":
    print("启动项目...")
    write_log("云黑服务器启动...")
    bl.run(host=host, port=port)
else:
    raise ImportError("此文件不可被引入")
