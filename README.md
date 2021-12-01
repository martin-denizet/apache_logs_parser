# apache_logs_parser

__This is an example tool developed as a project during Python classes. It was not meant to be used in the _"real
world"_.__

This tool converts standard Apache web server combined logs into Python objects to produce stats and to allow optionally
to save the results in a JSON file to be processed by a 3rd party tool like BI solution.

## Requirements

* Linux
* Python >= 3.7

## Install

### Install from git

```shell
pip install --user  git+https://github.com/martin-denizet/apache_logs_parser.git
# Test the installation
apache_logs_parser --version
```

### Install a specific version

Replace `0.1.0` with the version number you wish. See releases on GitHub to know versions available.

```shell
pip install --user -e git+https://github.com/martin-denizet/apache_logs_parser.git@0.1.0
# Test the installation
apache_logs_parser --version
```

# Usage

```shell
# Using the entrypoint, available if ~/.local/bin added to to $PATH
# if you need it added to the PATH, you can try: echo "export PATH=\"$PATH:~/.local/bin\" >> ~/.bashrc" 
apache_logs_parser -h
# Otherwise you can call it as a module:
python3 -m apache_logs_parser -h
```

## Convert Apache logs file to JSON

Takes as input an Apache combined log and converts it into a JSON file.

### Apache Log

Supported format:

```apacheconf
# Common Log Format
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined
```

Sample line:

```shell
93.114.45.13 - - [17/May/2015:10:05:14 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"
```

### JSON format

The JSON file is a list of dictionary, each Apache log line is converted to a dictionary. Single entry example:

```json
[
  {
    "remote_ip": "83.149.9.216",
    "time": "2015-05-17T10:05:03+00:00",
    "request": "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1",
    "response": 200,
    "bytes": 203023,
    "referrer": "http://semicomplete.com/presentations/logstash-monitorama-2013/",
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
    "method": "GET",
    "url": "/presentations/logstash-monitorama-2013/images/kibana-search.png",
    "protocol": "HTTP/1.1",
    "extension": "png",
    "path": "/presentations/logstash-monitorama-2013/images/kibana-search.png",
    "query": "",
    "is_mobile": false,
    "is_bot": false,
    "system_agent": "Mac OS X 10_9_1"
  }
]
```

### Examples

```shell
python3 -m apache_logs_parser convert tests/access.big.log --output-json apache-log.json
```

Note: Usage of `nice` is recommended for usage on production machines. Create JSON log data file from several files
using a wildcard or listing several files:

```shell
python3 -m apache_logs_parser convert *.log --output-json apache-log.json
```

## Display statistics from a JSON file

### Examples

```shell
# Target a json file generated with the `apache_logs_parser convert` command
python3 -m apache_logs_parser stats apache-log.json
```

Output contains:

* Details on page hits
* Response codes
* Hits per OS
* Pages giving a response code >= 400
* Top most visited pages
* Top most bandwidth consuming file extensions
* Top traffic per IP
* Unique visitors
* Average pages visited per visitor

<details>
  <summary>Sample output</summary>

``` 
Hit types
    hits        |████████████████████████████████████████████████████████████████████████████████████████████████████ : 9999 hits
    desktop_hits|██████████████████████████████████████████████████████████████████████████████████████████████▎ : 9426 hits
    bot_hits    |███████████▊ : 1170 hits
    mobile_hits |█████▊ : 573 hits
Response codes
    200|████████████████████████████████████████████████████████████████████████████████████████████████████ : 9125 hits/ 91.26%
    304|████▉ : 445 hits/ 4.45%
    404|██▍ : 213 hits/ 2.13%
    301|█▊ : 164 hits/ 1.64%
    206|▌ : 45 hits/ 0.45%
    500| : 3 hits/ 0.03%
    403| : 2 hits/ 0.02%
    416| : 2 hits/ 0.02%
Hits per OS
    Unknown        |████████████████████████████████████████████████████████████████████████████████████████████████████ : 4715 hits/ 47.15%
    Windows NT 6.1 |██████████████████████████████████████████████▉ : 2211 hits/ 22.11%
    Mac OS X 10_9_1|██████████████▋ : 692 hits/ 6.92%
    Windows NT 5.1 |██████████▍ : 488 hits/ 4.88%
    Mac OS X 10.7  |██████▍ : 301 hits/ 3.01%
    iPhone OS 6_0  |█████▊ : 274 hits/ 2.74%
    Windows NT 6.3 |█████▋ : 266 hits/ 2.66%
    Mac OS X 10.9  |███▎ : 153 hits/ 1.53%
    Windows NT 5.2 |██▉ : 138 hits/ 1.38%
    Windows NT 6.2 |██▍ : 112 hits/ 1.12%
    Mac OS X 10_8_5|█▉ : 86 hits/ 0.86%
    Android 4.4.2  |█▍ : 63 hits/ 0.63%
    iPad           |█▎ : 61 hits/ 0.61%
    iPhone OS 7_0_4|█▎ : 59 hits/ 0.59%
    Windows NT 6.0 |▊ : 37 hits/ 0.37%
    Mac OS X 10_7_5|▊ : 35 hits/ 0.35%
    Android 4.1.2  |▊ : 33 hits/ 0.33%
    Mac OS X 10.8  |▋ : 32 hits/ 0.32%
    Windows NT 5.0 |▌ : 26 hits/ 0.26%
    Mac OS X 10_9_0|▌ : 26 hits/ 0.26%
    Windows NT 9.0 |▌ : 23 hits/ 0.23%
    Mac OS X 10.6  |▌ : 22 hits/ 0.22%
    Mac OS X 10_7_1|▌ : 21 hits/ 0.21%
    Android 4.3    |▍ : 20 hits/ 0.20%
    Mac OS X 10_6_8|▎ : 14 hits/ 0.14%
    Mac OS X 10_8_4|▎ : 12 hits/ 0.12%
    Android 4.0.4  |▎ : 11 hits/ 0.11%
    Android 2.3.6  |▎ : 11 hits/ 0.11%
    Android 4.2.2  |▎ : 10 hits/ 0.10%
    Mac OS X 10.5  |▏ : 6 hits/ 0.06%
    Mac OS X 10_8_2|▏ : 5 hits/ 0.05%
    iPhone OS 5_1_1|▏ : 5 hits/ 0.05%
    iPhone OS 6_1_3|▏ : 4 hits/ 0.04%
    Android 4.1.1  |▏ : 4 hits/ 0.04%
    Android 2.3.5  |▏ : 3 hits/ 0.03%
    iPhone OS 6_1_4| : 2 hits/ 0.02%
    iPhone OS 6_1_5| : 2 hits/ 0.02%
    Android 2.3.7  | : 2 hits/ 0.02%
    Mac OS X 10_7_3| : 2 hits/ 0.02%
    iPhone OS 7_0_3| : 2 hits/ 0.02%
    Android 2.3.4  | : 1 hits/ 0.01%
    Mac OS X 10_9_2| : 1 hits/ 0.01%
    iPhone OS 7_0_5| : 1 hits/ 0.01%
    iPhone OS 6_1_2| : 1 hits/ 0.01%
    Mac OS X 10_7_4| : 1 hits/ 0.01%
    iPhone OS 6_1  | : 1 hits/ 0.01%
    Android 4.0.3  | : 1 hits/ 0.01%
    Mac OS X 10_5_8| : 1 hits/ 0.01%
    Android 4.2.1  | : 1 hits/ 0.01%
    iPhone OS 5_0_1| : 1 hits/ 0.01%
Pages giving response codes >= 400
    Responde code 403 "Forbidden", total: 2
        1 hits: /presentations/vim/+++++++++++++++++++++++++++++++++++Result:+%E8%F1%EF%EE%EB%FC%E7%EE%E2%E0%ED+%ED%E8%EA%ED%E5%E9%EC+%22newkoversjup%22;+ReCaptcha+%E4%E5%F8%E8%F4%F0%EE%E2%E0%ED%E0;+%28JS%29;+%E7%E0%F0%E5%E3%E8%F1%F2%F0%E8%F0%EE%E2%E0%EB%E8%F1%FC;+%ED%E5+%ED%E0%F8%EB%EE%F1%FC+%F4%EE%F0%EC%FB+%E4%EB%FF+%EE%F2%EF%F0%E0%E2%EA%E8;+Result:+%EE%F8%E8%E1%EA%E0:+%22i+never+really+liked+c%27s+assert%28%29+feature.+if+an+assertion+is+violated,+it%27lltell+you+what+assertion+failed+but+completely+lacks+any+context:%22;+%ED%E5+%ED%E0%F8%EB%EE%F1%FC+%F4%EE%F0%EC%FB+%E4%EB%FF+%EE%F2%EF%F0%E0%E2%EA%E8;
        1 hits: /svnweb/xpathtool/
    Responde code 404 "Not Found", total: 213
        61 hits: /files/logstash/logstash-1.3.2-monolithic.jar
        32 hits: /presentations/logstash-puppetconf-2012/images/office-space-printer-beat-down-gif.gif
        6 hits: /wp-login.php
        6 hits: /wp-login.php?action=register
        6 hits: /blog/wp-admin/
        6 hits: /wp-admin/
        6 hits: /wp/wp-admin/
        5 hits: /wordpress/wp-admin/
        4 hits: /administrator/
        4 hits: /admin.php
        4 hits: /image/logstash.png
        3 hits: /apple-touch-icon.png
        3 hits: /browserconfig.xml
        3 hits: /blog/geekery/pyblosxom-mdate-vim-hack.html/trackback/
        2 hits: /administrator/index.php
        2 hits: /apple-touch-icon-precomposed.png
        2 hits: /geekery/find-that-lost-screen-session.html
        2 hits: /projects/xdotool/xdotool
        2 hits: /presentations/logstash-puppetconf-2013/css/font/fontawesome-webfont.woff?v=3.2.1
        2 hits: /presentations/logstash-puppetconf-2013/css/font/fontawesome-webfont.ttf?v=3.2.1
        2 hits: /presentations/logstash-puppetconf-2013/css/font/fontawesome-webfont.svg
        2 hits: /misc/nmh//%22file://$file/%22
        2 hits: /scripts//%22$%7BWEBLOC%7D/view.php?file=$%7Blinkto%7D%5C%22
        2 hits: /scripts//%22$%7BWEBLOC%7D/view.php/?file=$%7Blinkto%7D%5C%22
        2 hits: /scripts//%22file://$file/%22
        1 hits: /doc/index.html?org/elasticsearch/action/search/SearchResponse.html
        1 hits: /projects/xdotool%3E
        1 hits: /projects/xdotool/+++++++++++++++++++++Result:+chosen+nickname+%22awarovadoms%22;sent;
        1 hits: /apple-touch-icon-120x120-precomposed.png
        1 hits: /apple-touch-icon-120x120.png
        1 hits: /projects/securitrack/config.xsl
        1 hits: /projects/securitrack/config.xml
        1 hits: /node/add/blog
        1 hits: /geekery/find-that-lost-screen-session-2.html
        1 hits: /blog/geekery/jquery-interface-/p%20ppuffer.html
        1 hits: /doc/org/elasticsearch/action/support/master/TransportMasterNodeOperationAction.html
        1 hits: /sitemap.xml
        1 hits: /blog/geekery/httorg/style/iphone.css?p://www.semicomplete.com/about/
        1 hits: /blog/geekery/jquery-i
        1 hits: /projects/xd
        1 hits: /blog/geekery/jquery-interface-%20
        1 hits: /user/register
        1 hits: /presentations/logstash-puppetconf-2012/lib/font/league_gothic-webfont.ttf)%20format(%22truetype%22
        1 hits: /articles/dy
        1 hits: /about/wal:RecentChanges&quo
        1 hits: /about/tal:RecentChanges&quo
        1 hits: /blog/tags/+
        1 hits: /blog/geekery/2!?
        1 hits: /blog/tags/2010
        1 hits: /blog/geekery/jquery-interface-/pppuffer.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/fckeditor/editor/fckeditor.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/include/fckeditor/editor/fckeditor.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/js/fckeditor/editor/fckeditor.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/admin/FCKeditor/editor/fckeditor.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/include/fckeditor/editor/filemanager/connectors/test.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/js/fckeditor/_samples/default.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/admin/FCKeditor/_samples/default.html
        1 hits: /blog/geekery/ec2-reserved-vs-ondemand.html/fckeditor/_samples/default.html
        1 hits: /blog/geekery/jquery-i**terface-puffer.html
        1 hits: /blog/geekery/www.csh.rit.edu/~robertp
        1 hits: /presentations/vim/%094
        1 hits: /files/logstash/logstash-%25
        1 hits: /articles/ssh-???????????????????/
        1 hits: /blog/geekery/jquery-interface-
        1 hits: /blog/geekery%E2%80%A6
        1 hits: /blog/tags/g
        1 hits: /files/xdotool/xdotool-%25
    Responde code 416 "Requested Range Not Satisfiable", total: 2
        2 hits: /files/xdotool/xdotool-2.20101014.3063.tar.gz
    Responde code 500 "Internal Server Error", total: 3
        2 hits: /misc/Title.php.txt
        1 hits: /projects/xdotool/
Most visited pages Top 10
    #1: / 575 hits
    #2: /blog/tags/puppet 489 hits
    #3: /projects/xdotool/ 224 hits
    #4: /projects/xdotool/xdotool.xhtml 154 hits
    #5: /articles/dynamic-dns-with-dhcp/ 135 hits
    #6: /blog/tags/firefox 60 hits
    #7: /articles/ssh-security/ 55 hits
    #8: /blog/geekery/disabling-battery-in-ubuntu-vms.html 52 hits
    #9: /presentations/logstash-puppetconf-2012/ 51 hits
    #10: /blog/geekery/solving-good-or-bad-problems.html 49 hits
Traffic size by extension Top 10
    #1: log 1.21GiB
    #2: jar 684.38MiB
    #3: None 248.00MiB
    #4: png 135.51MiB
    #5: jpg 113.39MiB
    #6: exe 54.29MiB
    #7: gif 48.69MiB
    #8: pdf 34.48MiB
    #9: txt 22.19MiB
    #10: html 10.10MiB
Traffic size by IP Top 10
    #1: 68.180.224.225 160.34MiB
    #2: 94.23.164.135 155.40MiB
    #3: 190.153.25.242 105.03MiB
    #4: 100.2.4.116 103.64MiB
    #5: 88.198.255.242 103.60MiB
    #6: 184.154.149.126 103.58MiB
    #7: 66.249.73.135 72.00MiB
    #8: 117.28.234.67 66.00MiB
    #9: 82.200.166.110 62.24MiB
    #10: 192.95.12.193 51.86MiB
Totals
    Total log entries: 9999
    Total : 2.56GiB
    Number of different visitors : 1247
    Number of pages visited : 4070
    Average pages visited per visitor : 3.26
```

</details>

Output can be customized using the `--stat-classes` option to limit the StatProducers to use.

## Create s stats JSON file

JSON stat file is made to simplify making statistics with a 3rd party tool by pre-processing data. The process takes 2
steps:

* Creating the stat JSON file

```shell
python3 -m apache_logs_parser stats apache-log.json --no-display --output-json stats.json
```

* Exploit the file in a 3rd party software like a BI solution

### Custom stats based on JSON stats file

In the section, we will see how custom stats can be displayed and manipulated using `jq`,
(if `jq` is not installed on your machine, you can get it via `apt install jq`).

Top 10 pages hits:

```shell
jq -c 'limit(10; .hits_per_page | to_entries | sort_by(.value) | reverse | .[] )' stats.json
```

Top 10 IPs per hits:

```shell
jq -c 'limit(10; .per_ip | to_entries | sort_by(.value.hits) | reverse | .[] )' stats.json
```

Top 10 IPs per bytes sent:

```shell
jq -c 'limit(10; .per_ip | to_entries | sort_by(.value.bytes) | reverse | .[] )' stats.json
```

Display hits:

```shell
jq -c '{hits, bot_hits, mobile_hits, desktop_hits}' stats.json
```

## Issue tracker

https://github.com/martin-denizet/apache_logs_parser/issues

## Known issues

* Too big of an input file will result in an out of memory error. It's not recommended running the tool on a production
  server for input files exceeding 1GB in size.
* Parser could break in case of Apache configuration change. If IP resolution of the IPs would be enabled for example.

## Todo

* Allow displaying stats of an Apache log file in a single step
* Add start datetime and end datetime as metadata
* Get the country related to the IP address

## Development

### How to contribute

* Please make a PR for the __develop__ branch.
* Make sure tests are up-to-date and passing.

### Run tests

```shell
python3 setup.py test
```

### Code style

CI has a code quality gate using flake8

## License

GPL-3.0 License
