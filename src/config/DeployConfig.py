# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser


class DeployConfig:
    def __init__(self, fin, gen=False):
        self.__file = fin
        self.__cfgParser = ConfigParser()

        if not gen:
            self.reload()

    def reload(self):
        self.__cfgParser.read(self.__file)

        mode = self.__cfgParser.get('MODE', 'MODE')
        if mode == 'LOCAL':
            self.BINDING_ADDRESS = '127.0.0.1'
            self.CORE_ADDRESS = '127.0.0.1'
        else:
            self.BINDING_ADDRESS = '0.0.0.0'
            self.CORE_ADDRESS = self.__cfgParser.get('CORE_SERVER', 'HOST')

        self.LOG_PORT = self.__cfgParser.get('PORT', 'LOG_PORT')
        self.DATA_PORT = self.__cfgParser.get('PORT', 'DATA_PORT')
        self.CORE_PORT =  self.__cfgParser.get('PORT', 'CORE_PORT')
