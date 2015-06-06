#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

from dialog import Dialog, _common_args_syntax
import sys
import os
import inspect

MENU_KEY_TYPE = 'type'
MENU_KEY_COMMON = 'common'
MENU_KEY_ACTION = 'action'
MENU_KEY_GO = 'go '
MENU_KEY_BACK = 'back'
MENU_KEY_EXIT = 'exit'
MENU_KEY_CLEAR = 'clear'
MENU_KEY_CHOICES = 'choices'


class UndefinedScreen(Exception):
    """ Screen is not present in the model
    """
    def __init__(self, screen_name):
        super(UndefinedScreen, self).__init__(
            "Screen '{0}' is not present in the model".format(screen_name))


class InvalidMethod(Exception):
    """ Invalid Method name
    """
    def __init__(self, method_name):
        super(InvalidMethod, self).__init__(
            "Invalid Method name '{0}'".format(method_name))


class Menu(object):
    """ Class Menu
    """

    def __init__(self, menu_data, debug=False):
        self._screens = []
        self._screen_values = {}
        self._dialog = Dialog()
        self._dialog_methods = dict(inspect.getmembers(self._dialog))
        self._custom_methods = dict(inspect.getmembers(self))
        self._common_args = list(_common_args_syntax.keys())
        self._debug_enable = debug
        if sys.version_info.major == 2:
            self.debug = self.debug_python2

        self._menu = menu_data

        self._load_common()

    def show(self, screen_name):
        """ Show the screen
        Args:
          screen_name(string): name of the screen to show
        Raises:
            UndefinedScreen
            InvalidMethod
        """
        self._screens.append(screen_name)
        while (self._screens != []):
            self._show_current_screen()

    def debug_python2(self, msg):
        if self._debug_enable:
            raw_input(msg)

    def debug(self, msg):
        if self._debug_enable:
            input(msg)

    def clear(self):
        """ Clear the screen
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_value(self, screen_name):
        """ Get the value stored by the screen
        Args:
            screen_name(string): name of the screen to get the value
        """
        value = None
        if screen_name in self._screen_values:
            value = self._screen_values[screen_name]
        return value

    def _load_common(self):
        self._common = {}
        for item in self._menu[MENU_KEY_COMMON]:
            self._common[item] = self._menu[MENU_KEY_COMMON][item]

    def _show_current_screen(self):
        current_screen = self._screens[-1]
        (dialog_exit, dialog_value) = self._show_dialog(current_screen)
        self._screen_values[current_screen] = dialog_value
        self._do_actions(current_screen, dialog_exit, dialog_value)

    def _show_dialog(self, item):
        try:
            dialog_type = self._menu[item][MENU_KEY_TYPE]
        except KeyError as e:
            raise UndefinedScreen(str(e))
        if dialog_type in self._dialog_methods:
            screen = self._dialog_methods[dialog_type]
            (allowed_args, varargs, keywords, locals) = inspect.getargspec(screen)
            args = self._common.copy()
            screen_args = dict([(i, self._menu[item][i]) for i in self._menu[item] if i in allowed_args or i in self._common_args])
            args.update(screen_args)
            self.debug("args: %s" % args)

            dialog_exit = self._dialog_methods[dialog_type](**args)

            dialog_value = [None]
            if type(dialog_exit) is tuple:
                dialog_exit, dialog_value = dialog_exit[0], dialog_exit[1:]

            return (dialog_exit, dialog_value)

    def _do_actions(self, item, dialog_exit, dialog_value):
        """ Do actions
        """
        action = self._menu[item].get(MENU_KEY_ACTION, {}).get(dialog_exit)
        if action is None:
            return

        if type(action) is dict:
            action = action.get(dialog_value[0])
        if type(action) is str:
            self._do_action(action)
        if type(action) is list:
            for action_item in action:
                self._do_action(action_item)

    def _do_action(self, action):
        """ Do action
        """
        if MENU_KEY_EXIT in action:
            self._screens = []
        elif MENU_KEY_GO in action:
            new_screen = action.split(' ')[1]
            if new_screen == MENU_KEY_BACK:
                self._screens.pop()
            else:
                self._screens.append(new_screen)
        else:
            # Custom method
            self._call_custom_method(action)

    def _call_custom_method(self, action):
        """ Call custom method
        """
        method_name = action
        parameters = {}
        if type(action) is list:
            if len(action) > 0:
                method_name = action[0]
            if len(action) > 1:
                parameters = action[1]

        if method_name in self._custom_methods:
            self._custom_methods[method_name](**parameters)
        else:
            raise InvalidMethod(action)
