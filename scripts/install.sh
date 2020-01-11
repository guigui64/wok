#!/usr/bin/env bash

set -u # to avoid expanding unset variables

# script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# arg variables
auto_completion=
install_dir="$HOME/.local/bin"

help() {
	cat << EOF
usage: $0 [OPTIONS]

	--help              Show this messaged
	--install-dir=NAME  Specify installation directory (default="$HOME/.local/bin")
	--[no-]completion   Enable/disable auto completion in shell (supports bash)
EOF
}

for opt in "$@"; do
	case $opt in
		--help)
			help
			exit 0
			;;
		--install-dir=*)
			install_dir=${opt/*=/}
			;;
		--completion)
			auto_completion=1
			;;
		--no-completion)
			auto_completion=0
			;;
		*)
			echo "unrecognized option: $opt"
			help
			exit 1
			;;
	esac
done

ask() {
	while true; do
		read -p "$1 [Y/n] " -r
		REPLY=${REPLY:-"y"}
		if [[ $REPLY =~ ^[Yy]$ ]]; then
			return 1
		elif [[ $REPLY =~ ^[Nn]$ ]]; then
			return 0
		fi
	done
}

echo "> Cleaning first..."
rm -rfv {build,dist}/
echo "> Clean [OK]"
echo

echo "> Building the executable"
echo
pyinstaller -n wok -F wokcli/wokcli.py 2> >(sed 's/^/\t/')
echo
echo "> Build [OK]"
echo

echo "> Copying executable to "$install_dir"..."
[ ! -d $install_dir ] && mkdir -v $install_dir
cp -v dist/wok $install_dir/
echo "> Copy [OK]"
echo

[ ${PATH##*"$install_dir"*} ] && ( echo "/!\\ $install_dir is not in your PATH /!\\" ; echo )

echo "> Auto-completion"
# Auto-completion
if [ -z "$auto_completion" ]; then
	ask "Do you want to enable auto-completion?"
	auto_completion=$?
fi
if [ $auto_completion -eq 0 ]; then
	echo "> Auto-completion [SKIPPED]"
else
	echo "TODO auto completion"
	echo "> Auto-completion [OK]"
fi
echo

echo "Install finished !"
exit 0
