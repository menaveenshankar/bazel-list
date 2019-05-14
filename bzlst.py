#!/usr/bin/python
from __future__ import print_function
import sys
import re
import os, glob
import argparse
import itertools

regex_rule = '\(\\n.*'


def find_build_files(path):
    return glob.iglob(path + '/**/BUILD', recursive=True)


def extract_rule_name(rule_list):
    # TODO: check if try catch works within list comprehension in py3
    result = []
    for x in rule_list:
        try:
            result.append(x.split('"')[1])
        except:
            pass
    return result


def extract_specific_rule(rule_type, content, option_idx, target_path):
    colour_attrib = lambda x, i: colours[i % len(colours)] + x + default_colour

    # TODO: find a better way to lex+parse, currently super hacky!
    rules = re.findall('{}{}'.format(rule_type, regex_rule), content)
    rule_names = extract_rule_name(rules)

    rule_fmt_disp = [output_format(x, colour_attrib(rule_type[:6], option_idx), target_path) for x in
                     rule_names] if rule_names else []
    return rule_fmt_disp


def extract_bazel_rules(filename, ws_dir, options):
    content = open(filename, 'r').read()
    target_path = '/' + filename.split(ws_dir)[1]

    output_display = [extract_specific_rule(opt, content, i, target_path) for i, opt in enumerate(options)]
    return itertools.chain(*output_display)


def filter_choices(target_choices, type_choices, user_target, user_type):
    all_choices_tuple = itertools.product(target_choices, type_choices)
    all_choices = ['_'.join(list(x)) for x in all_choices_tuple]

    for choice in [user_target, user_type]:
        if choice:
            all_choices = filter(lambda x: choice in x, all_choices)

    return all_choices


if __name__ == '__main__':
    target_choices = ['cc', 'py']
    type_choices = ['binary', 'library']

    parser = argparse.ArgumentParser(
        description='List all bazel targets in the format <target_type>: <target name>: <target path>')
    parser.add_argument("ws_dir")
    parser.add_argument("--target", dest='target', choices=target_choices, required=False)
    parser.add_argument("--type", dest='type', choices=type_choices, required=False)
    args = parser.parse_args()

    all_choices = filter_choices(target_choices, rule_choices, args.target, args.rule)
    all_builds = find_build_files(args.ws_dir)
    