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

    def main (self):
        print('This is the controller')
        self.View.main()
        #self.send_command()
        #print(self.View.ex1)
        
        ##self.Model.download_data()




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

    def start_worker_1(self):
        self.thread[1] = ThreadClass()
        self.thread[1].start()

        #self.thread[1].any_signal.connect(self.download_function)
        self.View.ex1.download_btn.setEnabled(False)


    def stop_worker_1(self):
        self.thread[1].stop()
        self.View.ex1.download_btn.setEnabled(True)

    # def download_function(self, value):
    #     index = self.sender().index
        
    #     if(value == 1):
    #         self.Model.download_data()
           
    #     else:
    #         pass


class ThreadClass(QThread):
    any_signal = pyqtSignal(int)
    def __init__(self, parent = None, index = 0):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True


    def run(self):
        print('Starting Thread')
        self.downloadtheshit()

    def downloadtheshit(self):
        
        try:
            train_dataset = datasets.MNIST(root='mnist_data/', download=True)

            
        except:
            print('The server is not very responsive, trying to reconnect')
            time.sleep(2)
            self.downloadtheshit()

    def stop(self):
        self.is_running = False
        print('Stopping Thread')
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Controller()
    my_app.main()
    sys.exit(app.exec_())
