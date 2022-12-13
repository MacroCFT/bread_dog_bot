from json import dumps, loads, JSONDecodeError, dump
from os import mkdir
from os.path import isdir
from sqlite3 import connect, OperationalError
from sys import stderr
from time import strftime
from traceback import print_exc

from flask import Flask, request

if not isdir("logs"):
    mkdir('logs')
log = open(fr'./logs/log-{strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w')


def write_log(l: str):
    log.write(f'''[{strftime("%x %X")}] {l}\n''')
    log.flush()


write_log("开始导入配置文件...")
try:
    with open("config.json") as w:
        cfg = loads(w.read())
        host = cfg["host"]
        port = cfg["port"]
        tokens = cfg["token"]
except JSONDecodeError as e:
    print_exc(file=log)
    print_exc()
    write_log(f"配置文件不符合JSON语法！\n{e}")
except ValueError as e:
    print_exc(file=log)
    print_exc()
    write_log(f"配置文件异常！\n{e}")
except FileNotFoundError as e:
    print_exc(file=log)
    write_log(f"配置文件不存在！尝试自动创建...\n{e}")
    print("配置文件不存在！尝试自动创建...")
    with open("config.json", "w") as e:
        dump(
            {
                "host": "0.0.0.0",
                "port": 5432,
                "token": {
                    "BDT_Default": [
                        "list",
                        "add",
                        "del"
                    ]
                }
            },
            e,
            indent=4
        )
        host = "0.0.0.0"
        port = 5432
        tokens = {
                    "BDT_Default": [
                        "list",
                        "add",
                        "del"
                    ]
                }
except PermissionError as e:
    print_exc(file=log)
    print_exc()
    write_log(f"无权读取配置文件！\n{e}")


class sql:
    def __init__(self, path):
        self.cur = None
        self.conn = None
        self.path = path
        s, r = self.execute_sql("SELECT name FROM sqlite_master WHERE type='table' AND name='black_list'")
        if s and (not r):
            print("数据库表不存在，自动创建...")
            s, r = self.execute_sql('CREATE TABLE IF NOT EXISTS black_list (qq TEXT,name TEXT,reason TEXT)')

    def execute_sql(self, s: str):
        try:
            self.conn = connect(self.path)
            self.cur = self.conn.cursor()
            self.cur.execute(s)
            sql_return_result = self.cur.fetchall()
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            write_log(f"数据库处理结果:{sql_return_result}")
            return True, sql_return_result
        except OperationalError as e:
            print_exc()
            write_log(f"数据库处理出错:{e}")
            return False, f"数据库处理时出错:{e}"

    def detect(self, token, qq):
        write_log(f"请求云黑用户的信息...token={token}")
        if token in tokens:
            if "list" in tokens[token]:
                s, r = self.execute_sql(f"select * from black_list")
                if s:
                    write_log(f"用户信息 {r} 请求成功...")
                    if qq:
                        write_log("有QQ返回内容，分离中...")
                        wl = []
                        for x in r:
                            print(x)
                            print(qq)
                            if x[0] in qq:
                                wl.append(x)
                        write_log(f"分离出的用户信息:{wl}")
                        return True, wl
                    else:
                        write_log("没有QQ返回内容，自动全选...")
                        return True, r
                else:
                    return False, r
            else:
                write_log(f"token:'{token}'没有查询云黑的权限")
                return False, "token没有查询云黑的权限"
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"

    def find(self, qq):
        write_log(f"请求云黑用户的信息...qq={qq}")
        s, r = self.execute_sql(f"select * from black_list where qq = '{qq}'")
        if s:
            return True, r
        else:
            return False, r

    def add(self, token, qq, group, reason):
        write_log(f"添加云黑...token={token}, qq={qq}, group={group}, reason={reason}")
        if token in tokens.keys():
            if "add" in tokens[token]:
                s, r = self.find(qq)
                if s:
                    if not r:
                        print("没有匹配的用户")
                        write_log(f"未匹配用户{qq}，添加云黑...")
                        s, r = self.execute_sql(f"INSERT INTO black_list VALUES('{qq}','{group}','{reason}')")
                        if s:
                            write_log(f"云黑用户 qq={qq}, group={group}, reason={reason} 已被添加...")
                            return True, "数据加入成功"
                        else:
                            return False, r
                    else:
                        print(r)
                        return False, f"该用户已存在于云黑数据库！\nQQ:{r[0][0]}\n加入的群:{r[0][1]}\n理由:{r[0][2]}"
                else:
                    return False, r
            else:
                write_log(f"token:'{token}'没有添加云黑的权限")
                return False, "token没有添加云黑的权限"
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"

    def delete(self, token, qq):
        write_log(f"删除云黑...token={token}, qq={qq}")
        if token in tokens:
            if "del" in tokens[token]:
                print(f"接收到删除云黑请求：QQ:{qq}")
                s, r = self.find(qq)
                if s:
                    if r:
                        print(f"发现云黑用户:{r}")
                        s, r = self.execute_sql(f"delete from black_list where qq = '{qq}'")
                        if s:
                            write_log(f"云黑用户{qq}已从云黑中移除")
                            return True, "数据删除成功"
                        else:
                            return False, r
                    else:
                        return False, f"云黑数据中没有{qq}！"
                else:
                    return False, r
            else:
                write_log(f"token:'{token}'没有删除云黑的权限")
                return False, "token没有删除云黑的权限"
        else:
            write_log(f"token:'{token}'不在可用的tokens列表内")
            return False, "token不正确"


bl_sql = sql("black_list.db")
bl = Flask(__name__)


@bl.route("/blacklist/", methods=["GET"])
def blacklist():
    try:
        write_log(f"接收到GET请求:{request.host_url}")
        write_log(f"请求者IP为:{request.remote_addr}")
        write_log(f"请求获取云黑列表...")
        print("接收到云黑数据请求...")
        s, r = bl_sql.detect(request.args.get("token"), request.args.getlist("qq"))
        if s:
            write_log(f"获取的云黑用户元数据:{r}")
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        print_exc(file=log)
        print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


@bl.route("/blacklist/add/", methods=["GET"])
def add_blacklist():
    try:
        write_log(f"接收到GET请求:{request.host_url}")
        write_log(f"请求者IP为:{request.remote_addr}")
        write_log(
            f'请求添加云黑请求：QQ:{request.args.get("QQ")}, 群组:{request.args.get("groupID")}，理由:{request.args.get("reason")}')
        print("接受到添加云黑请求：QQ:{0}, 群组:{1}，理由:{2}".format(request.args.get("QQ"), request.args.get("groupID"),
                                                                    request.args.get("reason")))
        s, r = bl_sql.add(request.args.get("token"), request.args.get("QQ"), request.args.get("groupID"),
                          request.args.get("reason"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        print_exc(file=log)
        print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


@bl.route("/blacklist/delete/", methods=["GET"])
def del_blacklist():
    try:
        write_log(f"接收到GET请求:{request.host_url}")
        write_log(f"请求者IP为:{request.remote_addr}")
        write_log(f"请求删除云黑:{request.args.get('QQ')}")
        print("接受到删除云黑请求：QQ:{0}".format(request.args.get("QQ")))
        s, r = bl_sql.delete(request.args.get("token"), request.args.get("QQ"))
        if s:
            return dumps({"data": r}), 200
        else:
            return dumps({"msg": r}), 403
    except Exception as e:
        print_exc(file=log)
        print_exc()
        log.flush()
        stderr.write("看起来出错了呢...要不提交一下issue?")
        return dumps({"msg": e}), 403


if __name__ == "__main__":
    print("启动项目...")
    write_log("云黑服务器启动...")
    bl.run(host=host, port=port)
else:
    raise ImportError("此文件不可被引入")
