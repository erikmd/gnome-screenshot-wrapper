#!/usr/bin/env python3

# Copyright (c) 2016-2018, 2021  Erik Martin-Dorel
#
# This file is distributed under the MIT license, which is available
# at https://opensource.org/licenses/MIT
#
# It is part of the gnome-screenshot-wrapper tool repo, version 0.9.6

import ast
import subprocess
import sys


def get(args):
    return subprocess.check_output(["gsettings", "get"]
                                   + args).decode("utf-8").rstrip()


def disable_default_keybinding(command):
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    cmd = ['set', schema, command, '[]']
    subprocess.check_call(['gsettings'] + cmd)


def reset_default_keybinding(command):
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    cmd = ['reset', schema, command]
    subprocess.check_call(['gsettings'] + cmd)


def exist_custom_keybinding(command, binding):
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    key = 'custom-keybindings'
    schema2 = (schema + '.' + key)[:-1] + ':'
    out = get([schema, key])
    if out[-2:] == '[]':
        return False
    else:
        lst = ast.literal_eval(out)
    for item in lst:
        xcommand = get([schema2 + item, "command"]).strip("'")
        xbinding = get([schema2 + item, "binding"]).strip("'")
        if command == xcommand and binding == xbinding:
            return True
    return False


def add_custom_keybinding(name, command, binding):
    if exist_custom_keybinding(command, binding):
        print("Definition of keybinding '" + binding
              + "' already performed.", file=sys.stderr)
        return
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    key = 'custom-keybindings'
    schema2 = schema + '.' + key
    path = '/' + schema2.replace('.', '/') + '/'
    schema2 = schema2[:-1] + ':'
    out = get([schema, key])
    if out[-2:] == '[]':
        lst = []
    else:
        lst = ast.literal_eval(out)
    custom = "custom"
    n = 0
    item = path + custom + str(n) + "/"
    while item in lst:
        n += 1
        item = path + custom + str(n) + "/"
    lst.append(item)
    cmd0 = [schema, key, str(lst)]
    cmd1 = [schema2 + item, "name", name]
    cmd2 = [schema2 + item, "command", command]
    cmd3 = [schema2 + item, "binding", binding]
    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        subprocess.check_call(["gsettings", "set"] + cmd)


def remove_custom_keybinding(command, binding):
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    key = 'custom-keybindings'
    schema2 = (schema + '.' + key)[:-1] + ':'
    out = get([schema, key])
    if out[-2:] == '[]':
        lst = []
    else:
        lst = ast.literal_eval(out)
    lst2 = list(lst)
    for item in lst2:
        xcommand = get([schema2 + item, "command"]).strip("'")
        xbinding = get([schema2 + item, "binding"]).strip("'")
        if command == xcommand and binding == xbinding:
            cmd = ['reset-recursively', schema2 + item]
            subprocess.check_call(['gsettings'] + cmd)
            lst.remove(item)
    if len(lst) < len(lst2):
        if lst == []:
            cmd = ['reset', schema, key]
            subprocess.check_call(['gsettings'] + cmd)
        else:
            cmd = ['set', schema, key, str(lst)]
            subprocess.check_call(['gsettings'] + cmd)


def main():
    if len(sys.argv) != 2 or not sys.argv[1] in ['install', 'uninstall']:
        print("""Usage:
    ./custom-keybindings.py install
    ./custom-keybindings.py uninstall""", file=sys.stderr)
        exit(0)

    if sys.argv[1] == "install":
        disable_default_keybinding('screenshot')
        disable_default_keybinding('area-screenshot')
        disable_default_keybinding('window-screenshot')
        add_custom_keybinding('Interactive Screenshot',
                              'gnome-screenshot-wrapper', 'Print')
        add_custom_keybinding('Interactive Screenshot of an area',
                              'gnome-screenshot-wrapper -a', '<Shift>Print')
        add_custom_keybinding('Interactive Screenshot of a window',
                              'gnome-screenshot-wrapper -w', '<Alt>Print')

    if sys.argv[1] == "uninstall":
        remove_custom_keybinding('gnome-screenshot-wrapper', 'Print')
        remove_custom_keybinding('gnome-screenshot-wrapper -a', '<Shift>Print')
        remove_custom_keybinding('gnome-screenshot-wrapper -w', '<Alt>Print')
        reset_default_keybinding('screenshot')
        reset_default_keybinding('area-screenshot')
        reset_default_keybinding('window-screenshot')


if __name__ == "__main__":
    main()
