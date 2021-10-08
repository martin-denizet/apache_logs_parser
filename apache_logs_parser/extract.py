# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
Module dedicated to extracting more information from log raw data
"""

import re
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

EXTENSION_RE = re.compile(r'\.([A-z0-9]{2,4})$', re.IGNORECASE)


def get_file_extension(url):
    """
    Gets the file extension
    :param url: url/path used by a request. for example:
    `"/images/web/2009/banner.png "`
    :return: The extension of the file hit, if identifiyable. In our example: `"png"`
    Defaults to `None`
    :rtype: str
    """
    extension_match = EXTENSION_RE.search(url)
    if extension_match:
        return extension_match.group(1)
    return None


METHOD_REGEX = re.compile(r"^([A-Z]+) ([^ ]+) (.*)$")


def extract_method_and_url(request):
    """

    :param request:
    .. code-block:: python

        "GET /presentations/logstash-scale11x/images/kibana-dashboard2.png HTTP/1.1"

    :return: dictionary with the information extracted, in our example:
    .. code-block:: python

        {
            'extension': 'png',
            'method': 'GET',
            'path': '/presentations/logstash-scale11x/images/kibana-dashboard2.png',
            'protocol': 'HTTP/1.1',
            'query': '',
            'url': '/presentations/logstash-scale11x/images/kibana-dashboard2.png'
        }

    :rtype: dict[str,str]
    """
    request_match = METHOD_REGEX.search(request)
    method = None
    url = None
    protocol = None
    path = None
    query = None
    if request_match:
        method, url, protocol = request_match.groups()
        url_parts = urlparse(url)
        path = url_parts.path
        query = url_parts.query
    return dict(
        method=method,
        url=url,
        protocol=protocol,
        extension=get_file_extension(url),
        path=path,
        query=query,
    )


BOT_RE = re.compile('.*(Googlebot|bingbot|Twitterbot|YandexBot|bot)', re.IGNORECASE)
DESKTOP_UA_RE = re.compile(
    r'.*(Windows NT \d+\.?\d*|Mac OS [A-z0-9._ ]+|Linux \d+(\.\d+)*)',
    re.IGNORECASE)

MOBILE_UA_RE = re.compile(
    r'.*(iPhone OS \d+(_\d+)*|Android \d+(\.\d+)*|iPad)',
    re.IGNORECASE)


def extract_client_information(user_agent):
    """
    Extracts more information from the user_agent provided by the browser
    :param user_agent: User agent string such as:
    >>> "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a"
    :rtype: dict[str,bool|str]
    """
    is_mobile = False
    is_bot = False
    os_string = 'Unknown'

    if BOT_RE.match(user_agent):
        is_bot = True

    mobile_os_match = MOBILE_UA_RE.match(user_agent)
    if mobile_os_match:
        os_string = mobile_os_match.group(1)
        is_mobile = True
    else:
        desktop_os_match = DESKTOP_UA_RE.match(user_agent)
        if desktop_os_match:
            os_string = desktop_os_match.group(1)
        else:
            logger.debug('OS could not be guessed for UA "{}"'.format(user_agent))

    return dict(
        is_mobile=is_mobile,
        is_bot=is_bot,
        system_agent=os_string,
    )
