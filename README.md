# git-utilities

Repository of useful git aliases and management scripts

## Aliases

Run the following to import useful aliases into your bash shell

```bash
source git-aliases.bash
```

## Rebase your repository to upstream

Run the following to rebase your repository against `upstream`:

```bash
<path to>/rebase-repo.sh
```

> **NOTE:** Assumes you have already set up an upstream repo with the following:

```bash
git remote add upstream <url of upstream repository>
```

## Set the time of the most recent commit to 'now'

Sometimes, after squashing git commits, it is useful to set the time to 'now', this is the script that will do it for you.

```bash
./set_last_commit_time.bash
```

> **NOTE:** You can also set it to any time you like with `-i`


