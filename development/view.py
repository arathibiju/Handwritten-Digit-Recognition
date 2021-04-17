# ##
# This is the VIEW of the application
# ##

import sys
from PyQt5.QtWidgets    import QApplication, QWidget, QPushButton, QToolTip, QLabel, QDialog
from PyQt5.QtWidgets    import QMainWindow, QAction, qApp, QDesktopWidget, QSizePolicy
from PyQt5.QtWidgets    import QGridLayout, QHBoxLayout, QVBoxLayout, QTextBrowser, QProgressBar
from PyQt5.QtGui        import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtCore       import QSize, Qt, QBasicTimer

class View:
    def __init__(self, Controller):
        print('We are in init of View')
        self.Controller = Controller
        print(Controller)

    def main(self):
        print('We are in main of View')
        print(self.Controller)

        #self.mainloop()
        
        
        self.main_view = MyApp(self)
        
        self.dialog_view = TrainModelDialog(self)
        #ex1.show()
        # #ex1.hide()
        #sys.exit(app.exec_())

class drawCanvas(QWidget) :
    def __init__(self):
        super().__init__()

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
            painter.setPen(QPen(Qt.black, 25))
            #painter.drawLine(self.last_x, self.last_y  -35, e.x(), e.y() - 35)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())

            painter.end()
            self.update()

            # Update the origin for next time.
            self.last_x = e.x()
            self.last_y = e.y()

    def clearCanvas(self):
        canvas = self.label.pixmap()
        canvas.fill(QColor("white"))
        self.update()
    
    def saveImage(self):
        image = self.label.pixmap()
        #image = image.scaled(20, 20, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        image.save("Testfxghfgdcjg.png")



    def mouseReleaseEvent(self, e):
            
        self.last_x = None
        self.last_y = None
        
    def resizeEvent(self, event):
        pass

class MyApp(QMainWindow):

    def __init__(self, view):
        super().__init__()
        print('myapp')
        self.initUI()

        self.window = QWidget()
        self.setCentralWidget(self.window)
        self.layout = QGridLayout()
        self.window.setLayout(self.layout)
  
        self.draw_widget = drawCanvas()
  
        self.layout.addWidget(self.draw_widget,0,0,5,1)

        clearButton = QPushButton("Clear",self)
        clearButton.clicked.connect(self.draw_widget.clearCanvas)

        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.draw_widget.saveImage)

        modelButton = QPushButton("Model",self)

        recognizeButton = QPushButton("Recognize",self)


        self.layout.addWidget(clearButton,1,1)
        self.layout.addWidget(modelButton,2,1)
        self.layout.addWidget(recognizeButton,3,1)
        self.layout.addWidget(saveButton,4,1)


    def initUI(self):
        print('myapp ui')
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

        self.show()

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

class TrainModelDialog(QWidget):
    def __init__(self, View):
        super().__init__()   
        
        self.View = View
        self.Controller = self.View.Controller
        print('now I see why')
        print(self.View)
        print('This is the controller inside the dialog')
        print(self.View.Controller)
        print(self.Controller)
        print(self.View.Controller.random_value)
        
        self.initUI()

    def initUI(self):
    ### Set up the browser here
        self.text_brower = QTextBrowser()
        self.text_brower.setAcceptRichText(True)

    ### Set up the progress bar here
    # Label for the progress bar
        self.plabel = QLabel('-/-', self)
    # Nothing is connected to the progress bar for now!
        self.pbar = QProgressBar(self)
        self.pbar.setTextVisible(True)
        self.pbar.setAlignment(Qt.AlignCenter)


    ### Set the layout for the trainModelDialog window.
    ### Here we use a combination of HBox and VBox
    #First, define the buttons we want to use
        self.train_btn = QPushButton('&Train', self)
        self.download_btn = QPushButton('&Download MNIST', self)
        self.cancel_btn = QPushButton('&Cancel', self)

        print('hey we are inside initUI dialog')
        print(self.View)
        print(self)

        #self.download_btn.setCheckable(True)

        self.train_btn.setEnabled(False)
        #self.cancel_btn.setCheckable(True)
        self.download_btn.clicked.connect(self.Controller.start_worker_1)
        self.train_btn.clicked.connect(self.Controller.start_worker_2)
        self.cancel_btn.clicked.connect(self.Controller.stop_worker_1)
        self.cancel_btn.clicked.connect(self.Controller.stop_worker_2)

    #hbox for all the buttons
        hbox = QHBoxLayout()
        #hbox.addStretch(0)
        hbox.addWidget(self.download_btn)
        hbox.addWidget(self.train_btn)
        hbox.addWidget(self.cancel_btn)

    #hbox for the progress bar!
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.pbar)
        hbox2.addWidget(self.plabel)
      
        vbox  = QVBoxLayout()
        #vbox.addStretch(4)
        vbox.addWidget(self.text_brower)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)   

    ### Initialise the postion of the trainModelDialog window.
        # It's not easy to make this tile to be at the centrem
        # may need to create a custom bar for this
        self.setWindowTitle('Dialog')
        self.move(300, 300)
        self.resize(400, 200)
        self.centre()
        self.show()

    

    ###We can define the centre of the dialog here, may be centre of the screen or centre of the current app???
    def centre(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    def set_commands(something):
        self.commands = something
        print('commands successfully sent!')

    # def enable_button(self):
    #     if self.train_btn.isChecked():
    #         self.download_btn.setEnabled(True)
    #         self.cancel_btn.setEnabled(True)
    #     else:
    #         self.download_btn.setEnabled(False)
    #         self.cancel_btn.setEnabled(False) 

    