# apache_logs_parser

__This is an example tool developed as a project during Python classes.__

This tool converts standard Apache web server logs into Python objects to produce stats and allows to save the results
in JSON files. By default, the tool will convert each Apache log line into a JSON object. The log lines are stored in
the `data` dictionary. The stats are stores in the `stats` dictionary.

## Requirements

Python > 3.4

## Install

### Install from source (git)

```shell
cd ~/
git clone https://github.com/martin-denizet/apache_logs_parser.git
pip install --user -e ~/apache_logs_parser
# Test the installation
apache_logs_parser --version
```

## Usage

```shell
apache_logs_parser -h
```

## Examples

### Convert data to JSON and produce stats

Note: Usage of `nice` is recommended for usage on production machines. Create JSON log data file from several files
using a wildcard:

```shell
nice apache_logs_parser --output-json /tmp/data.json --action convert /var/log/apache2/access_* 
```

Create JSON log data file including statistics:

```shell
nice apache_logs_parser --output-json /tmp/data_with_stats.json /var/log/apache2/access.log
```

Create JSON file containing only statistics:

```shell
nice apache_logs_parser --output-json /tmp/stats.json --action generate_stats /var/log/apache2/access.log
```

### Display stats

Stats can be displayed and manipulated using `jq`, (if `jq` is not installed on your machine, you can get it
via `apt install jq`).

Top 10 page hits:

```shell
jq -c 'limit(10; .stats.hits_per_page | to_entries | sort_by(.value) | reverse | .[] )' /tmp/stats.json
```

Top 10 IPs per hits:

```shell
jq -c 'limit(10; .stats.per_ip | to_entries | sort_by(.value.hits) | reverse | .[] )' /tmp/stats.json
```

Top 10 Ips per bytes sent:

```shell
jq -c 'limit(10; .stats.per_ip | to_entries | sort_by(.value.bytes) | reverse | .[] )' /tmp/stats.json
```

Display hits:

```shell
jq -c '.stats | {hits, bot_hits, mobile_hits, desktop_hits}' /tmp/stats.json
```

## Issue tracker

https://github.com/martin-denizet/apache_logs_parser/issues

## Known issues

* Too big of an input file will result in an out of memory error. It's not recommended running the tool on a production
  server for input files exceeding 1GB in size.
* Parser could break in case of Apache configuration change. If IP resolution of the IPs would be enabled for example.

## Todo

* Add start datetime and end datetime as metadata
* Get the country related to the IP address
* Allow specifying the stats producers to run in from the CLI

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
