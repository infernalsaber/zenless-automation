from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
from tqdm import tqdm
from time import sleep
import pyautogui
import random
from loguru import logger

def tsleep(t: float, desc: str = ''):
    """A nicer sleep with a bar"""
    if t > 1:
        for _ in tqdm(range(t//1), desc=desc):
            sleep(1)
    sleep(t % 1)


class CustomMouse(Controller):
    """A wrapper around pnyput's controller with some custom qol functionality"""
    
    def slowlyMoveTo(self, x: int, y: int, duration_seconds: float = 2.0):
        """
        Moves the mouse slowly to a target position.
        """
        start_x, start_y = self.position
        steps = 50  # Number of steps to divide the movement into
        
        # Calculate step size
        dx = (x - start_x) / steps
        dy = (y - start_y) / steps
        
        # Small pause between steps
        step_delay = duration_seconds / steps
        
        for _ in range(steps):
            # Move incrementally
            self.move(dx, dy)
            sleep(step_delay)
        
        # Ensure final position is exact
        self.position = (x, y)
    
    def goToPointAndClick(self, x: int, y: int, delay: float = 1.0):
        self.slowlyMoveTo(x, y, delay)
        self.click(Button.left, 1)
        
    def findPointByImage(self, candidates: list =[], default: tuple =(), confidence=0.7) -> tuple:
        
        if not candidates and not default:
            raise ValueError("Either candidates or default must be provided.")
        
        if not candidates:
            return default
        
        for image in candidates:
            try:
                loc = pyautogui.locateOnScreen(image, confidence=confidence)
                if loc:
                    return (loc.left + loc.width // 2, loc.top + loc.height // 2)
            except pyautogui.ImageNotFoundException:
                continue
        return default
        
    
    
class CustomKeyboard(KeyboardController):
    """A wrapper around pnyput's controller with some less qol functionality"""
    
    def softPress(self, key: Key | str, hold_time: float = 0.4):
        self.holdKey([key], hold_time)

    def holdKey(self, keys: list[Key | str], hold_time: float = 2.0):
        for key in keys:
            self.press(key)
        sleep(hold_time)
        for key in keys:
            self.release(key)
    
    def quickPress(self, key: Key | str, hold_time: float = 0.01):
        if hold_time > 1:
            logger.warning("Bruh... quickPress with hold_time > 1s? Randomizing press time ⚠")
            hold_time = random.uniform(0.01, 0.2)
            
        self.holdKey([key], hold_time)