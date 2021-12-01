# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import re
import logging
import json
from datetime import datetime

from apache_logs_parser.extract import extract_method_and_url, extract_client_information

logger = logging.getLogger(__name__)

# Log use CLF: Common Log Format
# LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined

# - %h	Remote hostname. Will log the IP address if HostnameLookups is set to Off, which is the default.
# If it logs the hostname for only a few hosts, you probably have access control directives mentioning them by name
REMOTE_HOSTNAME_RE = r"(?P<remote_ip>\d+\.\d+\.\d+\.\d+)"
# - %l Remote logname (from identd, if supplied).
# This will return a dash unless mod_ident is present and IdentityCheck is set On.
REMOTE_LOGNAME_RE = r"(-)"
# - %u Remote user if the request was authenticated. May be bogus if return status (%s) is 401 (unauthorized).
REMOTE_USER_RE = r"(-)"
# - %t Time the request was received, in the format [18/Sep/2011:19:18:28 -0400].
# The last number indicates the timezone offset from GMT
TIME_RE = r"\[(?P<time>[^\]]+)\]"
# - %r First line of request.
REQUEST_RE = r'"(?P<request>[^\"]+)"'
# - %>s Status. For requests that have been internally redirected, this is the status of the original request.
# Use %>s for the final status.
STATUS_RE = r"(?P<response>\d+)"
# - %b Size of response in bytes, excluding HTTP headers.
# In CLF format, i.e. a '-' rather than a 0 when no bytes are sent.
BYTES_SIZE_RE = r"(?P<bytes>\d+|\-)"
# - Referer
REFERER_RE = r'"(?P<referrer>[^\"]+)"'
# - User-agent
USER_AGENT_RE = r'"(?P<user_agent>[^\"]+)"'

# Put the pieces in the right order as per Apache configuration
LOG_LINE_PATTERN = " ".join([REMOTE_HOSTNAME_RE,
                             REMOTE_LOGNAME_RE,
                             REMOTE_USER_RE,
                             TIME_RE,
                             REQUEST_RE,
                             STATUS_RE,
                             BYTES_SIZE_RE,
                             REFERER_RE,
                             USER_AGENT_RE
                             ])

REGEX = re.compile(f"^{LOG_LINE_PATTERN}$")


def parse_log_file(file_name):
    """
    Open a file and create a list of dictionaries with each line as a dict
    :param file_name: File name as a string
    :rtype: [dict]
    """
    data = []
    with open(file_name, 'r') as fh:
        for line in fh:
            line_data = parse_line(line.strip())
            if line_data:
                data.append(line_data)
    logger.info(f"Read {len(data)} lines from file {file_name}")
    return data


def parse_line(line):
    """
    Convert a string log line into a dict
    :param line: Apache log line
    :rtype: dict|False
    """
    match = REGEX.search(line)
    if match:
        data = match.groupdict()

        data['time'] = parse_date(data['time']).isoformat()
        data['response'] = parse_int(data['response'])
        data['bytes'] = parse_int(data['bytes'])

        data.update(extract_method_and_url(data['request']))
        data.update(extract_client_information(data['user_agent']))

        return data

    logger.error(f'Could not understand line "{line}"')
    return False


def parse_int(int_string):
    """
    Log values are returned in string and empty fields are replaced with an hyphen.
    We want to be sure to have an integer as an output
    :param int_string: Integer as a string or "-"
    :rtype: int
    """
    if int_string == '-':
        int_string = 0
    return int(int_string)


def parse_date(date_string):
    """
    Converts Apache log datetime into Python datetime object
    :param date_string: Apache datetime string such as:
    `"17/May/2015:10:05:19 +0000"`
    :return: datetime instance
    :rtype: datetime
    """
    return datetime.strptime(date_string, "%d/%b/%Y:%H:%M:%S %z")


def generate_data_from_log(input_files):
    """
    Return a list dictionaries from one or many Apache file
    :param input_files: List of Apache log files names
    :type input_files: list|str|bytes
    :return: List of dictionaries
    """
    if type(input_files) in frozenset([str, bytes]):
        input_files = [input_files]
    data = []
    for file in input_files:
        data = data + parse_log_file(file)
    return data


def write_json_log(input_files, output_file):
    """
    Create a JSON log file from a list of Apache log files name
    :param input_files: List of input files name
    :param output_file: File name to write the JSON log to
    :return:
    """
    with open(output_file, 'w') as f:
        json.dump(
            generate_data_from_log(input_files),
            f, indent=4)
        logger.info(f"Wrote output to file {output_file}")
