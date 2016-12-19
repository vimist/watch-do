import glob
import importlib
import argparse
import os


def list_methods():
    files = os.listdir(os.path.join(os.path.dirname(__file__), 'methods/'))
    methods = []
    for f in files:
        if f.endswith('.py') and f not in ['base_method.py']:
            methods.append(f[0:-3])

    return methods


def string_to_method_class(cls_name):
    try:
        method_module = importlib.import_module('watch_do.methods.'+cls_name)
        cls = getattr(method_module, cls_name.title())
        return cls
    except ImportError:
        raise argparse.ArgumentTypeError(cls_name+' is not a valid method')


def string_to_bool(string):
    string_lower = string.lower()
    if string_lower in ['true', 't', 'yes', 'y']:
        return True
    elif string_lower in ['false', 'f', 'no', 'n']:
        return False
    else:
        raise argparse.ArgumentTypeError(
            'must be one of the following: '
            'true, false, t, f, yes, no, y, n'
        )
