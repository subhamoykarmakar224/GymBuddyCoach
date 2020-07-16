from PyQt4.QtGui import *
import Configuration as cfg


# Title Bar
class WindowTitleBar(QWidget):
    def __init__(self, mainwindow):
        super(WindowTitleBar, self).__init__()
        self.mainwindow = mainwindow
        css = """
                QWidget{
                    background: """ + cfg.COLOR_CHARCOAL + """
                    color:red
                    font:12px bold
                    font-weight:bold
                    border-radius: 1px
                    height: 11px
                }
                """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)
        self.setStyleSheet(css)
        self.mainwindow.setWindowTitle(cfg.APPLICATION_TITLE)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.maxNormal = True

        # Main Layout
        hbox = QHBoxLayout(self)

        # Widgets
        self.minimize = QPushButton(self)
        self.maximize = QPushButton(self)
        close = QPushButton(self)
        label = QLabel(cfg.APPLICATION_TITLE)

        # Widget Properties
        self.minimize.setIcon(QIcon('img/min.png'))
        self.minimize.setAutoFillBackground(True)
        self.minimize.setMinimumHeight(10)
        self.minimize.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.maximize.setIcon(QIcon('img/max2.png'))
        self.maximize.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.maximize.setMinimumHeight(10)
        close.setIcon(QIcon('img/close.png'))
        close.setMinimumHeight(10)
        close.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # Add to Main Layout
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1, 500)
        hbox.setSpacing(0)

        # Listeners
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

        self.setLayout(hbox)

    def showSmall(self):
        self.mainwindow.showMinimized()

    def showMaxRestore(self):
        if self.maxNormal:
            self.mainwindow.showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QIcon('img/max.png'))
        else:
            self.mainwindow.showMaximized()
            self.maxNormal = True
            self.maximize.setIcon(QIcon('img/max2.png'))

    def close(self):
        self.mainwindow.close()
