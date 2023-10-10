"""
Refactor.py

A temporary file for refactoring the classes and methods within boundbuilder.
"""
from pathlib import PurePath, Path
import sys
import oyaml as yaml


"""
Monadic Implemenation
"""


class Config:
    """
    # Manage loading the config. Monadic type.

    ## Methods:
        - __init__(self, **kwargs)
        - map(obj, tranform, *args)
    """
    name: str = None
    path: Path = None
    file: Path = None
    default_name: str = 'base_config.yaml'
    default_path: Path = Path.home() / Path('AppData/Local/Programs/boundbuilder')
    config: dict = None
    # whether the config object found the config or not
    has_config: bool = True

    def __init__(self, **kwargs):
        """ Wrapper for the Config monad type

        Params:
            name: str?
            path: Path?

        Data Fields:
            config: dict
            has_config: bool
        """
        self.name = kwargs['name'] or self.default_name
        self.path = kwargs['path'] or self.default_path

        self.file: Path = self.path / self.name
        self.default_file: Path = self.default_path / self.default_name

        self.__load_config(**kwargs)

    def __load_config(self, **kwargs):
        if kwargs['config']:
            self.config = kwargs['config']
        # search for config file in project folder
        elif self.file.is_file() and self.default_file.is_file() and not self.file.samefile(self.default_file):
            with open(self.file, 'r') as load_config:
                self.config = yaml.safe_load(load_config)
        # search for config file in default location
        elif self.default_file.is_file():
            with open(self.default_file, 'r') as load_config:
                self.config = yaml.safe_load(load_config)
        # if no config is found, then do not load config
        else:
            print('No config found.')
            self.has_config = False

    @classmethod
    def map(cls, obj: object, transform: callable, *args):
        if obj.has_config:
            name, path, config = transform(obj, *args)
        else:
            return obj

        return Config(
            name=name,
            path=path,
            config=config,
        )


class FileName:
    """
    # Class FileName

    Records the filename and gives some properties to manipulate it.
    """

    def __init__(self, name):
        self.full_name = name

        self.leader = FileName.__sep_leader(name)
        self.major_num = FileName.__sep_major_num(name)
        self.minor_num = FileName.__sep_minor_num(name)
        self.minor_alpha = FileName.__sep_minor_alph(name)
        self.rev = FileName.__sep_rev(name)

    @classmethod
    def __sep_leader(cls, name: str):
        temp = str()

        for char in name:
            if not char.isdigit():
                temp += (char)
            else:
                break

        return temp

    @classmethod
    def __sep_major_num(cls, name: str):
        temp = str()

        for char in name:
            if char.isdigit():
                temp += (char)
            elif char == '.':
                break

        return temp

    @classmethod
    def __sep_minor_num(cls, name: str):
        temp = str()
        after_delim = False

        for char in name:
            if char.isdigit() and after_delim:
                temp += (char)
            elif after_delim and not char.isdigit():
                break
            elif char == '.':
                after_delim = True

        return temp

    @classmethod
    def __sep_minor_alph(cls, name: str):
        temp = str()

        for char in name:
            if char.isdigit():
                temp += (char)
            elif char == '.':
                break

        return temp

    @classmethod
    def __sep_rev(cls, name: str):
        temp = str()
        after_delim = False

        for char in name:
            if char.isalpha() and after_delim:
                temp += (char)
            elif char == '.':
                after_delim = True

        return temp


class Project:
    base_path: Path = None
    files: dict = dict()
    __file_type: str = None
    has_files: bool = True

    def __init__(self, *files, **kwargs):
        if len(files) < 1:
            print("Please inputs files into the executable.")
            self.has_files = False
        else:
            print('Loading sheets...')

        # grab the base path of where the file is called from.
        self.base_path = Path(PurePath(files[0]).parents[0])

        self.config = Config(
            **{
                'name': kwargs['config_name'] or None,
                'path': kwargs['config_path'] or None
             }
        )
