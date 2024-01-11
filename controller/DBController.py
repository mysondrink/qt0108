"""
@Description：数据库管理类
@Author：mysondrink@163.com
@Time：2024/1/9 10:32
"""
# import pymysql
from PySide2.QtCore import Signal
from controller.AbstractThread import AbstractThread
import time

# from func.infoPage import infoMessage

TIME_TO_SLEEP = 2
TRYLOCK_TIME = -1
FAILED_CODE = 404
SUCCEED_CODE = 202


class CheckDataBaseThread(AbstractThread):
    def __init__(self) -> object:
        """
        构造函数
        初始化线程，调用父类方法进行日志记录
        Returns:
            object
        """
        super().__init__()

    def run(self) -> None:
        """
        线程运行函数
        进行数据库的检测
        Returns:
            None
        """
        try:
            info_msg = "数据库检测中。。。"
            code_msg = SUCCEED_CODE
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            connection = True
            if connection:
                # qmutex.tryLock(trylock_time)
                time.sleep(TIME_TO_SLEEP)
                info_msg = "连接数据库成功！"
                code_msg = SUCCEED_CODE
                status_msg = self.currentThread()
                # qmutex.unlock()
            else:
                # qmutex.tryLock(trylock_time)
                time.sleep(TIME_TO_SLEEP)
                info_msg = "连接数据库失败！"
                code_msg = FAILED_CODE
                status_msg = self.currentThread()
                # qmutex.unlock()
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
        except Exception as e:
            self.sendException()
            info_msg = "db error！"
            code_msg = FAILED_CODE
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
        finally:
            self.log_thread.deleteLater()
