# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


import argparse
import logging
from apache_logs_parser import actions
from apache_logs_parser.parser import write_json


def main():
    parser = argparse.ArgumentParser(description="Tool to parse apache logs")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument(dest='apache_log_files', type=argparse.FileType('r'), help="Input apache log input_files",
                        nargs='+')
    parser.add_argument('-o', '--output-json', type=argparse.FileType('w'), help="Output path of the JSON file")

    parser.add_argument("-a", "--action", type=str, choices=actions.ACTIONS, default=actions.CONVERT_AND_STATS,
                        help="Action to perform")

    args = parser.parse_args()

    process_args(args)


def process_args(args):
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    data = write_json([f.name for f in args.apache_log_files],
                      args.output_json.name,
                      generate_stats=args.action in (actions.CONVERT_AND_STATS, actions.STATS),
                      include_log_entries=args.action in (actions.CONVERT_AND_STATS, actions.CONVERT),
                      )


if __name__ == '__main__':
    main()
