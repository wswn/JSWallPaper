# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1172, 977)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy2)
        self.progressBar.setMaximumSize(QSize(16777215, 5))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.toolHorizontalLayout = QHBoxLayout()
        self.toolHorizontalLayout.setObjectName(u"toolHorizontalLayout")
        self.goLabel = QLabel(self.centralwidget)
        self.goLabel.setObjectName(u"goLabel")
        self.goLabel.setStyleSheet(u"margin-left: 5")
        self.goLabel.setScaledContents(False)

        self.toolHorizontalLayout.addWidget(self.goLabel)

        self.urlComboBox = QComboBox(self.centralwidget)
        self.urlComboBox.setObjectName(u"urlComboBox")
        self.urlComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.toolHorizontalLayout.addWidget(self.urlComboBox)

        self.savePushButton = QPushButton(self.centralwidget)
        self.savePushButton.setObjectName(u"savePushButton")
        self.savePushButton.setStyleSheet(u"margin-left: 5")

        self.toolHorizontalLayout.addWidget(self.savePushButton)

        self.saveLineEdit = QLineEdit(self.centralwidget)
        self.saveLineEdit.setObjectName(u"saveLineEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.saveLineEdit.sizePolicy().hasHeightForWidth())
        self.saveLineEdit.setSizePolicy(sizePolicy3)
        self.saveLineEdit.setMaxLength(256)
        self.saveLineEdit.setReadOnly(True)

        self.toolHorizontalLayout.addWidget(self.saveLineEdit)


        self.verticalLayout.addLayout(self.toolHorizontalLayout)

        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.webEngineView)

        self.verticalLayout.setStretch(2, 10)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JSWallpaper", None))
        self.goLabel.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.savePushButton.setText(QCoreApplication.translate("MainWindow", u"Save into", None))
    # retranslateUi

