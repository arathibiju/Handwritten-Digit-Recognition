# ##
# This is the CONTROLLER of the application
# ##
import sys
from PyQt5.QtWidgets    import QApplication
from PyQt5.QtCore       import QThread 

from model import Model
from view import View


class Controller(QThread):
    def __init__(self):
        super().__init__()
        self.random_value = 6

        self.Model = Model()
        self.View = View(self)

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

    def enable_train_btn(self):
        print("haha it's connected ")
        print('we are inside the controller class!')
        self.Model.download_data()
        if self.View.ex1.download_btn.isChecked():
            self.View.ex1.train_btn.setEnabled(True)
            
        else:
            pass
            #self.View.ex1.train_btn.setEnabled(False)  

    def worker(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Controller()
    my_app.main()
    sys.exit(app.exec_())
