import random
import time
from pynput.mouse import Button, Controller
from threading import Thread, Event, Lock
import webbrowser

WHOLE_RES_W = 3840-50
WHOLE_RES_H = 1080-50

SCREEN_1_EXIT_BTN_X = 1890
SCREEN_1_EXPAND_BTN_X = 1847
SCREEN_1_MIN_BTN_X = 1805

SCREEN_2_EXIT_BTN_X = 3817
SCREEN_2_EXPAND_BTN_X = 3770
SCREEN_2_MIN_BTN_X = 3725

SCREEN_BTNS_Y = 9

mouse = Controller()

move_lock = Lock()

def move_random(kill_evt):
   ''''''
   while(not kill_evt.wait(1)):
      wait = random.randint(10, 30)
      time.sleep(wait)

      x_pos = random.randint(0, WHOLE_RES_W)
      y_pos = random.randint(0, WHOLE_RES_H)

      print("Getting lock for move")
      try:
         with move_lock:
            mouse.position = (x_pos, y_pos)
      except Exception:
         continue


def click_random_screen_btn(kill_evt):
   ''''''
   while(not kill_evt.wait(1)):
      wait = random.randint(30, 40)
      time.sleep(wait)

      screen_target = random.randint(1,2)
      action = random.randint(0, 2)

      print("Getting lock for click")
      try:
         with move_lock:
            if(screen_target == 1):
               if(action == 0):
                  mouse.position = (SCREEN_1_EXIT_BTN_X, SCREEN_BTNS_Y)
               elif(action == 1):
                  mouse.position = (SCREEN_1_EXPAND_BTN_X, SCREEN_BTNS_Y)
               else:
                  mouse.position = (SCREEN_1_MIN_BTN_X, SCREEN_BTNS_Y)
            else:
               if(action == 0):
                  mouse.position = (SCREEN_2_EXIT_BTN_X, SCREEN_BTNS_Y)
               elif(action == 1):
                  mouse.position = (SCREEN_2_EXPAND_BTN_X, SCREEN_BTNS_Y)
               else:
                  mouse.position = (SCREEN_2_MIN_BTN_X, SCREEN_BTNS_Y)
            
            mouse.press(Button.left)
            mouse.release(Button.left)
      except Exception:
         continue

def do_rick_roll(kill_evt):
   while(not kill_evt.wait(1)):
      wait = random.randint(180, 1200)
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
