import sys
import yaml
from git import Repo
from actions import create_new_branch, switch_branch

if __name__ == '__main__':
    try:
        repo = Repo('.')

        with open('config.yml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)

        if sys.argv[1] == 'create':
            create_new_branch(repo, config)
        elif sys.argv[1] == 'switch':
            switch_branch(repo, config)
        else:
            print("No such command")
    except KeyError:
        print("Done.")
