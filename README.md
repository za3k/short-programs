Short Programs
---

A collection of short programs which I wrote and find useful, but don't need their own repository

add-base26
---
Adds two lines of english text, mod 26 (ancient-style crypto)

arch-package-summary
---
Lists manually installed packages with descriptions. Both normal and AUR packages are included, but AUR packages are tagged.

asciicam
---
Displays the webcam through ASCII graphics. Just for fun.

changed-files
---
In Arch Linux, lists the config files which have been altered from the default.

clonebb
---
Clones a Bitbucket repository. Usage: `clonebb [USER] REPOSITORY`

clonegh
---
Clones a Github repository. Usage: `clonegh [USER] REPOSITORY`

confirm
---
(Dead) `cp confirm.txt /usr/share/confirm/confirm` for install. Randomly tells you to avoid a default course of action to switch up habits. Poorly designed, doesn't work.

create-github-repo
---
Usage: `create-github-repo NAME DESCRIPTION`

decolorize
---
Strips ANSI color codes out of a stream

delink
---
Usage: `delink FILE`. Removes a level of symlink, moving the symlink's target in place of the symlink. Can have bad side-effects, use with caution.
See also `mvln`

dzen-clock
---
Make a small clock at the bottom of the screen

etherpad
---
Create, update, fetch, or delete text files on etherpad.za3k.com (or any other etherpad-lite instance).

    Usage: etherpad put [<pad>]
                    get <pad>
                    delete <pad>

extract-alarmpi
---
Downloads the latest version of Arch Linux for Raspberry Pi (aka alarmpi) as a .tar.gz file and converts it to an image file which can be copied directly to an SD card.

    Usage: extract-alarmpi [SOURCE.tar.gz [TARGET.img]]

filter
---
Usage: `cat <stream | filter --negative FILENAME` blacklists anything in FILENAME, there are options for whitelisting and dealing with repeats.

fragile-treediff
---
Usage: `fragile-treediff FOLDER1 FOLDER2`
Returns a success or failure error code, depending on whether two folders are exactly identical.

google
---
Searches for something on google, opening the results page in the default browser.

# google-count
Show the number of results on Google for xkcd-style big data analysis.

Requirements: `pip install beautifulsoup4`

Usage:

    google-count.py "Hello world"
    264000000

hours
---
Reports what hours I was at the computer, based on my bash history. On linux, I instead use [keystroked](https://github.com/vanceza/keystroked).

internet-timelimit
---
(Arch, netcfg) Connects to the internet for short period of time, then automatically disconnects. Usage: `internet.sh MINUTES REASON`

last
---
Prints the last line from bash's history

lines
---
Get a slice of lines from a file: `lines <start> <end> <file>` or `cat <file> | lines <start> <end>`.

lwjgl-fix
---
On Arch Linux, fix lwjgl.jar in minecraft

markov
---
Markov-chain input on a per-word basis

    > curl http://www.ccel.org/ccel/bible/kjv.txt | ./markov # King James Bible
    name resteth and can never a coffin in it; it doth also vanity unto Joseph, I live: and entered into the son of the gate was Jaziz the sons also suck the son of Jehoiada, a sign.
 
    preserved in wait with it.
    
    the
    while they
    prophets?
    our God, the angel, and became a loud voice, that have said, Hearken to me.
    
    concerning his presence; let him to those that is the
    Lord of the solemn feasts, as these things in the
    thou succeedest them, and buy them, Thus saith unto the tribe of
    that thou hast followed

mvln
---
Moves a files, but leaves a symlink pointing to the new location in the old place.
See also `delink`

{brown,pink,white}noise
---
Play randomly-generated noise through the speakers

owns?
---
Checks which Arch Linux package owns a command

passgen
---
Returns a random password or passphrase

Usage:

        passgen [-w|--word] [LENGTH]

ping-test
---
Return true if the internet is up (a single ping to 8.8.8.8 returns).

pomodoros
---
Reports number of pomodoros completed to beeminder. Usage: `pomdoros NUM-POMODOROS DESC`

pull-requester
---
(Obsoleted by git-hub command) Create a new pull request on github for the current github project

pushgh
---
Push to an empty Github repo. Usage: `pushgh [USER] REPOSITORY`

random
---
Print a random line out of a file

retry
---
Retry a command 5 times or until it succeeds

rtmux
---

Usage:

    rtmux HOST

Attaches to a remote tmux session, or opens one if none exists.

say
---
Read the text aloud. Requires `festival`.

setop
---
Command-line program for performing basic set operations on lines in files. `comm` can be used for some of this on sorted files but it's a little stronger.

timer
---
Kitchen timer for the command line

webcam-picture
---
Use the webcam to take a single picture. Usage: `webcam-picture picture.png`

wordcount
---
Counts the number of words in a file or stream.
