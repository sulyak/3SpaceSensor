import pyxinput as pyx
from pynput import keyboard

def main():
    print("hello world")
    #pyx.test_virtual()

    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(key))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__": main()