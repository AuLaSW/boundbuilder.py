"""
utils.py

Contains utilities needed for the boundbuilder application.
"""
from pathlib import PurePath, Path
import time
import os
import sys
# requires oyaml
import oyaml as yaml


def trace():
    pass


class ProjectManager:
    pass


"""
if Path('testing.yaml').exists():
    with open('testing.yaml', 'r') as test_status:
        testing = yaml.safe_load(test_status)['status']

    if testing:
        from pdb import set_trace as trace
"""


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


# When we drop files onto a python file, the sys.argv arguments are just the
# direct paths to the file, which is great. I can use that.
class DropIns:
    """
    # Class DropIns

    Class whose object holds onto and dissects the files that are dropped into
    it.

    ## Methods
    """

    files: dict = dict()
    base_path: Path
    proj_ord: ProjectManager
    __file_type: str = '.pdf'

    def __init__(self, *args):
        assert len(args) > 1, "Please drop files onto the application."

        print('Loading Sheets...')

        self.base_path = Path(PurePath(args[0]).parents[0])

        temp_files = list()

        for file in args:
            file_name = PurePath(file).name

            if not file_name.endswith(self.__file_type):
                continue

            temp_files.append(FileName(file_name.removesuffix(self.__file_type)))

        self.proj_ord = ProjectManager(
                bp=self.base_path,
                names=temp_files)

        self.files = self.proj_ord.order(temp_files)


class ProjectManager:
    """
    # ProjectManager

    Class that orders the incoming files based on project specifications.
    """

    # __base_config: Path = Path(os.path.dirname(__file__)) / 'base_config.yaml'
    __base_config: Path = Path.home() / Path('AppData/Local/Programs/boundbuilder/base_config.yaml')
    config: dict = dict()
    default_configs: dict

    def __init__(self, bp: PurePath, conf: str | dict = None,
                 names: list[FileName] = None) -> None:
        # we must have these values
        assert bp is not None, \
            "Must supply a base path for the drawings to ProjectOrdering."

        assert self.__base_config.exists(), \
            f"No base config file found, create {self.__base_config}."

        with open(self.__base_config, 'r') as base_config:
            print("Loading default configs...")
            self.default_configs = yaml.safe_load(base_config)

        # if we are choosing a default config, do that
        if isinstance(conf, str):
            assert conf in list(self.default_configs.keys()), \
                "Config string must be a defined default config."
            self.config = self.default_configs[conf]
        # if we are given a dictionary, use that as the config
        elif isinstance(conf, dict):
            self.config = conf
        # if we are given names, guess the ordering
        elif isinstance(names, list):
            self.config = self.default_configs[
                    ProjectManager.find_config(names)
                    ]
        # otherwise, grab the config from the config file
        else:
            config_path = bp.with_name('config.yaml')

            assert Path(config_path).exists(), \
                "The file 'config.yaml' must exist."

            with open(config_path, 'r') as load_config:
                self.config = yaml.safe_load(load_config)

        assert self.config != {}, "Config cannot be empty."

    @classmethod
    def find_config(cls, names: list[FileName]):
        """Attempts to determine config given list of names"""
        for file in names:
            # determine if there are civil drawings
            if file.leader == 'C':
                return 'default_w_civil'
            # if there is an A1.0, then we likely have landscaping plans
            elif file.full_name == 'A1.0':
                return 'default_w_landscaping'
            elif file.leader == 'LS-':
                return 'default_w_LSC'

        # otherwise, return the default value
        return "default"

    def order(self, names: list[FileName]) -> dict():
        """Input the file names and sort them based on the config used"""
        ordered_dict: dict = dict()
        print("Organizing sheets...")

        for bound_set, sheet_order in self.config.items():

            ordered_dict[bound_set] = list()

            # add the names to the set
            for leader in sheet_order:
                # checking to make sure we are trying to work with the dictionary
                if not isinstance(leader, str):
                    continue
                temp: list = list()
                # add all of the names for this leader to the temp set
                for name in names:
                    if name.leader == leader:
                        temp.append(name)

                trace()
                # these should sort the temp list
                temp = sorted(temp, key=lambda sheet: sheet.minor_alpha)
                temp = sorted(temp, key=lambda sheet: sheet.minor_num)
                temp = sorted(temp, key=lambda sheet: sheet.major_num)

                trace()

                # append the values from the temp list to the 
                # ordered list dictionary
                for value in temp:
                    ordered_dict[bound_set].append(value)

        return ordered_dict


if __name__ == "__main__":
    drop = DropIns(*sys.argv)
    order = drop.order()

    for key, value in order.items():
        print()
        print(key)
        print()
        for sheet in value:
            print(sheet.full_name)

    time.sleep(10)
