"""
Refactor.py

A temporary file for refactoring the classes and methods within boudnbuilder.
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
    config: dict = None
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
        self.name = kwargs['name'] or 'base_config.yaml'
        self.path = kwargs['path'] or \
            Path.home() / Path('AppData/Local/Programs/boundbuilder')

        file: Path = self.path / self.name

        if file.is_file() and not kwargs['config']:
            # define self.config
            with open(file, 'r') as load_config:
                self.config = yaml.safe_load(load_config)
        elif kwargs['config']:
            self.config = kwargs['config']
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
