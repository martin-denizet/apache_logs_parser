# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from collections import defaultdict


class StatProducer(object):
    """
    Base class for classes producing statistics.
    """

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self):
        self.set_up()

    def set_up(self):
        """
        Initialize the producer, variables can be declarer
        """
        raise NotImplementedError()

    def process_entry(self, data_entry):
        """
        :param data_entry: Apache log line as a dict
        :type data_entry: dict
        """
        raise NotImplementedError()

    def get_metrics(self):
        """
        Returns as a dict the statistics produced
        :rtype: dict
        """
        raise NotImplementedError()


class StatCount(StatProducer):
    """
    Count hits
    """

    def set_up(self):
        self.counts = dict(
            hits=0,
            bot_hits=0,
            mobile_hits=0,
            desktop_hits=0,
        )

    def process_entry(self, data_entry):
        self.counts['hits'] += 1
        if data_entry['is_bot']:
            self.counts['bot_hits'] += 1
        if data_entry['is_mobile']:
            self.counts['mobile_hits'] += 1
        if not data_entry['is_mobile']:
            self.counts['desktop_hits'] += 1

    def get_metrics(self):
        return self.counts


class StatHitPerPage(StatProducer):
    """
    Hits per page
    """

    def set_up(self):
        # Dictionary with a default value of 0 for each new key
        self.hits_per_page = defaultdict(lambda: 0)

    def process_entry(self, data_entry):
        if data_entry['extension'] is None:
            self.hits_per_page[data_entry['path']] += 1

    def get_metrics(self):
        return dict(
            hits_per_page=self.hits_per_page
        )


class StatPerExtension(StatProducer):
    """
    Count number of hits and total byte size by file extension
    """

    def set_up(self):
        self.per_extension = defaultdict(lambda: defaultdict(lambda: 0))

    def process_entry(self, data_entry):
        self.per_extension[data_entry['extension']]['bytes'] += data_entry['bytes']
        self.per_extension[data_entry['extension']]['hits'] += 1

    def get_metrics(self):
        return dict(
            per_extension=self.per_extension
        )


class StatPerIp(StatProducer):
    """
    Count number of hits and total byte size by IP
    """

    def set_up(self):
        self.per_ip = defaultdict(lambda: defaultdict(lambda: 0))

    def process_entry(self, data_entry):
        self.per_ip[data_entry['remote_ip']]['bytes'] += data_entry['bytes']
        self.per_ip[data_entry['remote_ip']]['hits'] += 1

    def get_metrics(self):
        return dict(
            per_ip=self.per_ip
        )


def get_stats(data, stats_classes=None):
    """
    Produces statistics on the data in argument.
    :param data: List of dicts extracted from apache logs
    :param stats_classes: List of stats classes to use to produce stats on the data.
    if left empty, all classes will be used
    :return: dictionary of statistics
    :rtype: dict
    """
    if stats_classes is None:
        stats_classes = [StatCount(), StatHitPerPage(), StatPerExtension(), StatPerIp()]

    stats = dict()
    for data_entry in data:
        if not data_entry:
            continue
        for stat in stats_classes:
            stat.process_entry(data_entry)

    for stat in stats_classes:
        stats.update(stat.get_metrics())

    return stats
