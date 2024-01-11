"""
@Description：菜单界面显示
@Author：mysondrink@163.com
@Time：2024/1/11 10:18
"""
import util.frozen as frozen
import sys
import traceback
# from func.infoPage import infoMessage
from view.gui.home import *
# from inf.probeThread import MyProbe
from view.AbstractPage import AbstractPage


class HomePage(Ui_Form, AbstractPage):
    next_page = Signal(str)
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
    """
    @detail 设置界面相关信息
    """
    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.startProbeMem()
        self.setBtnIcon()

    """
    @detail 设置按钮图标
    """
    def setBtnIcon(self):
        reagent_icon_path = frozen.app_path() + r"/res/icon/reagent.png"
        pixImg = self.mySetIconSize(reagent_icon_path)
        self.ui.reagent_icon_label.setPixmap(pixImg)
        self.ui.reagent_icon_label.setAlignment(Qt.AlignCenter)

        history_icon_path = frozen.app_path() + r"/res/icon/history.png"
        pixImg = self.mySetIconSize(history_icon_path)
        self.ui.history_icon_label.setPixmap(pixImg)
        self.ui.history_icon_label.setAlignment(Qt.AlignCenter)

        reagent_set_icon_path = frozen.app_path() + r"/res/icon/set.png"
        pixImg = self.mySetIconSize(reagent_set_icon_path)
        self.ui.reagent_set_icon_label.setPixmap(pixImg)
        self.ui.reagent_set_icon_label.setAlignment(Qt.AlignCenter)

        sys_icon_path = frozen.app_path() + r"/res/icon/sys.png"
        pixImg = self.mySetIconSize(sys_icon_path)
        self.ui.sys_icon_label.setPixmap(pixImg)
        self.ui.sys_icon_label.setAlignment(Qt.AlignCenter)

        power_icon_path = frozen.app_path() + r"/res/icon/power.png"
        self.ui.btnPower.setIconSize(QSize(32, 32))
        self.ui.btnPower.setIcon(QIcon(power_icon_path))

    """
    @detail 设置按钮图标比例
    @param path: 图片路径
    """
    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 50
        mgnHeight = 50  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    """
    @detail 开始存储探测
    """
    def startProbeMem(self):
        self.myprobe = MyProbe()
        self.myprobe.update_progress.connect(self.memWarning)
        self.myprobe.start()

    """
    @detail 存储满后警告
    """
    def memWarning(self, msg):
        print(msg)
        if msg == 404:
            m_title = "警告"
            m_info = "存储已经占满，请清理图片！"
            infoMessage(m_info, m_title)
            self.myprobe.deleteLater()
            return
        elif msg == 202:
            page_msg = 'TestPage'
            self.next_page.emit(page_msg)
            self.myprobe.deleteLater()

    """
    @detail 电源按钮操作，跳转到电源界面
    @detail 槽函数
    """
    @Slot()
    def on_btnPower_clicked(self):
        page_msg = 'PowerPage'
        self.next_page.emit(page_msg)

    """
    @detail 荧光检疫按钮操作，跳转到荧光检疫界面
    @detail 槽函数
    """
    @Slot()
    def on_btnData_clicked(self):
        self.startProbeMem()
        # page_msg = 'testPage'
        # self.next_page.emit(page_msg)

    """
    @detail 历史记录按钮操作，跳转到历史记录界面
    @detail 槽函数
    """
    @Slot()
    def on_btnHistory_clicked(self):
        page_msg = 'HistoryPage'
        self.next_page.emit(page_msg)

    """
    @detail 检疫设置按钮操作，跳转到检疫设置界面
    @detail 槽函数
    """
    @Slot()
    def on_btnSet_clicked(self):
        page_msg = 'EditPage'
        self.next_page.emit(page_msg)

    """
    @detail 系统设置按钮操作，跳转到系统设置界面
    @detail 槽函数
    """
    @Slot()
    def on_btnPara_clicked(self):
        page_msg = 'SysPage'
        self.next_page.emit(page_msg)