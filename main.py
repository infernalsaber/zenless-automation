from pynput.mouse import Button
from pynput.keyboard import Controller as Key
from random import random

from utils import tsleep, CustomMouse,  CustomKeyboard


mouse = CustomMouse()
keyboard = CustomKeyboard()


def confirm(default=(0, 0)):
    pt = mouse.findPointByImage(candidates=['pics/confirm.png', 'pics/confirm2.png'], default=default, confidence=0.7)
    mouse.goToPointAndClick(pt[0], pt[1], 1)
    tsleep(2)

def initiate_errand():
    keyboard.press(Key.alt)
    tsleep(1.5)
    mouse.slowlyMoveTo(100, 150, 1)
    keyboard.softPress(Key.f2)
        
    
    keyboard.release(Key.alt)
    tsleep(2)
    errand_pt = mouse.findPointByImage(candidates=['pics/errands1.png', 'pics/errands2.png'], default=(973, 148), confidence=0.7)
    mouse.slowlyMoveTo(errand_pt[0], errand_pt[1], 1)
    mouse.click(Button.left)
    tsleep(2)
    mouse.goToPointAndClick(986,834)
    mouse.goToPointAndClick(1121,628) # Teleport

def watch_the_loader(max_time=20, min_time=5):
    elapsed = 0
    while elapsed < max_time:
        tsleep(2)
        pt = mouse.findPointByImage(candidates=['pics/loading.png'], default=(0, 0), confidence=0.7)
        if pt == (0, 0):
            break
        elapsed += 1
    
    if elapsed < min_time:
        tsleep(min_time - elapsed)
    

def coffee():
    # Try one coffee
    initiate_errand()
    watch_the_loader()
    keyboard.softPress('w', hold_time=1)
    keyboard.softPress('f')
    tsleep(2)
    keyboard.softPress('1')
    tsleep(2)
    confirm()

def dinivation():
    # Dinivation
    initiate_errand()
    watch_the_loader()
    keyboard.softPress('f')
    tsleep(4)
    mouse.goToPointAndClick(1500,500)
    tsleep(2)   
    #Dragging
    mouse.press(Button.left)
    for _ in range(7):
        mouse.slowlyMoveTo(400 + random()*50, 500 + random()*50, 1)
        mouse.slowlyMoveTo(900 + random()*50, 500 - random()*50, 1)
    mouse.release(Button.left)
    tsleep(2)
    confirm()
    keyboard.softPress(Key.esc)
    tsleep(2)
    keyboard.softPress(Key.esc)

def store_mgmt():
    # Store Mgmt
    initiate_errand()
    watch_the_loader()
    keyboard.softPress('w', hold_time=1)
    keyboard.softPress('f')
    tsleep(2)
    keyboard.softPress('1')
    tsleep(2)
    if mouse.findPointByImage(candidates=['pics/store_mgmt.png'], default=(0, 0), confidence=0.7) == (0, 0):
        tsleep(2)
        keyboard.softPress(Key.esc)
    
    # Select Character
    tsleep(2)
    pt = mouse.findPointByImage(candidates=['pics/store_mgmt.png'], default=(900, 750), confidence=0.7)
    mouse.goToPointAndClick(pt[0], pt[1])
    
    tsleep(2)
    confirm()
    

    # Select movies
    mouse.goToPointAndClick(1200, 750)
    pt = mouse.findPointByImage(candidates=['pics/store_mgmt_movies.png'], default=(1400, 1030), confidence=0.7)
    mouse.goToPointAndClick(pt[0], pt[1])
    
    tsleep(2)
    mouse.goToPointAndClick(1700, 980)
    tsleep(2)
    confirm()
    confirm()

def collect_rewards():
    # Daily menu
    keyboard.softPress(Key.f2)
    tsleep(2)
    mouse.goToPointAndClick(1571, 275)
    tsleep(2)
    confirm()
    keyboard.softPress(Key.esc)
    
    # City Pass
    keyboard.softPress(Key.f3)
    tsleep(0.5)
    mouse.goToPointAndClick(1500, 50)
    tsleep(2)
    pt = mouse.findPointByImage(candidates=['pics/claim_all2.png'], default=(0, 0), confidence=0.7)
    if pt != (0, 0):
        mouse.goToPointAndClick(pt[0], pt[1])
        tsleep(2)
        keyboard.softPress(Key.esc)

def boot_application():
    
    key_pos = '1'
    keyboard.holdKey([Key.cmd, key_pos], hold_time=0.4)
    tsleep(5)
    keyboard.softPress(Key.left)
    tsleep(0.5)
    keyboard.softPress(Key.enter)
    tsleep(10)
    mouse.goToPointAndClick(950, 900)
    tsleep(10)
    mouse.goToPointAndClick(950, 900)
    tsleep(5)
    watch_the_loader()
    

def main():
    tsleep(5, desc="Starting in") 
    
    # boot_application()
    coffee()
    dinivation()
    store_mgmt()
        
    collect_rewards()

    # some verification goes here, maybe eventually
    # ----

    tsleep(5, desc="Closing in")
    keyboard.holdKey([Key.alt, Key.f4], hold_time=0.4)
    

if __name__ == "__main__":
    main()
    
