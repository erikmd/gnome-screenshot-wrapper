########################################################
# Installation Makefile for the gnome-screenshot wrapper
########################################################

INSTALL_DIR=install -d
INSTALL_FILE=install -m 644
INSTALL_EXEC=install -m 755
SRC=gnome-screenshot-wrapper
TARGET=/usr/bin/gnome-screenshot-wrapper
BINARY=/usr/bin/gnome-screenshot

all: help

help:
	@echo "Run 'make install'   to set up $(SRC)"
	@echo "Run 'make uninstall' to remove $(SRC)"

install:
	# Ensure zenity is installed
	which zenity
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
