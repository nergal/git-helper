# -*- coding: utf-8 -*-
from PyInquirer import prompt
from .common import get_current_branch, ask_confirm, switch_to_branch


def choose_branch_name(repo):
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


def switch_branch(repo):
    current_branch = get_current_branch(repo)
    print("Current branch is %s" % current_branch)

    branch_name = choose_branch_name(repo)

    if ask_confirm('Do you want to switch to %s' % branch_name):
        switch_to_branch(branch_name, False)

    print("Switched to branch %s" % branch_name)
