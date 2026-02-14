#change to your OS package manager
apt update
install(){ apt install -y "$@" ; }

install python3
install python3-pip
install python3-requests

printf "\e[32mLaunch agent with: \e[0mpython3 agent2.py\n"