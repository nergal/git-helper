# -*- coding: utf-8 -*-
from PyInquirer import prompt
from git import Repo, exc

repo = Repo('.')


def choose_branch_name():
    choises = list(map(lambda x: x.name, repo.heads))

    questions = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Choose a task for branch source',
            'choices': choises
        },
    ]
    answers = prompt(questions)
    return answers['task']


def get_current_branch():
    active_branch = repo.active_branch
    return active_branch.name


def ask_confirm(msg):
    answers = prompt({
        'type': 'confirm',
        'message': msg,
        'name': 'confirm',
        'default': True,
    })

    return answers['confirm']


def switch_to_branch(branch_name, new=False):
    if not repo.is_dirty():
        try:
            if new:
                try:
                    repo.git.branch(branch_name)
                except exc.GitCommandError as err:
                    print(err)
                finally:
                    repo.git.checkout(branch_name)
            else:
                repo.git.checkout(branch_name)
        except exc.GitError as err:
            print(err)

        return True
    raise EnvironmentError('Cannot switch, repo is dirty')


def switch_branch():
    current_branch = get_current_branch()
    print("Current branch is %s" % current_branch)

    branch_name = choose_branch_name()

    if ask_confirm('Do you want to switch to %s' % branch_name):
        switch_to_branch(branch_name, False)

    print("Switched to branch %s" % branch_name)
