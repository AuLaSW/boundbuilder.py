"""
utils.py

Contains utilities needed for the boundbuilder application.
"""
from pathlib import PurePath, Path
import time
import sys
# requires oyaml
import oyaml as yaml


# When we drop files onto a python file, the sys.argv arguments are just the
# direct paths to the file, which is great. I can use that.
class DropIns:
    """
    # Class DropIns

    Class whose object holds onto and dissects the files that are dropped into
    it.

    ## Methods
    """

    files: list = list()
    __file_type: str = '.pdf'

    def __init__(self, *args):
        assert len(args) > 1, "Please drop files onto the application."

        self.proj_ord = ProjectOrdering(conf="default")
        self.base_path = PurePath(args[1]).parents[0]

        for file in args[1:]:
            file_name = PurePath(file).name

            assert file_name.endswith(self.__file_type), \
                "Must use files with the 'pdf' ending."

            self.files.append(file_name.removesuffix(self.__file_type))

    def order(self):
        """Order the files dropped in based on the project config"""
        self.proj_ord.order(self.files)


class ProjectOrdering:
    """
    # ProjectOrdering

    Class that orders the incoming files based on project specifications.
    """

    config: dict = dict()
    default_configs: dict = {
        "default": {
            "ARCH": {'COVER', 'T', 'X', 'D', 'S', 'LS', 'A'},
            "STRUC": {'S'},
            "MECH": {'M'},
            "MP": {'MP'},
            "PLUMB": {'P'},
            "ELEC": {'ES', 'E'},
            "SET": {
                'ARCH',
                'MECH',
                'MP',
                'PLUMB',
                'ELEC',
            },
        },
        "default_w_civil": {
            "ARCH": {'COVER', 'T', 'X', 'C', 'D', 'S', 'LS', 'A'},
            "CIVIL": {'C'},
            "MECH": {'M'},
            "MP": {'MP'},
            "PLUMB": {'P'},
            "ELEC": {'ES', 'E'},
            "SET": {
                'ARCH',
                'MECH',
                'MP',
                'PLUMB',
                'ELEC',
                'CIVIL',
            },
        },
        "default_w_landscaping": {
            "ARCH": {'COVER', 'T', 'X', 'LS', 'D', 'S', 'A'},
            "MECH": {'M'},
            "MP": {'MP'},
            "PLUMB": {'P'},
            "ELEC": {'ES', 'E'},
            "SET": {
                'ARCH',
                'MECH',
                'MP',
                'PLUMB',
                'ELEC',
            },
        },
    }

    def __init__(self, bp: PurePath = None, conf=None):
        assert bp or conf is not None, \
            "Must supply either a base path or a default config to the ProjectOrdering class."

        # if we are choosing a default config, do that
        if conf is not None:
            self.default_configs[conf]

        # otherwise, grab the config
        else:
            config_path = bp.with_name('config.yaml')
            assert Path(config_path).exists(
            ), "The file 'config.yaml' must exist."

            with open(config_path, 'r') as load_config:
                self.config = yaml.safe_load(load_config)

    def order(self, *names: str):
        """Input the file names and sort them based on the config used"""
        # get all of the keys associated with the config so we can organize
        # the files
        config_keys = list(self.config.keys()).remove("SET")

        for name in names:
            if name.


DropIns(*sys.argv)
time.sleep(10)
