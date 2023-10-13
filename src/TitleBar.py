import sys
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import *
import os
from PySide6.QtGui import QColor, QAction
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *
from qframelesswindow import *
from tkinter import filedialog, messagebox
from TextWidget import TWidget


class CustomTitleBar(MSFluentTitleBar):

    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.toolButtonLayout = QHBoxLayout()
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.menuButton = TransparentToolButton(FIF.MENU, self)
        self.forwardButton = TransparentToolButton(FIF.RIGHT_ARROW.icon(color=color), self)
        self.backButton = TransparentToolButton(FIF.LEFT_ARROW.icon(color=color), self)

        # self.openButton = TransparentToolButton(QIcon("resource/open.png"), self)
        # self.openButton.clicked.connect(parent.open_document)
        # self.newButton = TransparentToolButton(QIcon("resource/new.png"), self)
        # self.newButton.clicked.connect(parent.onTabAddRequested)
        # self.saveButton = TransparentToolButton(QIcon("resource/save.png"), self)
        # self.saveButton.clicked.connect(parent.save_document)

        self.forwardButton.setDisabled(True)
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.menuButton)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)

        # self.toolButtonLayout.addWidget(self.openButton)
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

        # add tab bar
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        # self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)

        # self.hBoxLayout.insertWidget(7, self.saveButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertWidget(7, self.openButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertWidget(7, self.newButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertSpacing(8, 20)

        self.menu = RoundMenu("Menu")
        self.menu.setStyleSheet("QMenu{color : red;}")

        file_menu = RoundMenu("File", self)
        new_action = Action(text="New", icon=FIF.ADD.icon(QColor("white")))
        new_action.triggered.connect(parent.onTabAddRequested)
        file_menu.addAction(new_action)
        open_action = Action(text="Open", icon=FIF.SEND_FILL)
        open_action.triggered.connect(parent.open_document)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        save_action = Action(text="Save", icon=FIF.SAVE)
        save_action.triggered.connect(parent.save_document)
        file_menu.addAction(save_action)
        self.menu.addMenu(file_menu)

        edit_menu = RoundMenu("Edit", self)
        cut_action = Action(text="Cut", icon=FIF.CUT.icon(QColor("white")))
        cut_action.triggered.connect(lambda : TWidget.cut(parent.current_editor))
        edit_menu.addAction(cut_action)
        copy_action = Action(text="Copy", icon=FIF.COPY)
        copy_action.triggered.connect(lambda : TWidget.copy(parent.current_editor))
        edit_menu.addAction(copy_action)
        edit_menu.addSeparator()
        paste_action = Action(text="Paste", icon=FIF.PASTE)
        paste_action.triggered.connect(lambda : TWidget.paste(parent.current_editor))
        edit_menu.addAction(paste_action)
        self.menu.addMenu(edit_menu)


        # Create the menuButton
        # self.menuButton = TransparentToolButton(FIF.MENU, self)
        self.menuButton.clicked.connect(self.showMenu)

    def showMenu(self):
        # Show the menu at the position of the menuButton
        self.menu.exec(self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft()))

    def canDrag(self, pos: QPoint):
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)

    def test(self):
        print("hello")