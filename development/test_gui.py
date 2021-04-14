
import sys
from PyQt5.QtWidgets import QAction, QApplication, QGridLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QWidget, qApp
from PyQt5.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtCore import QSize, Qt


class drawCanvas(QWidget) :
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        canvas = QPixmap(self.width(),self.height())
        canvas.fill(QColor("white"))
        self.label = QLabel()
        self.label.setPixmap(canvas)

        self.layout.addWidget(self.label, 0, 0)

        self.last_x, self.last_y = None, None

        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        
    def sizeHint(self):
        return QSize(400,300)
        
    def mouseMoveEvent(self, e):
        

            if self.last_x is None: # First event.
             self.last_x = e.x()
             self.last_y = e.y()
             return # Ignore the first time.

            painter = QPainter(self.label.pixmap())
            painter.setPen(QPen(Qt.black, 8))
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
        pass


class MyApp(QMainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        
        # canvas = QPixmap(400, 300)
        # canvas.fill(QColor("white"))
        # self.label = QLabel()
        # self.label.setPixmap(canvas)
        # self.setCentralWidget(self.label)

        # grid = QGridLayout()
        # self.setLayout(grid)

        # grid.addWidget(self.label,0,0)
        # grid.addWidget(QPushButton("Button two"),0,1)
        
        

        self.initUI()

        self.window = QWidget()
        
        self.layout = QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
  
        self.draw_widget = drawCanvas()
  
        self.layout.addWidget(self.draw_widget,0,0,5,5)
        self.layout.addWidget(QPushButton("Clear"),0,6)
        self.layout.addWidget(QPushButton("Model"),0,7)
        self.layout.addWidget(QPushButton("Recognize"),0,8)


    def initUI(self):
        ## menu bar set up
        # Set menu bar exit action
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        trainAction = QAction("Train", self)
        trainAction.setStatusTip('Train the Model')

        helpAction = QAction("Docs", self)
        helpAction.setStatusTip('View github docs and instructions')

        trainImagesAction = QAction("View Training Images", self)
        trainImagesAction.setStatusTip('View Training Images used by the model')
        testImagesAction = QAction("View Testing Images", self)
        testImagesAction.setStatusTip('View Testing Images')

        #set menu bar options
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(trainAction)
        filemenu.addAction(exitAction)
        

        viewmenu = menubar.addMenu('&View')
        viewmenu.addAction(trainImagesAction)
        viewmenu.addAction(testImagesAction)

        helpmenu = menubar.addMenu('&Help')
        helpmenu.addAction(helpAction)

        #set status message
        self.statusBar().showMessage('Ready')

    

        self.setWindowTitle('Handwritten Digit Recognizer')
        self.setGeometry(300, 300, 600, 500)

    # def mouseMoveEvent(self, e):
        

    #         if self.last_x is None: # First event.
    #          self.last_x = e.x()
    #          self.last_y = e.y()
    #          return # Ignore the first time.

    #         painter = QPainter(self.label.pixmap())
    #         painter.setPen(QPen(Qt.black, 8))
    #         painter.drawLine(self.last_x, self.last_y  -35, e.x(), e.y() - 35)
    #         painter.end()
    #         self.update()

    #         # Update the origin for next time.
    #         self.last_x = e.x()
    #         self.last_y = e.y()


    # def mouseReleaseEvent(self, e):
        
            
    #     self.last_x = None
    #     self.last_y = None
        
    # def resizeEvent(self, event):
    #     canvas = self.label.pixmap()
    #     canvas = canvas.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     self.label.setPixmap(canvas)




    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
