# coding=utf-8

"""Command line processing"""


import argparse
from sksurgeryeval import __version__
from sksurgeryeval.ui.sksurgeryeval_demo import run_demo


def main(args=None):
    """Entry point for scikit-surgery-evaluation application"""

    parser = argparse.ArgumentParser(description='scikit-surgery-evaluation')

    ## ADD POSITIONAL ARGUMENTS
    parser.add_argument("-c", "--config",
                        type=str,
                        help="A configuration file",
                        required=True)


    # ADD OPTINAL ARGUMENTS

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output",
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgery-evaluation version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.config, args.verbose)
