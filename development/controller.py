# ##
# This is the CONTROLLER of the application
# ##
import sys
import time
from PyQt5.QtWidgets    import QApplication
from PyQt5.QtCore       import QThread, pyqtSignal 
from torchvision import datasets, transforms, models


from model import Model
from view import View


class Controller():
    def __init__(self):
        super().__init__()

        self.random_value = 6
        
        self.Model = Model()
        self.View = View(self)
        self.thread = {}

        self.thread[1] = ThreadClass(self, index = 1)
        self.thread[2] = ThreadClass(self, index = 2)

    def main (self):
        print('This is the controller')
        self.View.main()
        self.activate_train_btn()
        #self.send_command()
        #print(self.View.ex1)
        
        ##self.Model.download_data()
        

    def show_train_dialog(self): self.View.dialog_view.show()
    def show_images_view(self): 
        self.View.view_images.show()
        self.View.view_images_tabs.tabs.setCurrentIndex(1)
        print("pls work")

    def disable_train_btn(self): self.View.dialog_view.train_btn.setEnabled(False)    

    def activate_train_btn(self):
        #print(self.Model.data_available)
        if self.Model.data_available == True: self.View.dialog_view.train_btn.setEnabled(True)

    def pbar_update_slot(self, msg):
        self.View.dialog_view.pbar.setValue(int(msg))
        if self.View.dialog_view.pbar.value() ==  self.View.dialog_view.pbar.maximum():   
            self.View.dialog_view.pbar.setValue(self.View.dialog_view.pbar.maximum())

    def pbar_train_mode(self):
        self.View.dialog_view.pbar.setMinimum(0)
        total_steps =int(60000  * (self.Model.epoch_range - 1)) 
        self.View.dialog_view.pbar.setMaximum(total_steps)

    def reset_pbar(self):
        self.View.dialog_view.pbar.setValue(0)

    ######## DIALOG UI STUFF HERE#########
    def downloadDialog(self):
        self.View.dialog_view.text_brower.append("Downloading MINST dataset, please wait for server to respond")
    

    def trainDialog(self):
        self.View.dialog_view.text_brower.append("Training....")
    

    def clearDialog(self):
        print("inside this function")
        self.View.dialog_view.text_brower.clear()
        
        ################.................

    ### THIS IS THE PLACE WHERE WE DO MOST OF THE THINGS
    #def send_command(self):
        #self.view.set_commands('aaa')

        # self.view.train_btn.setCheckable(False)
        # self.view.self.download_btn.setEnabled(False)
        # self.view.cancel_btn.setEnabled(False)
        #self.view.train_btn.clicked.connect(enable_button)

    # def enable_train_btn(self):
    #     # print("haha it's connected ")
    #     # print('we are inside the controller class!')
    #     # self.Model.download_data()
    #     if self.View.ex1.download_btn.isChecked():
    #         self.View.ex1.train_btn.setEnabled(True)
    #         time.sleep(50000)
            
    #     else:
    #         pass
    #         self.View.ex1.train_btn.setEnabled(False)  


    ##############################     WORKER  #################################################################
    ############################################################################################################
    """ All model related tasks are heavy; Hence, we offload it into worker_1
        to make the main UI more responsive """

    def start_worker_1_download(self):
        self.thread[1].set_task("download")
        self.thread[1].start()
        
        #self.thread[1].any_signal.connect(self.download_function)
        self.View.dialog_view.download_btn.setEnabled(False)
    
    def start_worker_1_train(self):
        self.pbar_train_mode()
        self.thread[1].set_task("train")
        #self.thread[1].started.connect(self.pbar_train_mode)
        
        self.thread[1].start()
        

        print(self.View.dialog_view.pbar.maximum())
        #self.thread[1].started.connect(self.start_worker_2_train)
        self.View.dialog_view.train_btn.setEnabled(False)

    def stop_worker_1(self):
        self.thread[1].stop()

        self.View.dialog_view.download_btn.setEnabled(True)
    
    """ Worker 2 is reserved for future features"""

    """ The future is a bit sooner than expected"""
    """ but yea we use worker_2 to poll the steps for the progress bar
        This method is not very accurate and it may not be a good practice
        to use two threads operate on the same instance of an object """

    """ One way to overcome this issue is to make the Controller visible to 
        the Model but then it may not comply MVC... 
        Speaking of MVC, everyone has their own view but it's another story... """
        

    def start_worker_2_train(self):
        print('trying to start thread 2')
        self.thread[2].set_task("train")
        
        self.thread[2].start()
        self.thread[2].pbar_signal.connect(self.pbar_update_slot)
        
        
        

    def stop_worker_2(self):
        self.thread[2].stop()
        self.reset_pbar()
        self.Model.progress = 0


    ##############################################################################################################
    ##############################################################################################################

class ThreadClass(QThread):
    pbar_signal = pyqtSignal(int)
    def __init__(self, Controller, index = 0):
        super(ThreadClass, self).__init__()
            # Here we are passing the MVC classes for multithreading!!!
            # Operations related to the Model will be processed here in the background
        self.Model = Controller.Model
        #self.View = Controller.View
        self.Controller = Controller
        
        self.is_running = True
        self.index = index

    def run(self):
        # print('Starting Thread')
        # print(self.Controller)

            ## The run command will select the operation based on the self.task that we passed
            ## download : download the dataset
            ## train    : train the model
            ## test     : test the model
            ## validate : validate the model --- validate means we use our own digits, not from the MNIST dataset
        
        if self.index==1:
                ## Ohhh no!!! Python no case-switch, a dict might be hard to read...
            if self.task == "download" :
                
                self.Controller.disable_train_btn()
            ##    self.Controller.thread[2].start()
                self.Model.download_data()
                #self.download_dataset()
                self.Controller.activate_train_btn()

            elif self.task == "train":  
                self.Model.main()
                

            elif self.task == "test":  
                time.sleep(5)

            elif self.task == "validate":  
                time.sleep(5)
            
            
            

            print('closing thread 1')

        elif self.index==2:
            #self.Controller.something()

            if self.task == "train":
                step = 0 
                while step < self.Controller.View.dialog_view.pbar.maximum():
                    # print('check if thead 2 still alive')
                    print(self.Controller.View.dialog_view.pbar.value())
                    step = self.Model.progress
                    print(step)
                    time.sleep(0.1)
                    self.pbar_signal.emit(self.Model.progress)
                

            
            # print(self.Controller.thread)
            # print('starting thread 1') 
            # print(self.task)   
            # self.Model.download_data()
            
            #self.View.dialog_view.cancel_btn.click()
            #self.finished.connect(self.Controller.stop_worker_1)
            
            #self.View.dialog_view.download_btn.setEnabled(True)
            
            #########self.finished.connect(self.Controller.activate_train_btn)

        # elif self.index==2:
        #     print('starting thread 2')
            
        #     time.sleep(50000)

        # elif self.index==3:
        #     time.sleep(2)

    def stop(self):
        self.is_running = False
        print('Stopping Thread')
        self.terminate()
        
    def set_task(self, task): self.task = task
        
    def download_dataset(self):
        try:
            train_dataset = datasets.MNIST(root='mnist_data/', train=False, download=True)
            print('The shit is completed')
        except:
            print('The server is not very responsive, trying to reconnect')
            time.sleep(2)
            self.download_dataset()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Controller()
    my_app.main()
    sys.exit(app.exec_())
