import threading
import os
from tornado.websocket import WebSocketHandler
from tornado import gen
from functools import partial
import tornado.web
import tornado.ioloop
import logging
#import tornadoredis
import redis
import json
from tornado.process import Subprocess
from tornado.iostream import StreamClosedError
import signal
import traceback
import psutil
from upm import pyupm_jhd1313m1 as lcd

"""
使用Tornado创建一个Websocket Server，与GUI通信
"""

data = list()
lock = threading.Lock()
user_set = set()

COMMAND_TYPE ="command"
KILL_TYPE = "kill"

logging.basicConfig(level=logging.INFO)

# 此处与开发板相关，是grove套件中的LCD，可以忽略
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

"""
监听redis，如果myo_hub写入对应的数据，就将数据发送到GUI
"""


def redis_listener():
    r = redis.Redis(host="127.0.0.1")
    ps=r.pubsub()
    ps.subscribe(["voice", "gesture", "adjust", "log"])
    t_io_loop = tornado.ioloop.IOLoop.instance()
    for message in ps.listen():
        for user in user_set:
            t_io_loop.add_callback(user.write_message,str(message['data'], encoding="utf-8"))


class ShowWebSocket(WebSocketHandler):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd_subprocess_dict = dict()

    def check_origin(self, origin):
        return True

    def open(self):
        """
        收到websocket连接请求
        :return:
        """
        try:
            username = self.get_argument("username")
        except tornado.web.MissingArgumentError:
            username = "default"

        user_set.add(self)

        print(user_set)
        myLcd.setColor(0, 255, 0)
        myLcd.setCursor(0,0)
        myLcd.write(username + " connected")

        self.write_message(json.dumps({"type": "voice", "data": "连接成功"}, ensure_ascii=False))

    @gen.coroutine
    def on_message(self, message_json):
        """
        收到信息
        :param message_json:
        :return:
        """
        try:
            message = json.loads(message_json)
            if message["type"] == COMMAND_TYPE:
                # 执行命令
                self.run_subprocess(message["name"], message["data"])
                self.write_message(json.dumps({"type": "log", "data": "run command success"}, ensure_ascii=False))
                myLcd.setColor(255, 0, 0)
                myLcd.setCursor(0,0)
                myLcd.write("run " + message["name"])
                
            elif message["type"] == KILL_TYPE:
                # 停止命令
                self.kill_subprocess(message["name"])
                myLcd.setColor(0, 255, 0)
                myLcd.setCursor(0, 0)
                myLcd.write("stop " + message["name"])
        except:
            self.write_message(json.dumps({"type": "log", "data": "command faied"}, ensure_ascii=False))
            myLcd.setColor(255, 0, 0)
            myLcd.setCursor(0, 0)
            myLcd.write(message["name"] + " failed")

            traceback.print_exc()
            return

    def on_close(self):
        logging.warning("someone closed")
        user_set.remove(self)
        myLcd.setColor(255, 0, 0)
        myLcd.setCursor(0, 0)
        myLcd.write("someone closed")

    @gen.coroutine
    def run_subprocess(self, name, cmd):
        """
        执行指定的名称，并将线程绑定到对应的名称
        :param name: 线程绑定的名称
        :param cmd:  要在bash运行的命令
        :return:
        """
        cmd_proc = Subprocess(cmd, shell=True, preexec_fn=os.setsid, stdout=Subprocess.STREAM)
        self.cmd_subprocess_dict[name] = cmd_proc
        # yield self.redirect_stream(cmd_proc.stdout)
        yield cmd_proc.stdout.read_until_close()
        raise gen.Return(None)

    @gen.coroutine
    def redirect_stream(self, stream):
        while True:
            try:
                data = yield stream.read_bytes(128, partial=True)
                logging.info(data)
            except StreamClosedError:
                break
            else:
                self.write_message({"type": "process_result", "data": data})
    
    @gen.coroutine
    def kill_subprocess(self, name):
        """
        收到杀死进程的命令，杀死对应name的进程
        :param name: 指定的名称
        :return:
        """
        try:
            p = psutil.Process(self.cmd_subprocess_dict[name].pid)
            child_pid = p.children(recursive=True)
            for pid in child_pid:
                os.kill(pid.pid, signal.SIGKILL)
            p.terminate()
            self.write_message({"type": "log", "data": "kill command success"})
        except KeyError as e:
            self.write_message({"type": "log", "data": "no command with this name"})
        except Exception as e:
            traceback.print_exc()
            self.write_message(json.dumps({"type":"log", "data":"kill command failed"}))
            return

    @classmethod
    def push_data(cls, type, msg):
        print("push data")
        print(cls.user_set)
        for key, user in cls.user_set.items():
            try:
                user.write_message(type + "+" + msg)
            except tornado.websocket.WebSocketClosedError:
                logging.error("Error sending message", exc_info=True)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ShowWebSocket)
        ]
        super(Application, self).__init__(handlers)


def main():
    threading.Thread(target=redis_listener).start() # 开启redis监听进程
    app = Application()
    # websocket监听2233端口
    app.listen("2233", address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
