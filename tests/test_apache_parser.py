import os
import unittest
from datetime import datetime, timezone
from apache_logs_parser.parser import parse_line, parse_date, parse_log_file, generate_output_dict, \
    extract_client_information

current_dir = os.path.dirname(os.path.realpath(__file__))


class TestApacheParser(unittest.TestCase):
    def test_parse_image_hit(self):
        self.assertEqual(
            {'bytes': 203023,
             'extension': 'png',
             'is_bot': False,
             'is_mobile': False,
             'log_name': '-',
             'method': 'GET',
             'path': '/presentations/logstash-monitorama-2013/images/kibana-search.png',
             'protocol': 'HTTP/1.1',
             'query': '',
             'referrer': 'http://semicomplete.com/presentations/logstash-monitorama-2013/',
             'remote_ip': '83.149.9.216',
             'request': 'GET '
                        '/presentations/logstash-monitorama-2013/images/kibana-search.png '
                        'HTTP/1.1',
             'status': 200,
             'system_agent': 'Mac OS X 10_9_1',
             'time': '2015-05-17T10:05:03+00:00',
             'url': '/presentations/logstash-monitorama-2013/images/kibana-search.png',
             'user': '-',
             'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 '
                           'Safari/537.36'},
            parse_line(
                '''83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"'''
            ))

    def test_file_bot_hit(self):
        self.assertEqual(
            {'bytes': 235,
             'extension': 'py',
             'is_bot': True,
             'is_mobile': False,
             'log_name': '-',
             'method': 'GET',
             'path': '/scripts/grok-py-test/configlib.py',
             'protocol': 'HTTP/1.1',
             'query': '',
             'referrer': '-',
             'remote_ip': '46.118.127.106',
             'request': 'GET /scripts/grok-py-test/configlib.py HTTP/1.1',
             'status': 200,
             'system_agent': 'Unknown',
             'time': '2015-05-20T12:05:17+00:00',
             'url': '/scripts/grok-py-test/configlib.py',
             'user': '-',
             'user_agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; '
                           '+http://www.google.com/bot.html'},
            parse_line(
                '''46.118.127.106 - - [20/May/2015:12:05:17 +0000] "GET /scripts/grok-py-test/configlib.py HTTP/1.1" 200 235 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html"'''
            ))

    def test_bot_redirection(self):
        self.assertEqual(
            {'bytes': 0,
             'extension': 'png',
             'is_bot': False,
             'is_mobile': False,
             'log_name': '-',
             'method': 'GET',
             'path': '/images/googledotcom.png',
             'protocol': 'HTTP/1.1',
             'query': '',
             'referrer': '-',
             'remote_ip': '112.110.247.238',
             'request': 'GET /images/googledotcom.png HTTP/1.1',
             'status': 304,
             'system_agent': 'Unknown',
             'time': '2015-05-17T12:05:27+00:00',
             'url': '/images/googledotcom.png',
             'user': '-',
             'user_agent': 'Maui Browser'},
            parse_line(
                '''112.110.247.238 - - [17/May/2015:12:05:27 +0000] "GET /images/googledotcom.png HTTP/1.1" 304 - "-" "Maui Browser"'''
            ))


class TestSupportParsers(unittest.TestCase):
    def test_datetime(self):
        self.assertEqual(parse_date(
            '17/May/2015:10:05:03 +0000'
        ), datetime(2015, 5, 17, 10, 5, 3, tzinfo=timezone.utc))


class TestParseFile(unittest.TestCase):

    def test_parse_file(self):
        self.assertEqual(
            30,
            len(parse_log_file(os.path.join(current_dir, 'access.log')))
        )


if __name__ == '__main__':
    unittest.main()
