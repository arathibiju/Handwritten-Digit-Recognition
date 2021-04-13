
import sys
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QWidget, qApp
from PyQt5.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.label = QLabel()
        canvas = QPixmap(400, 300)
        canvas.fill(QColor("white"))
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.last_x, self.last_y = None, None

        self.initUI()
        

    def initUI(self):
        ## menu bar set up
        # Set menu bar exit action
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        #set menu bar options
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        viewmenu = menubar.addMenu('&View')
        helpmenu = menubar.addMenu('&Help')

        #set status message
        self.statusBar().showMessage('Ready')

    

        self.setWindowTitle('Handwritten Digit Recognizer')
        self.setGeometry(300, 300, 600, 500)

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QPainter(self.label.pixmap())
        painter.drawLine(self.last_x, self.last_y  -35, e.x(), e.y() - 35)
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()


    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        
    def resizeEvent(self, event):
        canvas = self.label.pixmap()
        canvas = canvas.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(canvas)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
