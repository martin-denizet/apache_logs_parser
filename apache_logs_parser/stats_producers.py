# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
import http.client
from collections import defaultdict

from apache_logs_parser.colors import header, Colors
from apache_logs_parser.display import Graph, TopList, size_format


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

    def display(self):
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

    def display(self):
        Graph.display(self.counts, 'Hit types', show_percents=False)


class ResponseCount(StatProducer):
    """
       Count hits
       """

    def set_up(self):
        self.response_code = defaultdict(int)

    def process_entry(self, data_entry):
        self.response_code[str(data_entry['response'])] += 1

    def get_metrics(self):
        return dict(
            responde_codes=self.response_code
        )

    def display(self):
        Graph.display(self.response_code, 'Response codes')


class StatHitPerSystemAgent(StatProducer):
    """
    Hits per system agent
    """

    def set_up(self):
        # Dictionary with a default value of 0 for each new key
        self.hits_per_system_agent = defaultdict(lambda: 0)

    def process_entry(self, data_entry):
        self.hits_per_system_agent[data_entry['system_agent']] += 1

    def get_metrics(self):
        return dict(
            hits_per_page=self.hits_per_system_agent
        )

    def display(self):
        Graph.display(self.hits_per_system_agent, "Hits per OS")


class StatPageIssues(StatProducer):
    """
    identifies URLs with response codes >= 400
    """

    def set_up(self):
        self.urls_per_response_code = defaultdict(lambda: defaultdict(lambda: 0))

    def process_entry(self, data_entry):
        response = data_entry['response']
        if response >= 400:
            self.urls_per_response_code[response][data_entry['url']] += 1

    def get_metrics(self):
        return dict(
            hits_per_page=self.urls_per_response_code
        )

    def display(self):
        header("Pages giving response codes >= 400")

        self.urls_per_response_code = dict(sorted(self.urls_per_response_code.items(), key=lambda x: x[0]))
        for k, v in self.urls_per_response_code.items():
            response_string = http.client.responses.get(k, 'Unknown')
            print(
                f"    {Colors.UNDERLINE + Colors.OKCYAN}Responde code {k} \"{response_string}\","
                f" total: {sum(v.values())}{Colors.ENDC}")
            v = dict(sorted(v.items(), key=lambda x: x[1], reverse=True))
            for url, counts in v.items():
                print(f"        {Colors.OKGREEN}{counts} hits{Colors.ENDC}: {url}")


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

    def display(self):
        TopList.display(self.hits_per_page, "Most visited pages")


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

    def display(self):
        size_by_extension = {k: v['bytes'] for k, v in self.per_extension.items()}
        TopList.display(size_by_extension, "Traffic size by extension", unit='bytes')


class StatPerIp(StatProducer):
    """
    Count number of hits and total byte size by IP
    """

    def set_up(self):
        # Create a dictionary of dictionaries containing integers
        self.per_ip = defaultdict(lambda: defaultdict(lambda: 0))

    def process_entry(self, data_entry):
        self.per_ip[data_entry['remote_ip']]['bytes'] += data_entry['bytes']
        self.per_ip[data_entry['remote_ip']]['hits'] += 1

    def get_metrics(self):
        return dict(
            per_ip=self.per_ip
        )

    def display(self):
        size_by_extension = {k: v['bytes'] for k, v in self.per_ip.items()}
        TopList.display(size_by_extension, "Traffic size by IP", unit='bytes')


class StatTotals(StatProducer):
    """
    Makes totals
    """

    def set_up(self):
        # Create a dictionary of dictionaries containing integers
        self.total_size = 0
        self.total_hits = 0
        self.different_visitors = set()
        self.pages_visited = 0

    def process_entry(self, data_entry):
        self.total_size += data_entry['bytes']
        self.total_hits += 1
        if data_entry['extension'] in {None, 'html'}:
            self.different_visitors.add(data_entry['remote_ip'])
            self.pages_visited += 1

    def get_metrics(self):
        return dict(
            total_size=self.total_size,
            total_hits=self.total_hits,
            different_visitors=list(self.different_visitors),
            pages_visited=self.pages_visited,
        )

    def display(self):
        header("Totals")
        print(f"    Total log entries: {self.total_hits}")
        print(f"    Total : {size_format(self.total_size)}")
        print(f"    Number of different visitors : {len(self.different_visitors)}")
        print(f"    Number of pages visited : {self.pages_visited}")
        print(f"    Average pages visited per visitor : {self.pages_visited / len(self.different_visitors):.2f}")


def get_stats_classes():
    return StatProducer.__subclasses__()


def get_stats_classes_names():
    return [c.__name__ for c in get_stats_classes()]


def get_stat_classes_by_name(name):
    for c in get_stats_classes():
        if name == c.__name__:
            return c
    raise ValueError(f"Could not find stats class {name}")
