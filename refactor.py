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


class DropIns:
    def __init__(self):
        pass
