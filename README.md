# git n
### Mandatory features
- switch between branches
- create new branch from a task
	- work with GitHub tasks
	- work with Jira
- push data to server in corresponding branches and create PR
- commit helper
- prettier / linter / tests run based on commits

### Nice to have features
- clean tasks
- rebase helper
- contextual switch between branches for hot fixes
- bisect helper

## Features description
### Switch between branches
Show list of branches and propose user to switch to an existing branch. In case of not committed changes present, store them in a stash. /And extract afterwards./

### Create new branch
Get list of assigned tasks and pull its names, normalize and use as a prefix for a branch. Propose user to choose branch type or set *feature* by default.

### Push data to server in corresponding branches and create PR
Push changes to server by a command to the same branch as local. Parse response and open PR page in browser according to user’s input.

### Commit helper
Parse task ID from a branch name and add it to commit message as a prefix. Also propose user a default commit message based on task ID.

### SCA checks
Run all appropriate checks and mark commit as a ready or not. Save execution results in db.

---
### Clean tasks
Clean merged and old branches. Allows use to choose which branches should be removed.

### Rebase helper
Shortcuts for rebase continue and rebase develop.

### Contextual switch between branches for hot fixes
Froze current task progress and create a new branch. Return to stashed changes afterwards.

### Bisect helper
Choose good and bad commits from a commits tree.