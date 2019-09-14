from git import exc
from PyInquirer import prompt


def get_current_branch(repo):
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


def switch_to_branch(repo, branch_name, new=False):
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
