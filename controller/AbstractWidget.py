"""
@Description：子界面抽象类实现
@Author：mysondrink@163.com
@Time：2024/1/8 16:36
"""
import sys
import traceback

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from controller.LogController import LogThread

class AbstractWidget(QWidget):
    update_log = Signal(str)

    def __init__(self) -> object:
        """
        构造函数，初始化日志类
        Returns:
            object
        """
        super().__init__()
        self.logThread = LogThread()
        self.logThread.start()
        self.update_log.connect(self.logThread.getLogMsg)
        sys.excepthook = self.HandleException

    def HandleException(self, excType, excValue, tb) -> None:
        """
        捕获和输出异常类
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
        发送异常信息
        Returns:
            None
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)
