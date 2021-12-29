# gnome-screenshot-wrapper

This repo contains a Bash wrapper for GNOME Screenshot.

In GNOME 3 (TTBOMK since GNOME Screenshot 3.3.2), the screenshots are
readily saved, without displaying any dialog prompt. And yet, it can
be extremely useful to be able to choose the file name for saving
one's screenshots.

The `gnome-screenshot-wrapper` script implements this feature. It is
written in Bash and it relies on the `zenity` tool.

The repo also contains a Python3 script to automate the config of
standard shortcuts (<kbd>Print</kbd> ;
<kbd>Alt</kbd>+<kbd>Print</kbd> ; <kbd>Shift</kbd>+<kbd>Print</kbd>).

It also binds another handy shortcut <kbd>Super</kbd>+<kbd>Print</kbd>
to the standard command `gnome-screenshot -i`.

The default shortcuts involving the clipboard are left untouched
(<kbd>Ctrl</kbd>+<kbd>Print</kbd> ;
<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Print</kbd> ;
<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Print</kbd>).

Before installing this tool, you may want to do a backup of your
shortcuts:

	dconf dump /org/gnome/settings-daemon/plugins/media-keys/ > dump.bak

or, optionally, a backup of your entire dconf database:

    dconf dump / > dump.bak

To avoid concurrent issues, such as a too long press on the
<kbd>Print</kbd> key, this tool uses a lock (namely, the directory
`/tmp/${USER}_gnome-screenshot-wrapper/` is temporarily created during
the execution of the wrapper script).

## Installation

You just need to clone this repo and use the provided Makefile:

	git clone https://github.com/erikmd/gnome-screenshot-wrapper
	cd gnome-screenshot-wrapper
	make install

These commands should be run **as a normal user**. The Makefile will
call itself `sudo` in the step that needs superuser rights.

## Uninstallation

To uninstall the wrapper, you can run:

	make uninstall

## Author and License

This tool was written by Erik Martin-Dorel. It is distributed under
the MIT license.
