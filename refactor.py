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
    name: str = None
    path: Path = None
    config: dict = None

    def __init__(self, **kwargs):
        """ Wrapper for the Config monad type

        Params:
            name: str?
            path: Path?

        Data Fields:
            config: dict
        """
        self.name = kwargs['name'] or 'base_config.yaml'
        self.path = kwargs['path'] or \
            Path.home() / Path('AppData/Local/Programs/boundbuilder')

        file: Path = self.path / self.name

        if file.is_file():
            # define self.config
            with open(file, 'r') as load_config:
                self.config = yaml.safe_load(load_config)
        else:
            print('No config found.')

    def map(self, obj: object, trasnform: callable, *ags):
        pass


class DropIns:
    def __init__(self):
        pass
