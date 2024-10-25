# .bashrc

GIT_PS1_SHOWDIRTYSTATE=true
GIT_PS1_SHOWUNTRACKEDFILES=true
GIT_PS1_SHOWSTASHSTATE=true
GIT_PS1_SHOWUPSTREAM=auto
export PS1='[\[\033[1;32m\]\u\[\033[00m\]@\h \[\033[1;34m\]\w\[\033[1;31m\]$(__git_ps1)\[\033[00m\]]\n\$ '
alias ll='ls -l --color=auto'
