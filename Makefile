########################################################
# Installation Makefile for the gnome-screenshot wrapper
########################################################

INSTALL_DIR=install -d
INSTALL_FILE=install -m 644
INSTALL_EXEC=install -m 755
SRC=gnome-screenshot-wrapper
TARGET=/usr/local/bin/gnome-screenshot-wrapper
BINARY=/usr/bin/gnome-screenshot

all: help

help:
	@echo "Run 'make install'   to setup $(SRC)"
	@echo "Run 'make uninstall' to purge $(SRC)"
	@echo
	@echo "REMARK: These commands should be run as a normal user."
	@echo "(The step that needs superuser rights will call sudo.)"

install:
	# Ensure zenity is installed
	which zenity
	# Ensure xdg-user-dir is available
	xdg-user-dir PICTURES
	# Ensure $(BINARY) is executable
	[ -f $(BINARY) ] && [ -x $(BINARY) ]
	# Install the wrapper
	sudo $(INSTALL_EXEC) $(SRC) $(TARGET)
	# Install the shortcuts
	./custom_keybindings.py install

uninstall:
	# Reset the shortcuts
	./custom_keybindings.py uninstall
	# Remove the wrapper
	sudo $(RM) $(TARGET)

.PHONY: all help install uninstall
