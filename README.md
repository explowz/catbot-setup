## Catbot Setup

Setup scripts for cat-bots (cathook navbots)
For more information, visit [Cathook](https://github.com/explowz/cathook)

After the install script finished successfully, navmesh files have to be moved into your tf2 maps directory.  
They can be found [here](https://github.com/explowz/catbot-database).

## Required Dependencies
Ubuntu/Debian
`sudo apt-get install nodejs firejail net-tools x11-xserver-utils`

Fedora/Centos
`sudo dnf install nodejs firejail net-tools xorg-x11-server-utils`

Arch/Manjaro (High Support)
`sudo pacman -Syu nodejs npm firejail net-tools xorg-xhost`

To run the bots on a headless machine also install `xorg-server-xvfb`