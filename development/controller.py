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
        # self.thread[2] = ThreadClass(self, index = 2)

    def main (self):
        print('This is the controller')
        self.View.main()
        self.activate_train_btn()
        #self.send_command()
        #print(self.View.ex1)
        
        ##self.Model.download_data()
        

    def show_train_dialog(self):
        self.View.dialog_view.show()

    def activate_train_btn(self):
        #print(self.Model.data_available)
        if self.Model.data_available == True: self.View.dialog_view.train_btn.setEnabled(True)

    def disable_train_btn(self):
        self.View.dialog_view.train_btn.setEnabled(False)


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
        to make the main UI more responsive"""

    def start_worker_1_download(self):
        self.thread[1].set_task("download")
        self.thread[1].start()
        #self.thread[1].any_signal.connect(self.download_function)
        self.View.dialog_view.download_btn.setEnabled(False)
    
    def start_worker_1_train(self):
        self.thread[1].set_task("train")
        self.thread[1].start()
        self.View.dialog_view.train_btn.setEnabled(False)

    def stop_worker_1(self):
        self.thread[1].stop()
        
        
        self.View.dialog_view.download_btn.setEnabled(True)
    
    """ Worker 2 is reserved for future features"""
    # def start_worker_2(self):
    #     self.thread[2].start()
    
    # def stop_worker_2(self):
    #     self.thread[2].stop()


    ##############################################################################################################
    ##############################################################################################################

class ThreadClass(QThread):
    any_signal = pyqtSignal(int)
    def __init__(self, Controller, index = 0):
        super(ThreadClass, self).__init__()
            # Here we are passing the MVC classes for multithreading!!!
            # Operations related to the Model will be processed here in the background
        self.Model = Controller.Model
        self.View = Controller.View
        self.Controller = Controller
        
        self.is_running = True
        self.index = index

    def run(self):
        # print('Starting Thread')
        # print(self.Controller)

            ## The run command will select the operations based on the self.task that we passed
            ## download : download the dataset
            ## train    : train the model
            ## test     : test the model
            ## validate : validate the model --- validate means we use our own digits, not from the MNIST dataset
        
        if self.index==1:
                ## Ohhh no!!! Python no case-switch, a dict might be hard to read...
            if self.task == "download" :
                self.Controller.disable_train_btn()
                self.Model.download_data()
                self.Controller.activate_train_btn()

            elif self.task == "train"    :  
                self.Model.main()
                time.sleep(5)

            elif self.task == "test"     :  
                time.sleep(5)

            elif self.task == "validate" :  
                time.sleep(5)
            
            # print(self.Controller.thread)
            # print('starting thread 1') 
            # print(self.task)   
            # self.Model.download_data()
            
            #self.View.dialog_view.cancel_btn.click()
            #self.finished.connect(self.Controller.stop_worker_1)
            print('closing thread 1')
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
        
    def set_task(self, task):
        self.task = task

    def download_dataset(self):
        try:
            train_dataset = datasets.MNIST(root='mnist_data/', download=True)
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
