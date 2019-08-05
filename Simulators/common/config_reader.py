import ast


class ConfigReader:
    def __init__(self):
        pass

    @staticmethod
    def readconfigfile(section, key):
        try:
            from configparser import ConfigParser
        except ImportError:
            from ConfigParser import ConfigParser  # ver. < 3.0
        # instantiate
        config = ConfigParser()
        # parse existing file
        config.read('..//testdata//config.ini')
        # read values from a section
        list_of_values = ast.literal_eval(config.get(section, key))
        return list_of_values
