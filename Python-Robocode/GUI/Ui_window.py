# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/charlie/Documents/Python/RobotCode/PyQt-Robocode/Python-Robocode/GUI/window.ui'
#
# Created: Fri Dec 20 17:46:14 2013
#      by: PyQt4 UI code generator 4.10
# Modified: Thu Oct 17 12:30:00JST 2019
#      by: hjmr
#
# WARNING! All changes made in this file will be lost!


from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QGraphicsView
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QSlider, QLabel, QCheckBox
from PyQt6.QtWidgets import QSpinBox, QSpacerItem, QMenuBar, QMenu, QStatusBar
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import Qt, QSize, QRect, QMetaObject


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 464)
        icon = QIcon()
        icon.addPixmap(QPixmap("robotImages/smallRed.png"), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableWidget)

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setStyleSheet("background-color: rgba(206, 206, 206, 162);")
        self.graphicsView.setObjectName("graphicsView")

        self.verticalLayout_3.addWidget(self.graphicsView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.label_battle_num = QLabel(self.centralwidget)
        self.label_battle_num.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_battle_num)
        self.spinBox_battle_num = QSpinBox(self.centralwidget)
        self.spinBox_battle_num.setMaximum(10000)
        self.spinBox_battle_num.setProperty("value", 10)
        self.spinBox_battle_num.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox_battle_num)
        self.verticalLayout.addLayout(self.horizontalLayout)

        #self.cbRandomWalls = QCheckBox(self.centralwidget)
        #self.cbRandomWalls.setObjectName("cbRandomWalls")
        #self.verticalLayout.addWidget(self.cbRandomWalls)

        self.horizontalLayout_2.addLayout(self.verticalLayout)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.label_game_speed = QLabel(self.centralwidget)
        self.label_game_speed.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_game_speed.setStyleSheet("")
        self.label_game_speed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_game_speed.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label_game_speed)

        self.hslider_game_speed = QSlider(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hslider_game_speed.sizePolicy().hasHeightForWidth())
        self.hslider_game_speed.setSizePolicy(sizePolicy)
        self.hslider_game_speed.setMinimumSize(QSize(200, 0))
        self.hslider_game_speed.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.hslider_game_speed.setMaximum(120)
        self.hslider_game_speed.setProperty("value", 60)
        self.hslider_game_speed.setOrientation(Qt.Orientation.Horizontal)
        self.hslider_game_speed.setInvertedAppearance(False)
        self.hslider_game_speed.setInvertedControls(True)
        self.hslider_game_speed.setObjectName("horizontalSlider")
        self.verticalLayout_2.addWidget(self.hslider_game_speed)

        self.terminateButton = QPushButton(self.centralwidget)
        self.terminateButton.setObjectName("terminateButton")
        self.verticalLayout_2.addWidget(self.terminateButton)
                
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.graphicsView_2 = QGraphicsView(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_2.sizePolicy().hasHeightForWidth())
        self.graphicsView_2.setSizePolicy(sizePolicy)
        self.graphicsView_2.setMinimumSize(QSize(200, 0))
        self.graphicsView_2.setMaximumSize(QSize(200, 16777215))
        self.graphicsView_2.setStyleSheet("background-color: rgba(194, 194, 194, 167);")
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.horizontalLayout_3.addWidget(self.graphicsView_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 792, 23))
        self.menubar.setObjectName("menubar")
        self.menuBattle = QMenu(self.menubar)
        self.menuBattle.setObjectName("menuBattle")
        self.menuRobot = QMenu(self.menubar)
        self.menuRobot.setObjectName("menuRobot")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew_2 = QAction(MainWindow)
        self.actionNew_2.setObjectName("actionNew_2")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClass_Reference = QAction(MainWindow)
        self.actionClass_Reference.setObjectName("actionClass_Reference")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuBattle.addAction(self.actionNew)
        self.menuRobot.addAction(self.actionNew_2)
        self.menuRobot.addAction(self.actionOpen)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionClass_Reference)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuBattle.menuAction())
        self.menubar.addAction(self.menuRobot.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "Python Robocode"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QApplication.translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QApplication.translate("MainWindow", "1st"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(QApplication.translate("MainWindow", "2nd"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(QApplication.translate("MainWindow", "3rd"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(QApplication.translate("MainWindow", "Points"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(QApplication.translate("MainWindow", "Kills"))
        self.pushButton.setText(QApplication.translate("MainWindow", "Start Last Battle"))
        self.label_battle_num.setText(QApplication.translate("MainWindow", "Battle\'s Number"))
        self.label_game_speed.setText(QApplication.translate("MainWindow", "Game Speed"))
        self.menuBattle.setTitle(QApplication.translate("MainWindow", "Battle"))
        self.menuRobot.setTitle(QApplication.translate("MainWindow", "Robot"))
        self.menuHelp.setTitle(QApplication.translate("MainWindow", "Help"))
        self.actionNew.setText(QApplication.translate("MainWindow", "New"))
        self.actionNew_2.setText(QApplication.translate("MainWindow", "New"))
        self.actionOpen.setText(QApplication.translate("MainWindow", "Open"))
        self.actionClass_Reference.setText(QApplication.translate("MainWindow", "Class Reference"))
        self.actionAbout.setText(QApplication.translate("MainWindow", "About"))
        # self.cbRandomWalls.setText(QApplication.translate("MainWindow", "Set Random Walls"))
        self.terminateButton.setText(QApplication.translate("MainWindow", "Terminate Current Battle"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

