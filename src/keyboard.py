from inputs import get_key
import math
import threading

class KeyboardController(object):

    def __init__(self):
        self.direction = 0
        self.speed = 0
        self.forward = 0
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self):
        b = 0
        if self.forward() == 1:
            b = self.speed/10
        return [self.direction, b]

    def change_speed(self, s):
        self.speed = max(0,self.speed+s)
        self.speed = min(10,self.speed+s)

    def _monitor_controller(self):
        while True:
            events = get_key()
            for event in events:
                if event.code == 'KEY_RIGHTSHIFT':
                    self.forward = event.state
                elif event.code == 'KEY_RIGHTALT':
                    self.direction = event.state * -1
                elif event.code == 'KEY_RIGHTMETA':
                    self.direction = event.state
                elif event.code == 'KEY_LEFTSHIFT':
                    self.change_speed(event.state)
                elif event.code == 'KEY_FN':
                    self.change_speed(event.state*-1)