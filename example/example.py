#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Python menu example
"""

import os
import yaml
import python_menu


class Menu1(python_menu.Menu):
    def custom(self):
        self.debug("Custom 1")

    def custom2(self, value):
        self.debug("Custom 2: %s" % value)

    def gauge(self):
        self.show('gauge_start')


def main():
    example_yaml = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'menu.yaml')
    stream = open(example_yaml, 'r')
    menu_data = yaml.load(stream)
    menu = Menu1(menu_data, debug=False)
    menu.show('main')

if __name__ == '__main__':
    main()
