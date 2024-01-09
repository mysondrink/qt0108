"""
@Description：加载界面
@Author：mysondrink@163.com
@Time：2024/1/9 9:56
"""

from controller.AbstractWidget import AbstractWidget
from controller.BlinkController import CheckBlinkThread
from controller.DBController import CheckDataBaseThread
from controller.CameraController import CheckCameraThread
from controller.SerialController import CheckSerialThread
import time
import util.frozen as frozen
from view.gui.loading import *

FLAG_NUM = 0
FAILED_CODE = 404
SUCCEED_CODE = 202


class LoadPage(Ui_Form, AbstractWidget):
    update_json = Signal(dict)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()
        self.list_widget = None
        self.cur_page = None
        self.flag_num = FLAG_NUM

    """
    @detail 设置界面相关信息
    """

    def InitUI(self):
        self.statusShowTime()
        self.ui.title_label.setText('  荧光分析仪')
        self.ui.retry_icon_label.hide()
        self.ui.btnRetry.hide()
        # self.ui.textEdit.setEnabled(False)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.NoFocus)

        screen = QDesktopWidget().screenGeometry()
        self.move(screen.left(), screen.top())
        self.showMaximized()

        # 创建定时器
        self.blink_timer = QTimer()
        self.blink_flag = True
        self.blink_timer.timeout.connect(self.blinkIcon)
        self.myBlinkThread = CheckBlinkThread()
        self.myBlinkThread.update_json.connect(self.blinkAssess)
        self.thread_timer = QTimer()
        self.thread_timer.timeout.connect(self.myBlinkThread.start)
        thread_delay_time = 2000
        self.thread_timer.start(thread_delay_time)

        self.startThread()

    """
    @detail 检测设备wifi连接情况，同时设置图标进行显示
    """

    def blinkAssess(self, msg):
        self.blink_timer.stop()
        code = msg['code']
        print(code)
        if code == 202:
            self.ui.wifi_label.show()
            wifi_icon_path = frozen.app_path() + r"/res/icon/icon-wi-fi.png"
            pixImg = self.mySetIconSize(wifi_icon_path)
            self.ui.wifi_label.setPixmap(pixImg)
            self.ui.wifi_label.setAlignment(Qt.AlignCenter)
        elif code == 404:
            wifi_icon_path = frozen.app_path() + r"/res/icon/icon-wi-fi-disconnected.png"
            pixImg = self.mySetIconSize(wifi_icon_path)
            self.ui.wifi_label.setPixmap(pixImg)
            self.ui.wifi_label.setAlignment(Qt.AlignCenter)
            # 设置定时器延迟时间，单位为毫秒
            # 延迟0.5秒跳转
            delay_time = 500
            self.blink_timer.start(delay_time)

    """
    @detail 图标闪烁提示
    """

    def blinkIcon(self):
        if self.blink_flag:
            self.blink_flag = False
            self.ui.wifi_label.hide()
        else:
            self.blink_flag = True
            self.ui.wifi_label.show()

    """
    @detail 设置按钮图标比例
    """

    def mySetIconSize(self, path):
        img = QImage(path)  # 创建图片实例
        mgnWidth = 30
        mgnHeight = 30  # 缩放宽高尺寸
        size = QSize(mgnWidth, mgnHeight)
        pixImg = QPixmap.fromImage(
            img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        return pixImg

    """
    @detail 开启相机、数据库、串口的线程检测
    """

    def startThread(self):
        self.thread_list = [CheckSerialThread(), CheckDataBaseThread(), CheckCameraThread()]
        self.thread_id = []

        for num in range(len(self.thread_list)):
            self.thread_id.append(self.thread_list[num])
            self.thread_list[num].update_json.connect(self.setInfoLabel)
            self.thread_list[num].finished.connect(self.thread_list[num].deleteLater)
            self.thread_list[num].start()

    """
    @detail 开启相机、数据库、串口的线程检测
    @param msg: 发送的信号
    """

    # @Slot()
    def setInfoLabel(self, msg):
        try:
            info_msg, code_msg, status_msg = msg['info'], msg['code'], msg['status']
            if status_msg in self.thread_id:
                self.thread_id.remove(status_msg)
            text = self.ui.textEdit.toPlainText()
            self.ui.textEdit.append(info_msg)
            lines = text.split('\n')
            if code_msg == FAILED_CODE:
                self.retryThread()
                self.flag_num = -1
            elif len(lines) == 5 and self.flag_num == 0:
                # 创建定时器
                self.change_timer = QTimer()
                self.flag_num == -1
                self.change_timer.timeout.connect(self.showPage)
                # 设置定时器延迟时间，单位为毫秒
                # 延迟2秒跳转
                delay_time = 2000
                self.change_timer.start(delay_time)
        except Exception as e:
            self.sendException()
            print(e)
            # m_title = ""
            # m_info = "系统错误！"
            # infoMessage(m_info, m_title, 300)

    """
    @detail 设置主界面中子界面的显示位置，同时显示登录界面
    """

    def showPage(self):
        print(self.flag_num)
        return
        self.list_widget = []
        if self.flag_num == 0:
            self.change_timer.stop()
            self._s = QStackedLayout()
            self._h = QHBoxLayout()
            # self.cur_page = perinfoPage()
            self.cur_page = loginPage()
            self.cur_page.next_page.connect(self.changePage)
            self.cur_page.update_json.connect(self.getJsonData)
            self.cur_page.update_log.connect(self.log_thread.getLogMsg)

            self.cur_page.setFocus()
            self._s.addWidget(self.cur_page)
            self._h.addLayout(self._s)
            self.ui.centerframe.setLayout(self._h)

            self._s.setSpacing(0)
            self._h.setSpacing(0)

            self._s.setContentsMargins(0, 0, 0, 0)
            self._h.setContentsMargins(0, 0, 0, 0)

            self.flag_num = -1
            self.list_widget.append(self._s.currentWidget())
            # 尾指针
            self.q_ptr = self._s.currentIndex()
            # 头指针
            self.p_ptr = self._s.currentIndex()

    """
    @detail 进行页面的跳转
    @param msg: 发送的信号，获取子页面返回的信号，信号是跳转页面
    """

    def changePage(self, msg):
        try:
            # 设置栈为2
            num = len(self.list_widget)
            if msg == 'history':
                temp = self.list_widget[1]
                self._s.removeWidget(self._s.currentWidget())
                self.list_widget.remove(self.list_widget[1])
                self.p_ptr -= 1
                temp.close()
                return
            # if num > 1:
            #     self._s.removeWidget(self.list_widget[0])
            #     self.list_widget.remove(self.list_widget[0])
            #     self.p_ptr += 1
            #     time.sleep(0.5)
            self.cur_page = globals()[msg]()
            self.cur_page.next_page.connect(self.changePage)
            self.cur_page.update_json.connect(self.getJsonData)
            self.cur_page.update_log.connect(self.log_thread.getLogMsg)
            self.cur_page.setFocus()

            # 防止页面重复
            # num = len(self.list_widget)
            # if self._s.indexOf(self.cur_page) > -1:
            #     self._s.removeWidget(self.list_widget[1])
            #     self.list_widget.remove(self.list_widget[1])
            #     self.q_ptr -= 1
            #     time.sleep(0.5)
            #     return
            if num > 1:
                temp = self.list_widget[0]
                self._s.removeWidget(self.list_widget[0])
                self.list_widget.remove(self.list_widget[0])
                self.p_ptr += 1
                temp.close()
                time.sleep(0.5)

            self._s.addWidget(self.cur_page)
            self._s.setCurrentIndex(self._s.count() - 1)
            self.list_widget.append(self._s.currentWidget())
            self.q_ptr += 1
            # self.ui.centerframe.setLayout(self._s)
            # self.cur_page.show()
        except Exception as e:
            self.sendException()
            print(e)
            # m_title = ""
            # m_info = "系统错误！"
            # infoMessage(m_info, m_title, 300)

    """
    @detail 设置时间显示，间隔为1秒
    """

    def statusShowTime(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.showCurrentTime)

        self.timer.start(1000)

    """
    @detail 设置显示时间格式
    """

    def showCurrentTime(self):
        cur_time = QDateTime.currentDateTime()
        time_display = cur_time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.ui.time_label.setText(time_display)

    """
    @detail 显示重试标签、按钮
    """

    def retryThread(self):
        self.ui.retry_icon_label.show()
        self.ui.btnRetry.show()

    """
    @detail 获取子界面发送的信息,同时发送给其他子界面
    @detail 槽函数
    @param msg: 发送的信号，获取子页面返回的信号，信号是子界面的消息
    """

    def getJsonData(self, msg):
        self.update_json.connect(self.cur_page.getData)
        self.update_json.emit(msg)

    """
    @detail 槽函数，重试按钮，重新进行相机、数据库、串口的线程检测
    """

    @Slot()
    def on_btnRetry_clicked(self):
        self.ui.textEdit.clear()
        self.flag_num = FLAG_NUM
        self.ui.retry_icon_label.hide()
        self.ui.btnRetry.hide()
        # for num in range(len(self.thread_id)):
        #     stat = self.thread_id[num].isFinished()
        #     if self.thread_id[num].isFinished() is False:
        #         continue
        #     self.thread_id[num].deleteLater()
        self.thread_id.clear()
        self.startThread()

    """
    @detail 未使用
    @detail 槽函数，进度条设置
    """

    @Slot()
    def loadingError(self):
        error_stylesheet = "QProgressBar {\
                               border: 2px solid lightgray;\
                               border-radius: 5px;\
                               text-align: center;\
                               color: white;\
                           }\
                           QProgressBar::chunk {\
                               background-color: #ff0000;\
                               border-radius: 4px;\
                           }"
        self.ui.progressBar.setStyleSheet(error_stylesheet)
        self.ui.btnRetry.setVisible(True)
        self.ui.retry_icon_label.setVisible(True)