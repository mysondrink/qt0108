"""
@Description：抽象page界面类
@Author：mysondrink@163.com
@Time：2024/1/11 11:17
"""
from view.AbstractWidget import AbstractWidget
from view.AbstractDialog import AbsctractDialog
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QImage, QPixmap


class ProcessDialog(AbsctractDialog):
    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, msg):
        pass


class AbstractPage(AbstractWidget):
    def __init__(self):
        """
        继承构造函数
        将日志处理连接到对话框
        """
        super().__init__()
        self.update_info.connect(self.showInfoDialog)
        # self.update_log.connect(self.showErrorDialog)

    def mySetIconSize(self, path) -> QPixmap:
        """
        设置按钮图标比例
        Args:
            path: 图片路径

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

    def showInfoDialog(self, msg) -> None:
        """
        显示弹窗
        Args:
            msg: 需要显示的弹窗信息

        Returns:
            None
        """
        dialog = AbsctractDialog()
        dialog.setInfo(msg)
        dialog.setParent(self)
        dialog.hideProgress()
        dialog.show()