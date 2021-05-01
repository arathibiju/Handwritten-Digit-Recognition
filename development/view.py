# ##
# This is the VIEW of the application
# ##

import sys
from PyQt5.QtWidgets    import QApplication, QWidget, QPushButton, QToolTip, QLabel, QDialog, QComboBox
from PyQt5.QtWidgets    import QMainWindow, QAction, qApp, QDesktopWidget, QSizePolicy, QTabWidget
from PyQt5.QtWidgets    import QGridLayout, QHBoxLayout, QMenu, QProgressBar, QTextBrowser, QVBoxLayout, QScrollArea
from PyQt5.QtGui        import QColor, QCursor, QIcon, QPainter, QPen, QPixmap, QPixmap, QFont
from PyQt5.QtCore       import QSize, Qt, QBasicTimer 


class View:
    def __init__(self, Controller):
        ##initialise the controller instance
        self.Controller = Controller

    def main(self):

        
        ## connect the different classes in View.py to the View class
        self.main_view = MyApp(self)
        
        self.dialog_view = TrainModelDialog(self)
        self.view_images = ViewImages(self)
        self.view_images_tabs = viewImagesTabs(self)
        


## this widget creates the canvas and updates the painter according to each mouse click and drag
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
            painter.setPen(QPen(Qt.black, 20, Qt.SolidLine, Qt.RoundCap))
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
        image.save("SavedImage.png")

        
    def resizeEvent(self, event):
        pass
  
## widget for main window in UI
class MyApp(QMainWindow):

    def __init__(self, View):
        super().__init__()

        #connect the controller class inherited from View to the MyApp class
        self.Controller = View.Controller


        ## initialise the mainwindow, add menubar and size
        self.initUI()

        ##create a widget and set is as the central widget in the window
        self.window = QWidget()
        self.setCentralWidget(self.window)
        ## appply a grid layout to the window
        self.layout = QGridLayout()
        self.window.setLayout(self.layout)
        ## add a draw canvas object to the main window
        self.draw_widget = drawCanvas()
        self.layout.addWidget(self.draw_widget,0,0)

        ## add a Qlabel to display the graph in the main window
        self.graph = QLabel()
        self.graph.setPixmap(QPixmap('BlankGraph.png'))
        ## add a Qlabel to display the recognition text in the main window under the graph
        self.text = QLabel()
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setText("Please draw a digit")

        ## set up the clear and reconize buttons functionality
        clearButton = QPushButton("Clear",self)
        clearButton.setStatusTip("Clear the Canvas")
        clearButton.clicked.connect(self.draw_widget.clearCanvas)

        self.recognizeButton = QPushButton("Recognize",self)
        self.recognizeButton = QPushButton("Recognize",self)
        self.recognizeButton.setStatusTip("Classify the drawn digit. Please load model before classifying")
        self.recognizeButton.setEnabled(False)
        self.recognizeButton.clicked.connect(self.recognizeButtonCheck)

        ## add the buttons, graph and text to layout
        self.layout.addWidget(clearButton,1,0)
        self.layout.addWidget(self.recognizeButton,2,0)
        self.layout.addWidget(self.graph, 0, 1)
        self.layout.addWidget(self.text, 1,1)
        
        self.setFixedSize(1300, 700)

        

    ## Reset the graph every time the recognize button is clicked.
    ## this is called from controller
    def resetGraph(self):
        self.graph.setPixmap(QPixmap('Graph.png'))

    ## Reset the text every time the recognize button is clicked.
    ## this is called from controller
    def resetText(self, digit):
        self.text.setText(f"Your digit is {digit}")
        

    ## save the image when recognize button is clicked
    ##start procesing images when recognize button clicked
    def recognizeButtonCheck(self):
        self.draw_widget.saveImage()
        self.Controller.process_images_control()

    def initUI(self):
        ## menu bar set up
        # Set menu bar exit action
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        ## set up a train action that connects to the train window
        train_action = QAction("Train", self)
        train_action.setStatusTip('Train the Model')
        train_action.triggered.connect(self.Controller.show_train_dialog)


        # trainImagesAction = QAction("View Training Images", self)
        # trainImagesAction.setStatusTip('View Training Images used by the model')
        # trainImagesAction.triggered.connect(self.Controller.show_images_view)
        # testImagesAction = QAction("View Testing Images", self)
        # testImagesAction.setStatusTip('View Testing Images')

        ## set up an action that opens the view images window
        imagesAction = QAction("View Model Images", self)
        imagesAction.setStatusTip('View the training and testing images used by the model')
        imagesAction.triggered.connect(self.Controller.show_images_view)



        #set menu bar options
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(train_action)
        filemenu.addAction(exitAction)
        viewmenu = menubar.addMenu('&View')
        viewmenu.addAction(imagesAction)
       

        #set status message
        self.statusBar().showMessage('Ready')

        # set window geometry
        self.setWindowTitle('Handwritten Digit Recognizer')
        self.setGeometry(300, 300, 400, 400)

        self.show()
    
        
    # def resizeEvent(self, event):
    #     canvas = self.label.pixmap()
    #     canvas = canvas.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     self.label.setPixmap(canvas)

class TrainModelDialog(QWidget):
    def __init__(self, View):
        super().__init__()   
        
        self.View = View
        self.Controller = self.View.Controller
        
        self.initUI()

    def initUI(self):
    ### Set up the browser here
        self.text_browser = QTextBrowser()
        self.text_browser.setAcceptRichText(True)
        self.text_browser.setContextMenuPolicy(Qt.CustomContextMenu)


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
        self.download_btn = QPushButton('&Download MNIST', self)
        #self.select_model_btn = QPushButton('Select Model', self)   # This is a place holder button
        self.load_model_btn = QPushButton('Load Model', self)       # This is a place holder
        self.train_btn = QPushButton('&Train', self)
        self.cancel_btn = QPushButton('&Cancel', self)
            # One of the button is a combo box so we define it here
            # This combo box has 2 options, 1 to select the MLP model, 1 for the CNN model
            # We select the CNN Model by default...
        self.select_model_cbb1 = QComboBox(self)

        self.select_model_cbb1.addItem('CNN Model')

        self.select_model_cbb1.addItem('MLP Model')
        

    ############# Configuring the initial states of all of the buttons
        #self.download_btn.setCheckable(True)

        self.select_model_cbb1.setEnabled(False)
        self.load_model_btn.setEnabled(False)
        self.train_btn.setEnabled(False)
        #self.cancel_btn.setCheckable(True)


        self.download_btn.clicked.connect(self.Controller.start_worker_1_download)
        #self.download_btn.clicked.connect(self.Controller.downloadDialog)   # This signal need to be moved to somewhere too, not here
        self.load_model_btn.clicked.connect(self.Controller.load_model_control)
        self.train_btn.clicked.connect(self.Controller.start_worker_1_train)
        self.train_btn.clicked.connect(self.Controller.start_worker_2_train)
        #self.train_btn.clicked.connect(self.Controller.trainDialog)        #Turn this off for testing purpose

        self.cancel_btn.clicked.connect(self.Controller.stop_worker_1)
        self.cancel_btn.clicked.connect(self.Controller.stop_worker_2)


    #hbox for all the buttons
        hbox = QHBoxLayout()
        #hbox.addStretch(0)
        hbox.addWidget(self.download_btn)
        hbox.addWidget(self.select_model_cbb1)
        hbox.addWidget(self.load_model_btn)
        hbox.addWidget(self.train_btn)
        hbox.addWidget(self.cancel_btn)

    #hbox for the progress bar!
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.pbar)
        hbox2.addWidget(self.plabel)
      
        vbox  = QVBoxLayout()
        #vbox.addStretch(4)
        vbox.addWidget(self.text_browser)
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
        #self.show()

    

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

            copyAction = QAction("Copy", self)
            copyAction.setStatusTip('Copy text')
            copyAction.triggered.connect(self.text_browser.copy)
            copyAction.setShortcut('Ctrl+Q')

            self.menu.addAction(copyAction)


            self.menu.popup(QCursor.pos())

            
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


class ViewImages(QMainWindow):
    def __init__(self, View):
        super().__init__()   
        self.View = View
        self.Controller = self.View.Controller
        
        self.initUI()

    def initUI(self):

        ### Initiliase the layout of the ViewImages Window
             ## create custom widget for the tabs and assign as the central widget
        self.tab_widget = viewImagesTabs(self)
        self.setCentralWidget(self.tab_widget)

        self.setWindowTitle('View Model Images')
        self.setGeometry(300, 300, 600, 400)
        self.centre()
   
    

    ###We can define the centre of the dialog here, may be centre of the screen or centre of the current app???
    def centre(self): 
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 


## subclass for the tab widget
class viewImagesTabs(QWidget):
    def __init__(self, View):
        super().__init__()
        self.View = View
        self.Controller = self.View.Controller 

        ## assign to a vbox layout. doesnt really matter as long as there is some layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)
       
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.view_train_images = ViewTrainImages(self)
        self.view_test_images = ViewTestImages(self)
     
        ## add tabs to widget by calling tab init functions, allowing us to easily customise tabs
        index = self.tabs.addTab(self.view_train_images, "Training Images")
        index1 = self.tabs.addTab(self.view_test_images, "Testing Images")
        ## addd tab widget to the layout to display it
        vbox.addWidget(self.tabs)

    ## init the first tab
    def TrainImagesUI(self):
        ## create widget and assign to a layout
        TrainImageTab = QWidget()
        layout = QVBoxLayout()
        TrainImageTab.setLayout(layout)
        ## add example text change this as needed
        self.label = QLabel()
        #label.setText("Example Text")
        #lbl_img.setPixmap(pixmap)
        self.label.setPixmap(QPixmap("Figure.png"))
        layout.addWidget(self.label)

        ### Return the tab widget!
        return TrainImageTab


    def TestImagesUI(self):
        ## create widget and assign to a layout
        TestImageTab = QWidget()
        layout = QVBoxLayout()
        TestImageTab.setLayout(layout)
        ## add example text change this as needed
        label = QLabel()
        label.setText("Example Text")
        layout.addWidget(label)

        ### Return the tab widget!
        return TestImageTab

class ViewTrainImages(QLabel):
    def __init__(self, View):
        super().__init__()
        self.View = View
        self.Controller = self.View.Controller 

        self.initUI()

    def initUI(self):  
    #First, define the label
        self.view_train_img = QLabel()
        self.view_train_img.setPixmap(QPixmap('Figure_1.png'))     #Test load

    #Second, define the ScrollArea
        # self.scroll_area = QScrollArea(self)
        # self.scroll_area.setWidget(self.view_train_img)


    #Then, define the buttons we want to use
        self.next_btn = QPushButton('&Next', self)
        self.prev_btn = QPushButton('&Prev', self)

        self.next_btn.clicked.connect(self.Controller.train_next_page)
        self.prev_btn.clicked.connect(self.Controller.train_prev_page)

        # self.test_btn1 = QPushButton('Test', self)
        # self.test_btn2 = QPushButton('Test 2', self)

    #hbox for all the buttons
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.prev_btn)
        hbox.addWidget(self.next_btn)

    #hbox for the main layout
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.view_train_img)
        

        ### vbox inside hbox2
        mini_vbox = QVBoxLayout()
        # mini_vbox.addWidget(self.test_btn1)
        # mini_vbox.addWidget(self.test_btn2)
        mini_vbox.addStretch(5)

        hbox2.addLayout(mini_vbox)


        vbox  = QVBoxLayout()

        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)   

        ## update the image each time button is clicked
    def update_image(self, index):
        self.view_train_img.clear()
        img = QPixmap('cache/train_set/mnist_cache_' + str(index) +'.png')
        self.view_train_img.setPixmap(img)
        self.update()


class ViewTestImages(QLabel):
    def __init__(self, View):
        super().__init__()
        self.View = View
        self.Controller = self.View.Controller 

        self.initUI()

    def initUI(self):  
    #First, define the label
        self.view_test_img = QLabel()
        self.view_test_img.setPixmap(QPixmap('Figure_1.png'))     #Test load

    #Second, define the ScrollArea
        # self.scroll_area = QScrollArea(self)
        # self.scroll_area.setWidget(self.view_train_img)


    #Then, define the buttons we want to use
        self.next_btn_test = QPushButton('&Next', self)
        self.prev_btn_test = QPushButton('&Prev', self)

        self.next_btn_test.clicked.connect(self.Controller.test_next_page)
        self.prev_btn_test.clicked.connect(self.Controller.test_prev_page)


    #hbox for all the buttons
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.prev_btn_test)
        hbox.addWidget(self.next_btn_test)

    #hbox for the main layout
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.view_test_img)
        

        ### vbox inside hbox2
        mini_vbox = QVBoxLayout()

        mini_vbox.addStretch(5)

        hbox2.addLayout(mini_vbox)


        vbox  = QVBoxLayout()

        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)   


    def update_image(self, index):
        self.view_test_img.clear()
        img = QPixmap('cache/test_set/mnist_cache_' + str(index) +'.png')
        self.view_test_img.setPixmap(img)
        self.update()