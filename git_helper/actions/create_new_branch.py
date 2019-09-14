# -*- coding: utf-8 -*-
from PyInquirer import prompt, Separator
from jira import JIRA
from git import Repo, exc
import yaml

repo = Repo('.')

with open('config.yml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

jira = JIRA(
    config['jira']['host'],
    basic_auth=(config['jira']['username'], config['jira']['token'])
)


def choose_branch_name():
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


def create_new_branch():
    current_branch = get_current_branch()
    print("Current branch is %s" % current_branch)

    if current_branch != 'develop' and ask_confirm('Do you want to switch to develop?'):
        switch_to_branch('develop')

    branch_name = choose_branch_name()

    if ask_confirm('Do you want to switch to %s' % branch_name):
        switch_to_branch(branch_name, True)

    print("Switched to branch %s" % branch_name)
