# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
import logging
import json
from datetime import datetime

from apache_logs_parser.extract import extract_method_and_url, extract_client_information
from apache_logs_parser.stats import get_stats

logger = logging.getLogger(__name__)
# Log use CLF: Common Log Format
# LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined
# - %h	Remote hostname. Will log the IP address if HostnameLookups is set to Off, which is the default. If it logs the hostname for only a few hosts, you probably have access control directives mentioning them by name
REMOTE_HOSTNAME_RE = r"(\d+\.\d+\.\d+\.\d+)"
# - %l Remote logname (from identd, if supplied). This will return a dash unless mod_ident is present and IdentityCheck is set On.
REMOTE_LOGNAME_RE = r"(-)"
# - %u Remote user if the request was authenticated. May be bogus if return status (%s) is 401 (unauthorized).
REMOTE_USER_RE = r"(-)"
# - %t Time the request was received, in the format [18/Sep/2011:19:18:28 -0400]. The last number indicates the timezone offset from GMT
TIME_RE = r"\[([^\]]+)\]"
# - %r First line of request.
REQUEST_RE = r'"([^\"]+)"'
# - %>s Status. For requests that have been internally redirected, this is the status of the original request. Use %>s for the final status.
STATUS_RE = r"(\d+)"
# - %b Size of response in bytes, excluding HTTP headers. In CLF format, i.e. a '-' rather than a 0 when no bytes are sent.
BYTES_SIZE_RE = r"(\d+|\-)"
# - Referer
REFERER_RE = r'"([^\"]+)"'
# - User-agent
USER_AGENT_RE = r'"([^\"]+)"'

REGEX = re.compile("^{} {} {} {} {} {} {} {} {}$".format(REMOTE_HOSTNAME_RE,
                                                         REMOTE_LOGNAME_RE,
                                                         REMOTE_USER_RE,
                                                         TIME_RE,
                                                         REQUEST_RE,
                                                         STATUS_RE,
                                                         BYTES_SIZE_RE,
                                                         REFERER_RE,
                                                         USER_AGENT_RE
                                                         ))


def parse_log_file(file_name):
    data = []
    with open(file_name, 'r') as fh:
        for line in fh:
            line_data = parse_line(line.strip())
            if line_data:
                data.append(line_data)
    logger.info("Read {} lines from file {}".format(len(data), file_name))
    return data


def parse_line(line):
    match = REGEX.search(line)
    if match:
        remote_ip, log_name, user, time, request, status, bytes, referrer, user_agent = match.groups()

        if bytes == '-':
            bytes = 0

        data = dict(
            remote_ip=remote_ip,
            log_name=log_name,
            user=user,
            time=parse_date(time).isoformat(),
            request=request,
            status=int(status),
            bytes=int(bytes),
            referrer=referrer,
            user_agent=user_agent,
        )
        data.update(extract_method_and_url(request))
        data.update(extract_client_information(user_agent))

        return data

    logger.warning('Could not understand line "{}"'.format(line))
    return False


def parse_date(date_string):
    """
    Converts Apache log datetime into Python datetime object
    :param date_string: Apache datetime string such as:
    `"17/May/2015:10:05:19 +0000"`
    :return: datetime instance
    :rtype: datetime
    """
    return datetime.strptime(date_string, "%d/%b/%Y:%H:%M:%S %z")


def generate_output_dict(input_files, generate_stats=False, include_log_entries=True):
    output_data = dict()
    if type(input_files) in frozenset([str, bytes]):
        input_files = [input_files]
    data = []
    for file in input_files:
        data = data + parse_log_file(file)
    if generate_stats:
        output_data.update(dict(stats=get_stats(data)))
    if include_log_entries:
        output_data.update(dict(data=data))

    return output_data


def write_json(input_files, output_file, generate_stats=False, include_log_entries=True):
    with open(output_file, 'w') as f:
        json.dump(
            generate_output_dict(input_files, generate_stats=generate_stats, include_log_entries=include_log_entries),
            f, indent=4)
        logger.info("Wrote output to file {}".format(output_file))
