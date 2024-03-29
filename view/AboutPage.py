"""
@Description：设备信息界面显示
@Author：mysondrink@163.com
@Time：2024/1/11 11:04
"""
import util.frozen as frozen
# from func.infoPage import infoMessage
from view.gui.about import *
import os
import shutil
import sys
import traceback
from view.AbstractPage import AbstractPage

class AboutPage(Ui_Form, AbstractPage):
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

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnUpload.setIconSize(QSize(32, 32))
        self.ui.btnUpload.setIcon(QIcon(confirm_icon_path))

    """
    @detail u盘上传信息到软件
    @detail 默认上传文件为example.txt，上传内容为6个数字，每个数字各占一行
    """
    def uploadFromUSB(self):
        # 指定目标目录
        target_dir = '/media/xiao/'

        # 获取U盘设备路径
        try:
            filename = r"/media/xiao/" + os.listdir(target_dir)[0]
        except Exception as e:
            m_title = ""
            m_info = "U盘未插入或无法访问！"
            infoMessage(m_info, m_title, 240)
            return

            # 检查U盘是否已插入
        if os.path.exists(filename):
            # 在U盘根目录下查找指定文件
            file_path = os.path.join(filename, "example.txt")
            if os.path.exists(file_path):
                # 读取文件内容并打印到控制台
                with open(file_path, "r") as f:
                    # print(f.read())
                    m_title = ""
                    m_info = f.read()
                    infoMessage(m_info, m_title)
            else:
                # print("文件不存在")
                m_title = ""
                m_info = "文件不存在!"
                infoMessage(m_info, m_title, 300)
        else:
            # print("U盘未插入或无法访问")
            m_title = ""
            m_info = "U盘未插入或无法访问!"
            infoMessage(m_info, m_title, 240)

    """
    @detail 上传按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnUpload_clicked(self):
        m_title = ""
        m_info = "上传中..."
        infoMessage(m_info, m_title, 380)
        # 创建定时器
        self.change_timer = QTimer()
        self.change_timer.timeout.connect(self.uploadFromUSB())
        # 设置定时器延迟时间，单位为毫秒
        # 延迟2秒跳转
        delay_time = 2000
        self.change_timer.start(delay_time)

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'SysPage'
        self.next_page.emit(page_msg)

