# Creates an eternal bash log in the form
# PID USER INDEX TIMESTAMP COMMAND
export HISTTIMEFORMAT="%s "
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND ; }"'echo $$ $USER \
                   "$(history 1)" >> ~/.bash_eternal_history'
