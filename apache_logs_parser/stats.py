# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import logging

from apache_logs_parser.stats_producers import get_stats_classes

logger = logging.getLogger(__name__)


def get_stats(data, stats_classes=None):
    """
    Create StatProducer instances from StatProducer classes and
    produce statistics from the data in argument.
    :param data: List of dicts extracted from apache logs
    :param stats_classes: List of stats_instances classes to use to produce stats_instances on the data.
    if left empty, all classes will be used
    :return: dictionary of statistics
    :rtype: dict
    """
    if stats_classes is None:
        stats_classes = get_stats_classes()

    # Instanciate all classes
    stats_instances = [c() for c in stats_classes]
    # For each entry in the data log
    for data_entry in data:
        if not data_entry:
            # Log line was not parsed correctly
            continue
        # Generate stats for all StatProducer instances
        for stat in stats_instances:
            stat.process_entry(data_entry)

    return stats_instances


def generate_stats(input_files, stats_classes=None):
    """
    Read log data from JSON files and compute the statistics from the data.
    :param input_files: List of JSON file names
    :param stats_classes: List of StatProducer subclasses to instanciate to produce stats or None,
    if set to None, it all StatProducer subclasses will be used
    :return: A list of StatProducer with data computed
    """
    if type(input_files) in frozenset([str, bytes]):
        input_files = [input_files]
    data = []
    for file in input_files:
        with open(file, 'r') as f:
            data = data + json.load(f)
    return get_stats(data, stats_classes)


def generate_json_stats(stats_instances):
    """
    Generate a dictionary of statistics from StatProducers subclasses instances.
    This presumes that the instances have been fed data.
    """
    stats = dict()
    for stat in stats_instances:
        stats.update(stat.get_metrics())
    return stats


def display_stats(stats_instances):
    for stat in stats_instances:
        stat.display()


def write_json_stats(stats_instances, stats_json_file_name):
    """
    Write stats to JSON file for processing by a 3rd party software like a BI solution.
    :param stats_instances: List of StatProducer subclasses instances. Data must have been fed in the instances.
    :param stats_json_file_name: Name of the file to write to
    """
    output_data = dict()
    for stat in stats_instances:
        output_data.update(stat.get_metrics())
    with open(stats_json_file_name, 'w') as stats_json_file:
        json.dump(
            output_data,
            stats_json_file, indent=4)
        logger.info(f"Wrote stats_instances to file {stats_json_file_name}")
