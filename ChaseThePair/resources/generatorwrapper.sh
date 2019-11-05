SCRIPT_PATH=`dirname $(readlink -f $0)`
BINARY="${SCRIPT_PATH}/setsGenerator-linux-amd64"
size=$1

pwd

printf "${size}\ny" | $BINARY

mv "logs.txt" "set_${size}.set"
