#!/usr/bin/python
from __future__ import print_function
import sys
import re
import os, glob
import argparse


if __name__ == '__main__':
    target_choices = ['cc', 'py']
    type_choices = ['binary', 'library']

    parser = argparse.ArgumentParser(
        description='List all bazel targets in the format <target_type>: <target name>: <target path>')
    parser.add_argument("ws_dir")
    parser.add_argument("--target", dest='target', choices=target_choices, required=False)
    parser.add_argument("--type", dest='type', choices=type_choices, required=False)
    args = parser.parse_args()
