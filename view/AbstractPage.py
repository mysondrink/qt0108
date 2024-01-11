"""
@Description：抽象page界面类
@Author：mysondrink@163.com
@Time：2024/1/11 11:17
"""
from view.AbstractWidget import AbstractWidget
from view.AbstractDialog import AbsctractDialog
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QImage, QPixmap

class ErrorDialog(AbsctractDialog):
    def __int__(self):
        super().__int__()

    def mouseDoubleClickEvent(self, msg):
        pass

class AbstractPage(AbstractWidget):
    def __init__(self):
        super().__init__()
        self.update_info.connect(self.showInfo)

    def HandleException(self, excType, excValue, tb) -> None:
        super().HandleException(excType, excValue, tb)
        dialog = ErrorDialog()
        dialog.setParent(self)
        # dialog.setAttribute(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        dialog.setInfo("系统错误")
        dialog.hideProgress()
        dialog.show()

    """
    @detail 设置按钮图标比例
    @param path: 图片路径
    """
    def mySetIconSize(self, path) -> QPixmap:
        """

        Args:
            path:

        Returns:
            pixImg: QPixmap
        """
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    def showInfo(self, msg):
        dialog = AbsctractDialog()
        dialog.setInfo(msg)
        dialog.setParent(self)
        dialog.hideProgress()
        dialog.show()