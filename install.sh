#change to your OS packagmenager
apt update
install(){ apt install -y "$@" ; }

install python3
install python3-pip
install python3-requests

printf "\n\n\e[32mInstallation successful!\e[0m\n"
printf "\e[32mLaunch agent with: \e[0mpython3 agent2.py\n"