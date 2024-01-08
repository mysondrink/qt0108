"""
@Description：
@Author：mysondrink@163.com\n
@Time：${DATE} ${TIME}\n
"""
import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


def main() -> None:
    """
    主程序入口
    Returns:
        null
    """
    app = QApplication()
    w = QWidget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

