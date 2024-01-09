"""
@Description：串口管理
@Author：mysondrink@163.com
@Time：2024/1/9 10:31
"""
from PySide2.QtCore import Signal
from controller.AbstractThread import AbstractThread
import time
# from func.infoPage import infoMessage

TIME_TO_SLEEP = 2
TRYLOCK_TIME = -1
FAILED_CODE = 404
SUCCEED_CODE = 202


class CheckSerialThread(AbstractThread):
    update_json = Signal(dict)

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
        进行串口的检测
        Returns:
            None
        """
        # qmutex.tryLock(trylock_time)
        try:
            info_msg = "串口检测中。。。"
            code_msg = SUCCEED_CODE
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            time.sleep(TIME_TO_SLEEP)
            info_msg = "连接串口成功！"
            code_msg = SUCCEED_CODE
            status_msg = self.currentThread()
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
            # qmutex.unlock()
        except Exception as e:
            self.sendException()
            info_msg = "serial error！"
            code_msg = FAILED_CODE
            status_msg = 1
            self.update_json.emit(dict(info=info_msg, code=code_msg, status=status_msg))
