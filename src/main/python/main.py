import os
import sys
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QTextEdit, QFileDialog, QAction
from PyQt5.QtCore import QSize, QSettings, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5 import uic

from ad_insertion_executor import ProcessingExecutor, InsertionExecutor


LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))


class AppThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)

    def run(self, cnt=0):
        return self.change_value.emit(cnt)


class BackgroundImgUI(object):
    def initUI(self):
        palette = QPalette()
        oImage = QPixmap(f"{LOCAL_DIR}/img/img_back.png")
        palette.setBrush(self.backgroundRole(), QBrush(oImage))
        self.setPalette(palette)


class MainUI(object):
    def initUI(self):
        self.resize(1376, 768)
        self.setWindowTitle(self.title)

        self.setWindowIcon(QtGui.QIcon(f"{LOCAL_DIR[-1]}/icons/Icon.ico"))


class QStartWindow(QWidget, MainUI, BackgroundImgUI):

    def __init__(self):
        super().__init__()
        self.title = "Smart Advertising"
        MainUI.initUI(self)
        BackgroundImgUI.initUI(self)
        self.initQStartWindow()

    def initQStartWindow(self):
        self.setWindowTitle(self.title)
        self.setObjectName('QStartWindow')
        layout = QVBoxLayout()
        label1 = QLabel('Smart Advertising', self)
        label1.setStyleSheet('width: 769px; height: 81px; left: 576px; top: 332px; font-weight: 500; font-size: 75px;'
                             'position: absolute; color: #1E6C93;'
                             'line-height: 118px; text-align: center;')

        label2 = QLabel('Your advertising in any movies', self)
        label2.setStyleSheet('width: 601px; height: 45px; left: 660px; top: 471px; font-size: 38px; color: #FFFFFF;')
        label3 = QLabel('... and do not miss this ad', self)
        label3.setStyleSheet('font-weight: normal; font-size: 28px;')
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        button = QPushButton('START')
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignHCenter)
        layout.setAlignment(label1, Qt.AlignHCenter)
        layout.setAlignment(label2, Qt.AlignHCenter)
        layout.setAlignment(label3, Qt.AlignHCenter)

        button.clicked.connect(self._nextWindow)
        self.dialogs = list()

        self.setLayout(layout)
        self.show()

    def _nextWindow(self):
        next_win = QAddContentWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()


class QAddContentWindow(QWidget, MainUI):
    def __init__(self):
        super().__init__()
        self.title = "Add Video content"
        self.initAddContentUI()

    def initAddContentUI(self):
        layout = QVBoxLayout()
        MainUI.initUI(self)
        button = QPushButton('Next ->')
        button.clicked.connect(self._nextWindow)
        layout.setAlignment(button, Qt.AlignBottom)
        self.dialogs = list()

        self.btn1 = QPushButton("Open Image")
        self.btn2 = QPushButton("Open Video")
        self.btn1.clicked.connect(self._getImage)
        self.btn2.clicked.connect(self._getVideo)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(button)

        self.label = QLabel("Hello")
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.show()

    def _getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'output', "Image files (*.jpg *.gif *.png)")
        imagePath = fname[0]
        print(imagePath)
        pixmap = QPixmap(imagePath)
        print(pixmap)
        self.label.setPixmap(QPixmap(pixmap))
        #self.resize(pixmap.width(), pixmap.height())

    def _getVideo(self):
        print("Video")

    def _nextWindow(self):
        next_win = QSettingsWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()


class QSettingsWindow(QWidget, MainUI):
    def __init__(self):
        self.title = "Settings"
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        super().__init__()
        MainUI.initUI(self)
        self.initQSettingsWindowtUI()
        self._settings_init_()
        self.get_all_settings()
        fileLabel = QLabel("Named:")
        textLabel = QLabel("Containing text:")
        directoryLabel = QLabel("In directory:")

    def _settings_init_(self):
        cfg = {
            'contour_threshold': 1.5,
            'conf_threshold': 0.6,
            'banner_size': 0.2,
            'background': False,
            'allowed_ram_size': 1000,
            'use_segmentation': True,
            'device': 'gpu'
        }

        for k, v in cfg.items():
            self.settings.setValue(k, v)

        self.settings.sync()

    def get_all_settings(self):
        cfg = {}
        for k in self.settings.allKeys():
            cfg.pop(k, self.settings.value(k))
        return cfg

    def initQSettingsWindowtUI(self):
        layout = QVBoxLayout()
        MainUI.initUI(self)
        button = QPushButton('Next ->')
        button.clicked.connect(self._nextWindow)
        layout.setAlignment(button, Qt.AlignBottom)
        self.dialogs = list()
        layout.addWidget(button)

        self.setLayout(layout)

    def _nextWindow(self):
        next_win = QMountingWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()



class QMountingWindow(QWidget, MainUI, BackgroundImgUI):
    def __init__(self):
        self.title = 'Mounting Video'
        super().__init__()
        MainUI.initUI(self)
        BackgroundImgUI.initUI(self)
        self.initQMountingWindowUI()


    def get_all_settings(self):
        cfg = {}
        for k in self.settings.allKeys():
            cfg.pop(k, self.settings.value(k))
        return cfg

    def initQMountingWindowUI(self):
        layout = QVBoxLayout()
        MainUI.initUI(self)
        button = QPushButton('Next ->')
        button.clicked.connect(self._nextWindow)
        layout.setAlignment(button, Qt.AlignBottom)
        self.dialogs = list()
        lb1 = QLabel("Your ad is mounted in a video. Waiting ..")
        lb1.setStyleSheet('font-weight: normal; font-size: 28px;')
        lb2 = QLabel(f"Downloads ... {self.get_download_val()}%")
        lb3 = QLabel("Detection ... 0%")
        lb4 = QLabel("Banner insert ... 0%")
        lb5 = QLabel("Processing ... 0%")
        layout.addWidget(lb1)
        layout.addWidget(lb2)
        layout.addWidget(lb3)
        layout.addWidget(lb4)
        layout.addWidget(lb5)
        layout.addWidget(button)
        self.setLayout(layout)
        self.settings = QSettings("settings.ini", QSettings.IniFormat)

        print(self.get_all_settings())
        video = 'test_video.mp4'
        logo = 'test_logo.png'

        processing_executor = ProcessingExecutor(video, logo, self.get_all_settings())
        processing_executor.process_video()

    def _nextWindow(self):
        next_win = QInsertAdsWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()

    def get_download_val(self):
        thread = AppThread()
        thread.run(cnt=2)
        print(thread.run(2))

        return 1


class QInsertAdsWindow(QWidget, MainUI):
    def __init__(self):
        self.title = 'Insert ADS'
        super().__init__()
        MainUI.initUI(self)
        self.initQInsertAdsWindowUI()

    def initQInsertAdsWindowUI(self):
        layout = QVBoxLayout()
        MainUI.initUI(self)
        button = QPushButton('Next ->')
        button.clicked.connect(self._nextWindow)
        layout.setAlignment(button, Qt.AlignBottom)
        self.dialogs = list()
        layout.addWidget(button)

        self.setLayout(layout)

    def _nextWindow(self):
        next_win = QMountedAdsWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()


class QMountedAdsWindow(QWidget, MainUI, BackgroundImgUI):
    def __init__(self):
        self.title = 'Mounted ADS Video'
        super().__init__()
        MainUI.initUI(self)
        self.initQMountingADSWindowUI()
        BackgroundImgUI.initUI(self)

    def initQMountingADSWindowUI(self):
        layout = QVBoxLayout()
        MainUI.initUI(self)
        button = QPushButton('Next ->')
        button.clicked.connect(self._nextWindow)
        layout.setAlignment(button, Qt.AlignBottom)
        self.dialogs = list()
        layout.addWidget(button)

        self.setLayout(layout)

    def _nextWindow(self):
        next_win = QCompleatWindow()
        self.dialogs.append(next_win)
        next_win.show()
        self.hide()


class QCompleatWindow(QWidget, MainUI):
    def __init__(self):
        self.title = 'Complete'
        super().__init__()
        MainUI.initUI(self)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('../static/styles.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    appctxt.app.setStyle('Windows')
    window = QStartWindow()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
