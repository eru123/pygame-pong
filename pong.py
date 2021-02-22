from window_base import *


class Pong:

    def quit(self):
        print("\n###########################")
        print("  THANK YOU FOR PLAYING!!")
        print("###########################\n")
        sys.exit()

    def run(self):
        while 1:
            pg.display.update()

        self.quit()
