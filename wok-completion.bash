#!/bin/bash

_wok_completions() {
	if [[ $COMP_CWORD == 1 ]]; then
		COMPREPLY=($(compgen -W "status switch job task end start details" -- "${COMP_WORDS[1]}"))
	elif [[ $COMP_CWORD > 1 ]]; then
		WORD=${COMP_WORDS[$COMP_CWORD]}
		if [[ $WORD == -* ]]; then
			# options
			COMPREPLY=($(compgen -W "-h --help" -- "$WORD"))
			case ${COMP_WORDS[1]} in
				# "status"|"details"|"end") # nothing
				"switch"|"start")
					COMPREPLY+=($(compgen -W "-c --create" -- "$WORD"))
					;;
				"job")
					COMPREPLY+=($(compgen -W "-t --table -c --create -d --delete -r --rename -l --list" -- "$WORD"))
					;;
				"task")
					COMPREPLY+=($(compgen -W "-t --table -c --create -d --delete -r --rename -l --list" -- "$WORD"))
					;;
			esac
		else
			# arguments
			current_job=$(cat ~/.wok/current_job 2> /dev/null)
			jobs=($(ls ~/.wok | grep -v current_job))
			case ${COMP_WORDS[1]} in
				# "status"|"details") # nothing
				"switch"|"job")
					COMPREPLY+=($(compgen -W "$(echo ${jobs[@]})" -- "$WORD"))
					;;
				"task")
					tasks=($(ls ~/.wok/${current_job}))
					COMPREPLY+=($(compgen -W "$(echo ${tasks[@]})" -- "$WORD"))
					;;
				"start"|"end")
					paths=($([ ${current_job} ] && ls ~/.wok/${current_job}))
					for job in "${jobs[@]}"; do
						for task in $(ls ~/.wok/$job); do
							paths+=($job.$task)
						done
					done
					COMPREPLY+=($(compgen -W "$(echo ${paths[@]})" -- "$WORD"))
			esac
		fi
	fi
}

complete -F _wok_completions wok
