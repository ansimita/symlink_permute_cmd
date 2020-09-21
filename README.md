# Create Symbolic Links for Permutations of a Command

![](https://i.kym-cdn.com/entries/icons/original/000/027/995/crying.jpg)

Ever mistype `ls` and other commands?

This script permutes the characters of a command and symlinks the resulting
command variations to the actual command.

## Examples

```
$ sl
-bash: sl: command not found
$ ./symlink_permute_cmd ls
'sl' created in /home/username/.local/bin symlinks to /bin/ls
$ sl -1
LICENSE.md
README.md
symlink_permute_cmd
test.py
```

The example below shows that existing commands that are variations of the `git`
command are skipped.

```
$ tgi status
-bash: tgi: command not found
$ ./symlink_permute_cmd git
'gti' created in /home/username/.local/bin symlinks to /usr/bin/git
'igt' created in /home/username/.local/bin symlinks to /usr/bin/git
'itg' created in /home/username/.local/bin symlinks to /usr/bin/git
'tgi' created in /home/username/.local/bin symlinks to /usr/bin/git
'tig' command exists. Skipping...
$ tgi status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

The example below shows that the private bin directory can be specified.
The private bin directory will be created if it does not exist.

```
$ ./symlink_permute_cmd ps --symlink-at ~/.bin
Created private bin directory at /home/username/.bin
Please add /home/username/.bin to your $PATH
'sp' created in /home/username/.bin symlinks to /bin/ps
```

The example below shows that the script checks whether a command, based on your
`$PATH`, exists before creating the symlinks.

```
$ ./symlink_permute_cmd foo
foo: command not found
```

The example below shows that the script can accept the absolute path of a
command.

```
$ ./symlink_permute_cmd /bin/rm
'mr' created in /home/username/.local/bin symlinks to /bin/rm
```

## Note

The private bin directory that the script creates symlinks at is
`$HOME/.local/bin` if both `$HOME/bin` and `$HOME/.local/bin` do not exist.

## Requirements

Requires Python 3.6 or newer.

## Tests

```
$ python3 -m unittest
```

## License

[MIT](LICENSE.md).
