'''
Handwritten Digit Recognizer
This is the CONTROLLER of the application

Authors : Dexter Pham and Arathi Biju

Semester 1 2021

'''
import sys
import time
import os

from PyQt5.QtWidgets    import QApplication
from PyQt5.QtCore       import QThread, pyqtSignal, QObject, Qt 
from torchvision        import datasets, transforms, models
from matplotlib         import pyplot

from PyQt5.QtWidgets import *
from PyQt5.QtCore   import *
from PyQt5.QtGui    import *

from model import Model
from view import View


class Controller(QObject):
    def __init__(self):
        ## set up controller object that manages and runs the code
        super(Controller, self).__init__()
        self.dir_init()

        self.current_value_train = -1
        self.current_value_test = -1
        ## add the Model and View classes to the controller 
        self.Model = Model()
        self.View = View(self)
        self.thread = {}

        #set up the thread class
        self.thread[1] = ThreadClass(self, index = 1)
        self.thread[2] = ThreadClass(self, index = 2)

    def main (self):
        self.View.main()
        self.enable_train_btn()
        self.load_complete_flag = False
        #self.send_command()
        
        ##self.Model.download_data()

    def dir_init(self):
        if os.path.isdir('cache/train_set'):
            pass
        else:  
            os.mkdir('cache/train_set')

        if os.path.isdir('cache/test_set'):
            pass
        else:  
            os.mkdir('cache/test_set') 
        
    ## these functions call the coresponding functions in the View class and maintain the MVC pattern
    ## Functions are related to the Train Dialog Window
    def show_train_images_view(self):   self.View.train_images_view.show()
    def show_train_dialog(self):        self.View.dialog_view.show()
    def disable_train_btn(self):        self.View.dialog_view.train_btn.setEnabled(False) 
    def disable_download_btn(self):     self.View.dialog_view.download_btn.setEnabled(False)
    def enable_download_button(self):   self.View.dialog_view.download_btn.setEnabled(True) 
    def enable_combo_box(self):         self.View.dialog_view.select_model_cbb1.setEnabled(True)
    
    def enable_train_btn(self):
        if self.Model.data_available == True: self.View.dialog_view.train_btn.setEnabled(True)
    def enable_load_button(self):
        if self.Model.data_available == True: self.View.dialog_view.load_model_btn.setEnabled(True)
    def pbar_update_slot(self, msg):
        self.View.dialog_view.pbar.setValue(int(msg))
        if self.View.dialog_view.pbar.value() ==  self.View.dialog_view.pbar.maximum(): 
            self.View.dialog_view.pbar.setValue(self.View.dialog_view.pbar.maximum())
        
    ## sets up progress bar for displaying training progress
    def pbar_train_mode(self):
        self.View.dialog_view.pbar.setMinimum(0)
        total_steps =int(60000  * (self.Model.epoch_range - 1)) 
        self.View.dialog_view.pbar.setMaximum(total_steps)

    ## reset progress bar 
    def reset_pbar(self):
        self.View.dialog_view.pbar.setValue(0)

    def downloadDialog(self): self.View.dialog_view.text_browser.append("Downloading MINST dataset..")
    def trainDialog(self):  self.View.dialog_view.text_browser.append("Training....")

## when download is complete enable train, load and combo box as display confirmation text
    def message_download_complete(self):
        if self.thread[1].complete == True:
            self.thread[1].disconnect()
            self.View.dialog_view.text_browser.append('Download Complete! MNIST Dataset is available')
            self.enable_train_btn()
            self.enable_download_button()
            self.enable_load_button()
            self.enable_combo_box()
            time.sleep(0.1)
        else:
            self.View.dialog_view.text_browser.append('Download Cancelled')
            self.enable_download_button()

## when training complete display confirmation text
    def message_training_complete(self):
        self.thread[1].disconnect()
        if self.thread[1].complete == True:
            self.View.dialog_view.text_browser.append('Training Complete! Model is ready to load and use')
            self.View.dialog_view.text_browser.append('Training accuracy is ' + str(self.Model.current_accuracy / 100) + '%')
        else:
            self.View.dialog_view.text_browser.append('Training Cancelled')

    
    def clearDialog(self): self.View.dialog_view.text_browser.clear()
    def show_images_view(self): self.View.view_images.show()


    ### below functions relate to the view images tab
    def train_next_page (self):
        #for i in range(0 ,11):
        self.current_value_train += 1
        self.load_image(self.current_value_train)

    def train_prev_page (self):
        self.current_value_train -= 1
        if self.current_value_train <= -1: 
            self.current_value_train = -1 
        else:
            
            self.load_image(self.current_value_train)
            #self.View.view_images.tab_widget.view_train_images.update_image()


    def test_next_page (self):
        self.current_value_test += 1
        self.load_image_test(self.current_value_test)

    def test_prev_page (self):
        self.current_value_test -= 1
        if self.current_value_test <= -1: 
            self.current_value_test = -1 
        else: 
            self.load_image_test(self.current_value_test)
    
    def load_image(self, index):

        if os.path.isfile('cache/train_set/mnist_cache_' + str(index) + '.png'):
            self.View.view_images.tab_widget.view_train_images.update_image(index)
        else:
        
            start = time.time()
            fig, axis = pyplot.subplots(10, 10, figsize=(4, 4)) 
            self.batch_train = index * 100
            x = 0
            current_batch = 0
            for i in range (0, 59999):
                labels = self.Model.train_dataset[i][1]
 
                if (labels !=10 and current_batch >= self.batch_train and current_batch < (self.batch_train + 100)):
                    print(current_batch)
                    print(self.batbatch_trainch)
                   
                    if (labels !=10 and x<100):
                        pyplot.subplot(10, 10, x+1)
                        pyplot.axis('off')
                        img = self.Model.train_dataset[i][0]
                        pyplot.imshow(img.reshape(28,28), cmap=pyplot.get_cmap('binary'))
                        x += 1

                current_batch += 1
            pyplot.savefig('cache/train_set/mnist_cache_' + str(index) +'.png')
            pixmap = QPixmap("Testiferror.png")      # Load a pixmap here, need place to store it
            
            #self.View.view_images.tab_widget.view_train_images.clear()
            #self.View.view_images.tab_widget.view_train_images.setPixmap(pixmap)
            self.View.view_images.tab_widget.view_train_images.update_image(index)
            end = time.time()

            print(f'it took {end - start} sec to make an image.')

    def load_image_test(self, index):

        if os.path.isfile('cache/test_set/mnist_cache_' + str(index) + '.png'):
            self.View.view_images.tab_widget.view_test_images.update_image(index)
        else:
        
            start = time.time()
            fig, axis = pyplot.subplots(10, 10, figsize=(4, 4))
            self.batch = index * 100
            x = 0
            current_batch = 0
            for i in range (0, 9999):
                labels = self.Model.test_dataset[i][1]
                if (labels !=10 and current_batch >= self.batch and current_batch < (self.batch + 100)):
                    print(current_batch)
                    print(self.batch)
                    #if(x <100):
                    if (labels !=10 and x<100):
                        pyplot.subplot(10, 10, x+1)
                        pyplot.axis('off')
                        img = self.Model.test_dataset[i][0]
        
                        pyplot.imshow(img.reshape(28,28), cmap=pyplot.get_cmap('binary'))
                        x += 1

                current_batch += 1
            pyplot.savefig('cache/test_set/mnist_cache_' + str(index) +'.png')
            pixmap = QPixmap("Testiferror.png")      # Load a pixmap here, need place to store it
            
            #self.View.view_images.tab_widget.view_train_images.clear()
            #self.View.view_images.tab_widget.view_train_images.setPixmap(pixmap)
            self.View.view_images.tab_widget.view_test_images.update_image(index)
            end = time.time()

            print(f'it took {end - start} sec to make an image.')
            
    ## implements load button functionality
    def load_model_control(self): 
        self.Model.load_model()
        self.View.dialog_view.text_browser.append('Loading Complete!')
        # We need a state_dict for this line:
        #self.View.dialog_view.text_browser.append('The loaded model has the training accuracy of ' + str(self.Model.current_accuracy / 100) + '%')

        self.load_complete_flag = True
        self.View.main_view.recognizeButton.setEnabled(True)

    ## calls the process images function from model when recognize is clicked
    def process_images_control(self): 
        self.Model.process_images()
        self.View.main_view.resetGraph()
        self.View.main_view.resetText(self.Model.current_digit)


    ##############################     WORKER  #################################################################
    ############################################################################################################
    ## Below functions and classes relate to the multithreading required for the downloading, training 
    # and progress bar implementation
    """ (All model related tasks are heavy; Hence, we offload it into worker_1
        to make the main UI more responsive )"""

    # starts the download and disables the train and download buttons untill download complete
    def start_worker_1_download(self):
        self.thread[1].set_task("download")
        self.thread[1].complete = False
        self.thread[1].started.connect(self.downloadDialog)
        self.thread[1].finished.connect(self.message_download_complete)
        self.disable_train_btn()
        self.disable_download_btn()
        self.thread[1].start()

    # starts the train thread and sends signals to update progress bar
    def start_worker_1_train(self):
        self.pbar_train_mode()
        self.thread[1].set_task("train")
        self.thread[1].complete = False
        self.thread[1].started.connect(self.pbar_train_mode)
        self.thread[1].started.connect(self.trainDialog)
        
        self.thread[1].finished.connect(self.message_training_complete)
        self.thread[1].start()
    
        self.View.dialog_view.train_btn.setEnabled(False)
       

    def stop_worker_1(self):
        self.thread[1].stop()
        self.enable_train_btn()

    
    """ Worker 2 is used to poll the steps for the progress bar"""
        
    def start_worker_2_train(self):
        self.thread[2].set_task("train")
        self.thread[2].pbar_signal.connect(self.pbar_update_slot)
        self.thread[2].start()
        
    def stop_worker_2(self):
        self.thread[2].stop()
        self.Model.progress = 0
        self.reset_pbar()
        ##self.completed_training_dialog()


## class object for QThread to implement the multithreading
class ThreadClass(QThread):
    pbar_signal = pyqtSignal(int)
    data_available_signal = pyqtSignal(int)
    def __init__(self, Controller, index = 0):
        super(ThreadClass, self).__init__()
            # Here we are passing the MVC classes for multithreading
            # Operations related to the Model will be processed here in the background
        self.Model = Controller.Model
        self.View = Controller.View
        self.Controller = Controller
        
        self.is_running = True
        self.index = index
        self.complete = False
    def run(self):

            ## The run command will select the operation based on the self.task that we passed
            ## download : download the dataset
            ## train    : train the model
            ## test     : test the model
            ## validate : validate the model --- validate means we use our own digits, not from the MNIST dataset
        
        if self.index==1:
            if self.task == "download" :
                self.Model.download_data()
                self.complete = True

            elif self.task == "train": 
                self.Model.main() 
                self.complete = True

            elif self.task == "test":  
                time.sleep(5)

            elif self.task == "validate":  
                time.sleep(5)
            

        elif self.index==2:
            if self.task == "train":
                step = 0 
                while step < self.Controller.View.dialog_view.pbar.maximum():
                    step = self.Model.progress
                    time.sleep(0.1)
                    self.pbar_signal.emit(self.Model.progress)
                


    def stop(self):
        self.is_running = False
        self.terminate()
        
    def set_task(self, task): self.task = task
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Controller()
    my_app.main()
    sys.exit(app.exec_())
