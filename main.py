"""
@Description：主程序入口文件
@Author：mysondrink@163.com
@Time：2024/1/8 15:11
"""
import sys
from view.LoadPage import LoadPage
from PySide2.QtWidgets import QApplication


def main() -> None:
    """
    主程序入口
    Returns:
        null
    """
    app = QApplication()
    w = LoadPage()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

