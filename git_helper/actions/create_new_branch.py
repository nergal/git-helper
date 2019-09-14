# -*- coding: utf-8 -*-
from PyInquirer import prompt, Separator
from jira import JIRA
from .common import get_current_branch, ask_confirm, switch_to_branch


def choose_branch_name(jira):
    issues = jira.search_issues(
        'status != Done AND assignee in (currentUser()) ORDER BY priority DESC, updated DESC'
    )
    choises = list(map(lambda issue: '%s - %s' % (issue.key, issue.fields.summary), issues))
    choises.extend([Separator(), 'Add custom branch'])

    questions = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Choose a task for branch source',
            'choices': choises
        },
        {
            'type': 'list',
            'name': 'branch_type',
            'message': 'Branch type',
            'choices': [
                'Feature',
                'Bugfix',
                'Hotfix',
                'Release'
            ],
            'when': lambda x: x['task'] != 'Add custom branch'
        },
        {
            'type': 'input',
            'name': 'branch_name',
            'message': 'Enter a branch name',
            'when': lambda x: x['task'] == 'Add custom branch'
        }
    ]
    answers = prompt(questions)

    if 'branch_name' in answers.keys():
        return answers['branch_name']
    else:
        return '%s/%s' % (answers['branch_type'].lower(), answers['task'].split(' ', 1)[0])


def create_new_branch(repo, config):
    jira = JIRA(
        config['jira']['host'],
        basic_auth=(config['jira']['username'], config['jira']['token'])
    )

    current_branch = get_current_branch(repo)
    print("Current branch is %s" % current_branch)

    if current_branch != 'develop' and ask_confirm('Do you want to switch to develop?'):
        switch_to_branch(repo, 'develop')

    branch_name = choose_branch_name(jira)

    if ask_confirm('Do you want to switch to %s' % branch_name):
        switch_to_branch(repo, branch_name, True)

    print("Switched to branch %s" % branch_name)
