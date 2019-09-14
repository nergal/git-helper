from git_helper.actions import get_current_branch, ask_confirm, switch_to_branch
from unittest.mock import MagicMock, PropertyMock, patch
from git.exc import GitCommandError
from pytest import raises


def test_switch_to_branch_old():
    mock_repo = MagicMock()
    mock_git = MagicMock()
    mock_checkout = MagicMock()
    mock_branch = MagicMock()
    mock_is_dirty = MagicMock(return_value=False)

    type(mock_repo).git = mock_git
    type(mock_repo).is_dirty = mock_is_dirty
    type(mock_git).checkout = mock_checkout
    type(mock_git).branch = mock_branch

    # !is_dirty, !new -> checkout
    branch_name = 'asdasddd'
    switch_to_branch(mock_repo, branch_name, False)

    mock_checkout.assert_called_with(branch_name)
    mock_branch.assert_not_called()


def test_switch_to_branch_new():
    mock_repo = MagicMock()
    mock_git = MagicMock()
    mock_checkout = MagicMock()
    mock_branch = MagicMock()
    mock_is_dirty = MagicMock(return_value=False)

    type(mock_repo).git = mock_git
    type(mock_repo).is_dirty = mock_is_dirty
    type(mock_git).checkout = mock_checkout
    type(mock_git).branch = mock_branch

    # !is_dirty, new -> branch, checkout
    branch_name = 'ffffffzzzz'
    switch_to_branch(mock_repo, branch_name, True)

    mock_checkout.assert_called_with(branch_name)
    mock_branch.assert_called_with(branch_name)


def test_switch_to_branch_dirty():
    mock_repo = MagicMock()
    mock_git = MagicMock()
    mock_checkout = MagicMock()
    mock_branch = MagicMock()
    mock_is_dirty = MagicMock(return_value=True)

    type(mock_repo).git = mock_git
    type(mock_repo).is_dirty = mock_is_dirty
    type(mock_git).checkout = mock_checkout
    type(mock_git).branch = mock_branch

    # is_dirty -> exception
    branch_name = 'ttttttyyy'
    with raises(EnvironmentError) as exception:
        switch_to_branch(mock_repo, branch_name, True)

    assert exception.type is EnvironmentError
    mock_checkout.assert_not_called()
    mock_branch.assert_not_called()


def test_switch_to_branch_new_exists():
    mock_repo = MagicMock()
    mock_git = MagicMock()
    mock_checkout = MagicMock()
    mock_branch = MagicMock()
    mock_is_dirty = MagicMock(return_value=False)

    mock_branch.side_effect = GitCommandError('Branch exists', status=0)

    type(mock_repo).git = mock_git
    type(mock_repo).is_dirty = mock_is_dirty
    type(mock_git).checkout = mock_checkout
    type(mock_git).branch = mock_branch

    # exising branch -> checkout
    branch_name = 'qweeewqwqw'
    switch_to_branch(mock_repo, branch_name, True)

    mock_checkout.assert_called_with(branch_name)
    mock_branch.assert_called_with(branch_name)


def test_get_current_branch():
    payload = MagicMock()
    active_branch = MagicMock()
    type(active_branch).name = PropertyMock(return_value='asddsa')
    type(payload).active_branch = active_branch

    result = get_current_branch(payload)
    assert result == 'asddsa'


@patch('git_helper.actions.common.prompt')
def test_ask_confirm(mock_prompt):
    payload = {
        'confirm': 'asdddd'
    }
    mock_prompt.configure_mock(return_value=payload)

    call_payload = {
        'type': 'confirm',
        'message': 'test',
        'name': 'confirm',
        'default': True,
    }
    result = ask_confirm('test')
    mock_prompt.assert_called_with(call_payload)
    assert result == 'asdddd'
