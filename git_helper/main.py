import sys
from actions import create_new_branch, switch_branch

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'create':
            create_new_branch()
        elif sys.argv[1] == 'switch':
            switch_branch()
        else:
            print("No such command")
    except KeyError:
        print("Done.")
