# ##
# This is the VIEW of the application
# ##

import sys
from PyQt5.QtWidgets    import QApplication, QWidget, QPushButton, QToolTip, QLabel, QDialog
from PyQt5.QtWidgets    import QMainWindow, QAction, qApp, QDesktopWidget, QSizePolicy
from PyQt5.QtWidgets    import QGridLayout, QHBoxLayout, QMenu, QProgressBar, QTextBrowser, QVBoxLayout
from PyQt5.QtGui        import QColor, QCursor, QIcon, QPainter, QPen, QPixmap, QPixmap
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
        self.train_images_view = ViewModelImages(self)
        #ex1.show()
        # #ex1.hide()
        #sys.exit(app.exec_())

class drawCanvas(QWidget) :
    def __init__(self):
        super().__init__()


        #set widget in a gridlayout for display
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Initialize the pixmap to be same size as the widget and make it white
        self.canvas = QPixmap(self.width(),self.height())
        #canvas = QPixmap(400,400)
        self.canvas.fill(QColor("white"))
        #assign the pixmap to a Qlabel for display it on the widget
        self.label = QLabel()
        self.label.setPixmap(self.canvas)
        

        #add QLabel to the layout to display the pixmap
        self.layout.addWidget(self.label, 0, 0)

        #initialize first mouse coordinates for Qpainter
        self.last_x, self.last_y = None, None

        #set minimum size of canvas
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        
    def sizeHint(self):
        return QSize(400,300)
        
        ### tried to fix resize event but instead it creates weird outcome
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.drawPixmap(self.rect(), self.canvas)

    #Implemetation of painting logic
    def mouseMoveEvent(self, e):
        
            ## For every new "stroke" ie every new click and drag reset the mouse coordinates
            if self.last_x is None: # First event.
             self.last_x = e.x()
             self.last_y = e.y()
             return # Ignore the first time.

            # rect = self.contentsRect()
            # pmRect = self.canvas.rect()
            # if rect != pmRect:
            # # the pixmap rect is different from that available to the label
            #     align = self.alignment()
            # if align & Qt.AlignHCenter:
            #     # horizontally align the rectangle
            #     pmRect.moveLeft((rect.width() - pmRect.width()) / 2)
            # elif align & Qt.AlignRight:
            #     # align to bottom
            #     pmRect.moveRight(rect.right())
            # if align & Qt.AlignVCenter:
            #     # vertically align the rectangle
            #     pmRect.moveTop((rect.height() - pmRect.height()) / 2)
            # elif align & Qt.AlignBottom:
            #     # align right
            #     pmRect.moveBottom(rect.bottom())


            ## set the painter widget to act on the pixmap, set pen and stroke size
            painter = QPainter(self.label.pixmap())
            painter.setPen(QPen(Qt.black, 20))
            #painter.drawLine(self.last_x, self.last_y  -35, e.x(), e.y() - 35)
            #draw a line from the current mouse position to the last mouse position
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())

            #end painting and update window (dependent on screen refresh rate)
            painter.end()
            self.update()

            # Update the origin for next time.
            self.last_x = e.x()
            self.last_y = e.y()

    ## Reset the mouse coordinates every mouse release
    def mouseReleaseEvent(self, e):
            
        self.last_x = None
        self.last_y = None
        
    ## Logic for clear canvas button, simply set the pixmap to be fully white
    def clearCanvas(self):
        self.canvas = self.label.pixmap()
        self.canvas.fill(QColor("white"))
        self.update()
    
    ## Logic for Saving Image
    ## Scale down the image to required size, smooth transformation and save as .png
    def saveImage(self):
        image = self.label.pixmap()
        image = image.scaled(20, 20, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        image.save("SavedTestImage.png")

        
    def resizeEvent(self, event):
        pass

class MyApp(QMainWindow):

    def __init__(self, View):
        super().__init__()

        self.Controller = View.Controller


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

        train_action = QAction("Train", self)
        train_action.setStatusTip('Train the Model')
        train_action.triggered.connect(self.Controller.show_train_dialog)

        helpAction = QAction("Docs", self)
        helpAction.setStatusTip('View github docs and instructions')

        trainImagesAction = QAction("View Training Images", self)
        trainImagesAction.setStatusTip('View Training Images used by the model')
        trainImagesAction.triggered.connect(self.Controller.show_train_images_view)
        testImagesAction = QAction("View Testing Images", self)
        testImagesAction.setStatusTip('View Testing Images')

        #set menu bar options
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(train_action)
        filemenu.addAction(exitAction)
        

        viewmenu = menubar.addMenu('&View')
        viewmenu.addAction(trainImagesAction)
        viewmenu.addAction(testImagesAction)

        helpmenu = menubar.addMenu('&Help')
        helpmenu.addAction(helpAction)

        #set status message
        self.statusBar().showMessage('Ready')

    

        self.setWindowTitle('Handwritten Digit Recognizer')
        self.setGeometry(300, 300, 400, 400)

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
        self.text_brower.setContextMenuPolicy(Qt.CustomContextMenu)


    ### Set up the progress bar here
    # Label for the progress bar
        self.plabel = QLabel('-/-', self)
    # Nothing is connected to the progress bar for now!
        self.pbar = QProgressBar(self)
        self.pbar.setTextVisible(True)
        self.pbar.setAlignment(Qt.AlignCenter)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)      # Set the progress bar to 0 at the beginning!

        #self.pbar.setAttribute(Qt.WA_StyledBackground)
        #StyleSheet = "GreenProgressBar::chunk {background-color: #009688;}"
        #StyleSheet = "QProgressBar""{""border: solid grey;""border-radius: 50px;"" color: black; E0E0E0""}05B8CC"
        #self.pbar.setStyleSheet(StyleSheet)
        """ css doesn't work properly, idk why??? """
        
        self.pbar.setStyleSheet("QProgressBar"
                          "{"
                          "border: solid grey;"
                          "border-radius: 15px;"
                          " color: black; "
                          "}"
                          "QProgressBar::chunk "
                          "{background-color: #009688;"
                          "border-radius :150px;"
                          "}")


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
        self.download_btn.clicked.connect(self.Controller.start_worker_1_download)
        self.download_btn.clicked.connect(self.Controller.downloadDialog)
        self.train_btn.clicked.connect(self.Controller.start_worker_1_train)
        self.train_btn.clicked.connect(self.Controller.start_worker_2_train)
        self.train_btn.clicked.connect(self.Controller.trainDialog)
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
            ### turn off self.show(), move this into a View tab on Main Window
            ### only use this for quick debugging
        self.show()

    

    ###We can define the centre of the dialog here, may be centre of the screen or centre of the current app???
    def centre(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            self.menu = QMenu()
            clearAction = QAction("Clear", self)
            clearAction.triggered.connect(self.Controller.clearDialog)
            self.menu.addAction(clearAction)

            CopyAction = QAction("Copy", self)
            self.menu.popup(QCursor.pos())

    
        print("right button was clicked from menu")


 
            
    ### Debugging command to be used internally in View.py, OFF by default!
    # def set_commands(something):
    #     self.commands = something
    #     print('commands successfully sent!')

    # def enable_button(self):
    #     if self.train_btn.isChecked():
    #         self.download_btn.setEnabled(True)
    #         self.cancel_btn.setEnabled(True)
    #     else:
    #         self.download_btn.setEnabled(False)
    #         self.cancel_btn.setEnabled(False) 

    
class ViewTrainImages(QMainWindow):
    def __init__(self, View):
        super().__init__()   
        print("view model dialog init")
        self.View = View
        self.Controller = self.View.Controller
        
        self.initUI()

    def initUI(self):

    ### Here we use a combination of HBox and VBox
    #First, define the buttons we want to use
        self.next_btn = QPushButton('&Next', self)
        self.prev_btn = QPushButton('&Previous', self)
        


        hbox = QHBoxLayout()
        hbox.addWidget(self.prev_btn)
        hbox.addWidget(self.next_btn)

        vbox  = QVBoxLayout()
        #vbox.addStretch(4)
        vbox.addLayout(hbox)

        self.setLayout(vbox)  


        print('hey we are inside initUI dialog')
        print(self.View)
        print(self)

        
    ### Initialise the postion of the trainModelDialog window.
        # It's not easy to make this tile to be at the centrem
        # may need to create a custom bar for this
        self.setWindowTitle('View Training Images')
        self.move(300, 300)
        self.resize(400, 200)
        self.centre()
            ### turn off self.show(), move this into a View tab on Main Window
            ### only use this for quick debugging
        #self.show()

    

    ###We can define the centre of the dialog here, may be centre of the screen or centre of the current app???
    def centre(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 



class ViewModelImages(QMainWindow):
    def __init__(self, View):
        super().__init__()   
        print("view model dialog init")
        self.View = View
        self.Controller = self.View.Controller
        
        self.initUI()

    def initUI(self):

    ### Here we use a combination of HBox and VBox
    #First, define the buttons we want to use
        self.next_btn = QPushButton('&Next', self)
        self.prev_btn = QPushButton('&Previous', self)
        


        hbox = QHBoxLayout()
        hbox.addWidget(self.prev_btn)
        hbox.addWidget(self.next_btn)

        vbox  = QVBoxLayout()
        #vbox.addStretch(4)
        vbox.addLayout(hbox)

        self.setLayout(vbox)  


        print('hey we are inside initUI dialog')
        print(self.View)
        print(self)

        
    ### Initialise the postion of the trainModelDialog window.
        # It's not easy to make this tile to be at the centrem
        # may need to create a custom bar for this
        self.setWindowTitle('View Training Images')
        self.move(300, 300)
        self.resize(400, 200)
        self.centre()
            ### turn off self.show(), move this into a View tab on Main Window
            ### only use this for quick debugging
        #self.show()

    

    ###We can define the centre of the dialog here, may be centre of the screen or centre of the current app???
    def centre(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 