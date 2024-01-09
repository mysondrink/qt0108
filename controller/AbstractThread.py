"""
@Description：抽象线程类
@Author：mysondrink@163.com
@Time：2024/1/9 10:09
"""
import sys
import traceback

from PySide2.QtCore import QThread, Signal
from controller.LogController import LogThread


class AbstractThread(QThread):
    update_log = Signal(str)

    def __init__(self) -> object:
        """
        构造函数，初始化日志类
        Returns:
            object
        """
        super().__init__()
        self.log_thread = LogThread()
        self.log_thread.start()
        self.update_log.connect(self.log_thread.getLogMsg)
        sys.excepthook = self.HandleException

    def HandleException(self, excType, excValue, tb) -> None:
        """
        自动捕获和输出异常类
        Args:
            excType: 异常类型
            excValue: 异常对象
            tb: 异常的trace back

        Returns:

        """
        sys.__excepthook__(excType, excValue, tb)
        err_msg = "".join(traceback.format_exception(excType, excValue, tb))
        self.update_log.emit(err_msg)
        # m_title = ""
        # m_info = "系统错误！"
        # infoMessage(m_info, m_title, 300)

    def sendException(self) -> None:
        """
        手动发送异常信息
        Returns:
            None
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print("sendexception")
        self.update_log.emit(err_msg)