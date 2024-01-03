
import random
import time
import sys

def print_progress_dots(num_dots, delay=.1):
    for _ in range(num_dots):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(delay)
        
    print()
