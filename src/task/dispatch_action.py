import argparse
from argparse import ArgumentParser, Namespace


class DispatchAction(argparse.Action):

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values, option_strings= None):
        setattr(namespace, 'command_allowed', self.dest)
        setattr(namespace, 'command_value', values)