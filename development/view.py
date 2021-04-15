# ##
# This is the view of the application
# ##


class View:
    def __init__(self, controller):
        self.controller = controller


    def main(self):
        print('We are in main of View')