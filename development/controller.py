# ##
# This is the controller of the application
# ##

from view import View

class Controller:
    def __init__(self):
        #self.model = Model()
        self.view = View(self)

    def main (self):
        print('This is the controller')
        self.view.main()



if __name__ == '__main__':
    my_app = Controller()
    my_app.main()

