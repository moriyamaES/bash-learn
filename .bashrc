# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

# git
. /usr/share/doc/git/contrib/completion/git-completion.bash
. /usr/share/doc/git/contrib/completion/git-prompt.sh

GIT_PS1_SHOWDIRTYSTATE=true
GIT_PS1_SHOWUNTRACKEDFILES=true
GIT_PS1_SHOWSTASHSTATE=true
GIT_PS1_SHOWUPSTREAM=auto
export PS1='[\[\033[1;32m\]\u\[\033[00m\]@\h \[\033[1;34m\]\w\[\033[1;31m\]$(__git_ps1)\[\033[00m\]]\n\$ '

