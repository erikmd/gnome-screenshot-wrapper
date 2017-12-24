########################################################
# Installation Makefile for the gnome-screenshot wrapper
########################################################

INSTALL_DIR=install -d
INSTALL_FILE=install -m 644
INSTALL_EXEC=install -m 755
SRC=gnome-screenshot
TARGET=/usr/bin/gnome-screenshot
BACKUP=/usr/bin/gnome-screenshot.real
DIVERT=--add --rename --divert $(BACKUP) $(TARGET)

all: help

help:
	@echo "Run 'sudo make install'   to set up the $(SRC) wrapper"
	@echo "Run 'sudo make uninstall' to remove the $(SRC) wrapper"

install:
	# Ensure zenity is installed
	zenity --version
	# Ensure $(TARGET) is executable
	[ -f $(TARGET) ] && [ -x $(TARGET) ]
	# Ensure dpkg-divert works & raises no clashes for this divert
	dpkg-divert --test $(DIVERT)
	# Install the divert
	dpkg-divert $(DIVERT)
	# Install the wrapper
	$(INSTALL_EXEC) $(SRC) $(TARGET)

uninstall:
	# Ensure $(BACKUP) is still here
	[ -f $(BACKUP) ] && [ -x $(BACKUP) ]
	# Remove the wrapper
	$(RM) $(TARGET)
	# Remove the divert
	dpkg-divert --rename --remove $(TARGET)

.PHONY: all help install uninstall
