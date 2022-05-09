import os

from jproperties import Properties

"""
returns the token(pos0) and the user(pos1)
"""
def load_config() -> tuple:
    configs = Properties()
    path = os.path.dirname(os.getcwd())
    with open(path + '/Config.properties', 'rb') as config_file:
        configs.load(config_file)
    __token = configs.get("token1").data
    __holder = configs.get("user1").data
    return __token, __holder
