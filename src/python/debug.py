from time import sleep
import sys

def interactive_debugging_mode():
    print('starting in interactive debugging mode...')
    print(' '.join(sys.argv))
    while True:
        print('sleeping 60 seconds...')
        sleep(60)
        pass
    pass

if __name__ == '__main__':
    interactive_debugging_mode()
    pass 
