
import time
import sys

def print_progress_dots(num_dots, delay=.1):
    for i in range(num_dots):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(delay)
        
    print()


def print_progress_loader():
    max_dots = 20
    for i in range(1, max_dots + 1):
        print('.' * i, end='\r')
    for i in range(max_dots - 1, 0, -1):
        print('.' * i, end='\r')
    print()
