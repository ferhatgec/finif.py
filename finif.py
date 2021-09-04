#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# finif[dot]py - cli .ini parser
#
# github.com/ferhatgec/finif.py
# github.com/ferhatgec/finif

from sys import argv

class finif:
    def __init__(self, filename: str):
        self.file_data = ''
        self.init = inif()

        with open(filename, 'r') as file:
            for line in file:
                self.file_data += line

            self.file_data += '\n'

        self.init.parse(self.file_data)

    def get(self, argument: str) -> str:
        data = argument.split(':')

        return self.init.get(data[0], data[1]) if len(data) > 1 else '""'


class inif_category:
    def __init__(self):
        self.category_name = ''
        self.key_value = {}


class inif:
    class inif_tokens:
        CategoryStart = '['
        CategoryEnd = ']'
        Eq = '='
        Comment = ';'

    def __init__(self):
        self.__init = []

        self.__category_start, \
        self.__category_data, \
        self.__key_data = False, False, False

        self.__category_name, self.__key, self.__data = '', '', ''

    def parse(self, file_data: str):
        for ch in file_data:
            if self.__key_data:
                if ch != '\n':
                    self.__data += ch
                    continue

                self.__key = self.__key.strip()

                if len(self.__init) > 1 and self.__init[len(self.__init) - 1].category_name == self.__category_name:
                    self.__init[len(self.__init) - 1].key_value[self.__key].append(self.__data)
                else:
                    val = inif_category()
                    val.category_name = self.__category_name
                    val.key_value = {
                        self.__key: self.__data
                    }

                    self.__init.append(val)

                self.__key_data = False
                self.__key = ''
                self.__data = ''

                continue

            if self.__category_start:
                if ch != self.inif_tokens.CategoryEnd:
                    self.__category_name += ch
                    continue

                self.__category_start = False
                self.__category_data = True
                continue

            if ch == self.inif_tokens.CategoryStart:
                if not len(self.__category_name) == 1:
                    self.__category_name = ''

                self.__category_start = True
            elif ch == self.inif_tokens.Eq:
                if self.__category_data and not len(self.__key) == 1:
                    self.__key_data = True
            else:
                if self.__category_data and ch != ' ':
                    self.__key += ch

    def get(self, category: str, key: str) -> str:
        for val in self.__init:
            if val.category_name == category:
                for store in val.key_value.items():
                    if store[0] == key:
                        return store[1]

        return '\"\"'


if len(argv) < 2:
    print('finif.py - cli .ini parser')
    exit(1)

init = finif(argv[1])

for i in range(2, len(argv)):
    print(f'\x1b[0;97m{init.get(argv[i])}\x1b[0m')
