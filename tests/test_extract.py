import os
import unittest

from apache_logs_parser.extract import get_file_extension, extract_client_information, extract_method_and_url

current_dir = os.path.dirname(os.path.realpath(__file__))


class TestExtractors(unittest.TestCase):
    def test_image_extension(self):
        self.assertEqual(
            get_file_extension("/images/web/2009/banner.png"),
            'png'
        )

    def test_page_extension(self):
        self.assertEqual(
            get_file_extension("/articles/dynamic-dns-with-dhcp/"),
            None
        )

    def test_extract_method_and_url(self):
        self.assertEqual(
            {'extension': 'png',
             'method': 'GET',
             'path': '/presentations/logstash-scale11x/images/kibana-dashboard2.png',
             'protocol': 'HTTP/1.1',
             'query': '',
             'url': '/presentations/logstash-scale11x/images/kibana-dashboard2.png'},
            extract_method_and_url("GET /presentations/logstash-scale11x/images/kibana-dashboard2.png HTTP/1.1")
        )

    def test_iphone_emulator(self):
        self.assertEqual(
            {'is_bot': True, 'is_mobile': True, 'os_string': 'iPhone OS 6_0'},
            extract_client_information(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            )
        )

    def test_iphone(self):
        self.assertEqual(
            {'is_bot': False, 'is_mobile': True, 'os_string': 'iPhone OS 7_0_4'},
            extract_client_information(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a"
            )
        )


if __name__ == '__main__':
    unittest.main()
