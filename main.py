"""
@Description：主程序入口文件
@Author：mysondrink@163.com
@Time：2024/1/8 15:11
"""
import sys
from PySide2.QtWidgets import QApplication
from view.AbstractDialog import AbsctractDialog
from view.LoadPage import LoadPage

"""
@闪退多为信号与槽问题，注意检查信号与槽函数的连接
@少数情况为函数定义问题，函数缺少参数或参数错误
@定义成员变量时会报错，存在当再次访问即对成员变量赋值时，类方法无法调用正确的变量，问题无法解决
"""


def main() -> None:
    """
    主程序入口
    Returns:
        None
    """
    app = QApplication()
    w = LoadPage()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
