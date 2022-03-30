import enum


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        """https://docs.python.org/3/library/enum.html#using-automatic-values"""
        return name


class TownActionEnum(AutoName):
    create = enum.auto()
    edit = enum.auto()
    delete = enum.auto()
    view = enum.auto()
    assign = enum.auto()


class GlobalCategoryActionEnum(AutoName):
    view = enum.auto()
    detail = enum.auto()
    create = enum.auto()
    edit_name = enum.auto()
    edit_description = enum.auto()
    delete = enum.auto()


class CategoryActionEnum(AutoName):
    view_towns = enum.auto()
    view_by_town = enum.auto()
    create = enum.auto()
    detail = enum.auto()

    edit_name = enum.auto()
    edit_description = enum.auto()
    delete = enum.auto()
    add_sub_category = enum.auto()
    view_sub_category = enum.auto()