import unittest
import typing
import logging
from pydt3 import DEVONthink3
from pydt3.apps.devonthink.database import Database
from pydt3.apps.devonthink.reminder import Reminder
from pydt3.application import Application

logger = logging.getLogger(__name__)

def check_type(value, type_):
    logger.info(f"Checking {value} against {type_}")
    if type_ is typing.Any:
        return True
    generic_origin = typing.get_origin(type_)
    if generic_origin is not None and generic_origin is list:
        generic_args = typing.get_args(type_)
        assert len(generic_args) == 1, f"Expected 1 generic argument, got {len(generic_args)}"
        return isinstance(value, list) and all(isinstance(e, generic_args[0]) for e in value)
    if generic_origin is not None and generic_origin is typing.Union:
        acceptable_types = typing.get_args(type_)
        return any(check_type(value, acceptable_type) for acceptable_type in acceptable_types)
    else:
        if type_ is float:
            return isinstance(value, int) or isinstance(value, float)
        return isinstance(value, type_)


def _test_obj_properties(obj, skips=()):
    type_ = type(obj)
    print('-=====', locals())
    for name in dir(type_):
        try:
            if name.startswith('_'):
                continue
            if name in skips:
                continue
            if isinstance(getattr(type_, name), property):
                logger.info(f"Testing {obj}.{name}")
                returned_value = getattr(obj, name)
                returned_type = typing.get_type_hints(getattr(type_, name).fget, localns=globals()).get('return', typing.Any)
                assert check_type(returned_value, returned_type), f"Expected {type_}.{name} to be of type {returned_type}, got {returned_value}"
        except NotImplementedError:
            continue
