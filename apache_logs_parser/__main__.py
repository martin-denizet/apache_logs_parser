# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import argparse
import logging
from apache_logs_parser import commands, __version__
from apache_logs_parser.parser import write_json_log
from apache_logs_parser.stats import generate_stats, display_stats, write_json_stats
from apache_logs_parser.stats_producers import get_stat_classes_by_name, get_stats_classes_names


def main():
    """
    Entrypoint for processing command line arguments
    """
    parser = argparse.ArgumentParser(description="Tool to parse apache logs")
    parser.add_argument("--version", help="Display tool version",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity",
                        action="store_true")

    # We parse args now because if we only want to know the version, we don't need to go further and add
    # required arguments
    known_args, unknown_args = parser.parse_known_args()
    if known_args.version:
        print(__version__)
        # stop processing arguments
        return

    # Sub-parser for each command
    command_parser = parser.add_subparsers(dest='command', help='command', required=True)

    # Parser for converting Apache log file files into JSON
    convert_parser = command_parser.add_parser(commands.CONVERT, help='Convert Apache log files into JSON')
    convert_parser.add_argument(dest='apache_log_files', type=argparse.FileType('r'),
                                help="Input apache log input_files",
                                nargs='+')
    convert_parser.add_argument('-o', '--output-json', type=argparse.FileType('w'),
                                default='log.json', help="Output path of the JSON file")

    # Parser for displaying statistics
    stat_parser = command_parser.add_parser(commands.STATS, help='Display Apache statistics based on JSON files')
    stat_parser.add_argument(dest='json_logs', type=argparse.FileType('r'),
                             help="Input apache log input_files",
                             nargs='+')

    # Allow the user to save stats_instances computed, to use in a BI solution for example
    stat_parser.add_argument('-o', '--output-json', type=argparse.FileType('w'),
                             help="Save raw stats_instances in a JSON file",
                             required=False
                             )
    stat_parser.add_argument('--no-display', action='store_true', help="Do not display the stats_instances")

    # Allow the user to specify which stats_instances are computed/displayed
    stat_parser.add_argument('--stat-classes', choices=get_stats_classes_names(),
                             default=get_stats_classes_names(),
                             nargs='+', help="Name of the stats_instances producers to use, uses all by default")

    # Read the values from the command line
    args = parser.parse_args()

    # Process arguments from the command line
    process_args(args)


def process_args(args):
    """
    Processing arguments provided by argparse
    """

    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    # Convert command
    if args.command == commands.CONVERT:
        write_json_log(
            [f.name for f in args.apache_log_files],
            args.output_json.name,
        )

    # Stats command
    if args.command == commands.STATS:
        # We get only the stats_instances producer we want
        stats_instances = generate_stats(
            [f.name for f in args.json_logs],
            [get_stat_classes_by_name(c) for c in args.stat_classes]
        )
        # Do we want to display the stats?
        if not args.no_display:
            display_stats(stats_instances)

        # Do we wat to save the stats to a JSON file
        if args.output_json:
            write_json_stats(
                stats_instances,
                args.output_json.name
            )


# If the file is executed, not imported
if __name__ == '__main__':
    main()
