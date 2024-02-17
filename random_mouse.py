# pyinstaller --onefile .\random_mouse.py
# py -m pip install pyinstaller

import random
import time
from pynput.mouse import Button, Controller
from threading import Thread, Event, Lock
import webbrowser
from screeninfo import get_monitors

ORGIN_EXIT_BTN_X = 1890
ORGIN_EXPAND_BTN_X = 1847
ORGIN_MIN_BTN_X = 1805

SCREEN_BTNS_Y = 9

# Get all monitors
monitors = get_monitors()

mouse = Controller()

# Print the number of monitors and their resolutions
print(f"Number of monitors: {len(monitors)}")
for i, monitor in enumerate(monitors):
   print(f"Monitor {i}: {monitor.width}x{monitor.height} at {monitor.x},{monitor.y}")

move_lock = Lock()

def move_random(kill_evt):
   ''''''
   while(not kill_evt.wait(1)):
      wait = random.randint(10, 30)
      time.sleep(wait)

      screen = random.randint(0, len(monitors)-1)
      monitor = monitors[screen]

      if(monitor.x < 0):
         x_pos = random.randint(monitor.x, 0)
      else:
         x_pos = random.randint(0, monitor.x)

      y_meas = monitor.y+monitor.height
      if(y_meas < 0):
         y_pos = random.randint(y_meas, 0)
      else:
         y_pos = random.randint(0, y_meas)

      print("Getting lock for move")
      try:
         with move_lock:
            print(f"Moving to Screen {screen}: {(x_pos, y_pos)}")
            mouse.position = (x_pos, y_pos)
      except Exception:
         continue


def click_random_screen_btn(kill_evt):
   ''''''
   while(not kill_evt.wait(1)):
      wait = random.randint(30, 40)
      time.sleep(wait)

      screen = random.randint(0, len(monitors)-1)
      monitor = monitors[screen]

      # action = random.randint(0, 2)
      # Not doing exit now. Don't want to close rick rolls
      action = random.randint(1, 2)
      print(f"Action: {action}")
      print("Getting lock for click")
      try:
         with move_lock:
            if(action == 0):
               print(f"Screen {screen}: Exiting")
               mouse.position = (ORGIN_EXIT_BTN_X+monitor.x, SCREEN_BTNS_Y)
            elif(action == 1):
               print(f"Screen {screen}: Expanding")
               mouse.position = (ORGIN_EXPAND_BTN_X+monitor.x, SCREEN_BTNS_Y)
            else:
               print(f"Screen {screen}: Minimizing")
               mouse.position = (ORGIN_MIN_BTN_X+monitor.x, SCREEN_BTNS_Y)
            
            mouse.press(Button.left)
            mouse.release(Button.left)
      except Exception:
         continue

def do_rick_roll(kill_evt):
   while(not kill_evt.wait(1)):
      wait = random.randint(180, 600) # 3 mins to 10 mins
      time.sleep(wait)

      webbrowser.open('https://www.youtube.com/watch?v=eBGIQ7ZuuiU', new = 2)

thd_kill_event = Event()
# move fucntions to threads
random_move_thd = Thread(target=move_random, args=[thd_kill_event])
random_btn_click_thd = Thread(target=click_random_screen_btn, args=[thd_kill_event])
rick_roll_thd = Thread(target=do_rick_roll, args=[thd_kill_event])

random_move_thd.start()
random_btn_click_thd.start()
rick_roll_thd.start()

try:
   while(True):
      # wating for ctrl+c input
      time.sleep(.1)
except KeyboardInterrupt:
   thd_kill_event.set()
   print("Thread Kill Event Triggered")
   random_move_thd.join()
   print("Move Killed")
   random_btn_click_thd.join()
   print("Click Killed")
   rick_roll_thd.join()
   print("Rick Roll Killed")

   exit()
