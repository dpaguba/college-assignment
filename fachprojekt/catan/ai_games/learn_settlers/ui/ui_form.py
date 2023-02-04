# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QTextBrowser,
    QVBoxLayout, QWidget)

from ai_games.learn_settlers.ui.board_view import BoardView

class Ui_Display(object):
    def setupUi(self, Display):
        if not Display.objectName():
            Display.setObjectName(u"Display")
        Display.resize(1412, 929)
        self.actionConnect = QAction(Display)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionJoinGame = QAction(Display)
        self.actionJoinGame.setObjectName(u"actionJoinGame")
        self.centralwidget = QWidget(Display)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.board = BoardView(self.centralwidget)
        self.board.setObjectName(u"board")
        self.board.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.horizontalLayout_2.addWidget(self.board)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.status = QLabel(self.centralwidget)
        self.status.setObjectName(u"status")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.status)

        self.ai_turn_button = QPushButton(self.centralwidget)
        self.ai_turn_button.setObjectName(u"ai_turn_button")

        self.horizontalLayout.addWidget(self.ai_turn_button)

        self.dice_button = QPushButton(self.centralwidget)
        self.dice_button.setObjectName(u"dice_button")

        self.horizontalLayout.addWidget(self.dice_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.resources = QTableWidget(self.centralwidget)
        if (self.resources.columnCount() < 7):
            self.resources.setColumnCount(7)
        if (self.resources.rowCount() < 1):
            self.resources.setRowCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.resources.setVerticalHeaderItem(0, __qtablewidgetitem)
        self.resources.setObjectName(u"resources")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resources.sizePolicy().hasHeightForWidth())
        self.resources.setSizePolicy(sizePolicy1)
        self.resources.setMinimumSize(QSize(512, 192))
        self.resources.setMaximumSize(QSize(16777215, 16777215))
        self.resources.setSizeIncrement(QSize(0, 0))
        self.resources.setBaseSize(QSize(0, 192))
        self.resources.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.resources.setTextElideMode(Qt.ElideLeft)
        self.resources.setRowCount(1)
        self.resources.setColumnCount(7)
        self.resources.horizontalHeader().setCascadingSectionResizes(False)
        self.resources.horizontalHeader().setMinimumSectionSize(50)
        self.resources.horizontalHeader().setDefaultSectionSize(50)
        self.resources.horizontalHeader().setProperty("showSortIndicator", True)
        self.resources.horizontalHeader().setStretchLastSection(False)
        self.resources.verticalHeader().setHighlightSections(True)

        self.verticalLayout.addWidget(self.resources)

        self.dev_cards = QTableWidget(self.centralwidget)
        if (self.dev_cards.columnCount() < 5):
            self.dev_cards.setColumnCount(5)
        if (self.dev_cards.rowCount() < 1):
            self.dev_cards.setRowCount(1)
        self.dev_cards.setObjectName(u"dev_cards")
        sizePolicy1.setHeightForWidth(self.dev_cards.sizePolicy().hasHeightForWidth())
        self.dev_cards.setSizePolicy(sizePolicy1)
        self.dev_cards.setMinimumSize(QSize(0, 80))
        self.dev_cards.setMaximumSize(QSize(16777215, 60))
        self.dev_cards.setBaseSize(QSize(80, 80))
        self.dev_cards.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.dev_cards.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.dev_cards.setRowCount(1)
        self.dev_cards.setColumnCount(5)
        self.dev_cards.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.dev_cards)

        self.trade_values = QTableWidget(self.centralwidget)
        if (self.trade_values.columnCount() < 5):
            self.trade_values.setColumnCount(5)
        if (self.trade_values.rowCount() < 1):
            self.trade_values.setRowCount(1)
        self.trade_values.setObjectName(u"trade_values")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.trade_values.sizePolicy().hasHeightForWidth())
        self.trade_values.setSizePolicy(sizePolicy2)
        self.trade_values.setMinimumSize(QSize(0, 120))
        self.trade_values.setMaximumSize(QSize(16777215, 100))
        self.trade_values.setBaseSize(QSize(0, 0))
        self.trade_values.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.trade_values.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.trade_values.setRowCount(1)
        self.trade_values.setColumnCount(5)
        self.trade_values.verticalHeader().setVisible(True)

        self.verticalLayout.addWidget(self.trade_values)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.trade_button = QPushButton(self.centralwidget)
        self.trade_button.setObjectName(u"trade_button")

        self.horizontalLayout_5.addWidget(self.trade_button)

        self.discard_button = QPushButton(self.centralwidget)
        self.discard_button.setObjectName(u"discard_button")

        self.horizontalLayout_5.addWidget(self.discard_button)

        self.decline_button = QPushButton(self.centralwidget)
        self.decline_button.setObjectName(u"decline_button")

        self.horizontalLayout_5.addWidget(self.decline_button)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_log = QLabel(self.centralwidget)
        self.label_log.setObjectName(u"label_log")

        self.horizontalLayout_4.addWidget(self.label_log)

        self.label_possible_actions = QLabel(self.centralwidget)
        self.label_possible_actions.setObjectName(u"label_possible_actions")

        self.horizontalLayout_4.addWidget(self.label_possible_actions)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.log = QTextBrowser(self.centralwidget)
        self.log.setObjectName(u"log")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.log.sizePolicy().hasHeightForWidth())
        self.log.setSizePolicy(sizePolicy3)
        self.log.setMinimumSize(QSize(0, 80))

        self.horizontalLayout_3.addWidget(self.log)

        self.pos_action_list = QTextBrowser(self.centralwidget)
        self.pos_action_list.setObjectName(u"pos_action_list")
        sizePolicy3.setHeightForWidth(self.pos_action_list.sizePolicy().hasHeightForWidth())
        self.pos_action_list.setSizePolicy(sizePolicy3)
        self.pos_action_list.setMinimumSize(QSize(0, 80))

        self.horizontalLayout_3.addWidget(self.pos_action_list)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.end_match_button = QPushButton(self.centralwidget)
        self.end_match_button.setObjectName(u"end_match_button")

        self.horizontalLayout_6.addWidget(self.end_match_button)

        self.end_turn_button = QPushButton(self.centralwidget)
        self.end_turn_button.setObjectName(u"end_turn_button")
        sizePolicy.setHeightForWidth(self.end_turn_button.sizePolicy().hasHeightForWidth())
        self.end_turn_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.end_turn_button)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        Display.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Display)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1412, 22))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        Display.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Display)
        self.statusbar.setObjectName(u"statusbar")
        Display.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionConnect)
        self.menuMenu.addAction(self.actionJoinGame)

        self.retranslateUi(Display)

        QMetaObject.connectSlotsByName(Display)
    # setupUi

    def retranslateUi(self, Display):
        Display.setWindowTitle(QCoreApplication.translate("Display", u"Display", None))
        self.actionConnect.setText(QCoreApplication.translate("Display", u"&Connect", None))
        self.actionJoinGame.setText(QCoreApplication.translate("Display", u"&JoinGame", None))
        self.status.setText(QCoreApplication.translate("Display", u"Waiting for Start", None))
        self.ai_turn_button.setText(QCoreApplication.translate("Display", u"AI turn", None))
        self.dice_button.setText(QCoreApplication.translate("Display", u"0", None))
        self.trade_button.setText(QCoreApplication.translate("Display", u"Trade", None))
        self.discard_button.setText(QCoreApplication.translate("Display", u"Discard", None))
        self.decline_button.setText(QCoreApplication.translate("Display", u"Decline", None))
        self.label_log.setText(QCoreApplication.translate("Display", u"Action Log", None))
        self.label_possible_actions.setText(QCoreApplication.translate("Display", u"Possible Actions", None))
        self.end_match_button.setText(QCoreApplication.translate("Display", u"End Match", None))
        self.end_turn_button.setText(QCoreApplication.translate("Display", u"End Turn (Pass)", None))
        self.menuMenu.setTitle(QCoreApplication.translate("Display", u"Menu", None))
    # retranslateUi

