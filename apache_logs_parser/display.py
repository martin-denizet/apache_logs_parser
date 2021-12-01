# (c) 2021 Martin DENIZET
# GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from apache_logs_parser.colors import header, Colors


def size_format(size):
    """
    Format a Bytes value in the closest relevant unit
    :param size: A number of bytes
    :type size: int|float
    :return: A formatted string
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return f"{size:3.2f}{unit}B"
        size /= 1024.0
    return f"{size:.2f}YiB"


class Graph(object):
    """
    Static class for graphs
    """

    @classmethod
    def display(cls, data, title=None, unit='hits', show_percents=True, descending_sort=True, top=None):
        """

        :param data:
        :type data: dict
        :param title:
        :param unit:
        :param show_percents:
        :param descending_sort:
        :param top:
        """

        if title:
            header(title + (f" Top {top}" if top is not None else ""))

        data = dict(sorted(data.items(), key=lambda x: x[1], reverse=descending_sort))
        if top is not None:
            data = data[0:top]
        max_value = max(data.values())
        sum_values = sum(data.values())
        label_max_length = max([len(label) for label in data.keys()])
        for key, value in data.items():
            bar_size = value * 100 / max_value
            bars = cls.horizontal_bar(bar_size)
            percent_string = ""
            if show_percents:
                percent = value * 100 / sum_values
                percent_string = f"/ {percent:.2f}%"
            formatted_value = f"{value} {unit}"
            if unit == 'bytes':
                formatted_value = size_format(value)
            print(f"    {Colors.OKBLUE + key.ljust(label_max_length) + Colors.ENDC}|{bars} :"
                  f" {Colors.OKGREEN}{formatted_value}{Colors.ENDC}{percent_string}")

    @classmethod
    def horizontal_bar(cls, percent, scale=100):
        """
        Generate an horizontal bar
        :param percent: A number between 0 and 1
        :type percent: int|float
        :param scale: The number of characters for a full bar
        """
        value = (percent / 100) * scale
        decimal_part = value % 1
        return '█' * int(value) + cls.block(decimal_part)

    @classmethod
    def block(cls, value):
        """
        Use utf-8 characters to represent a fraction in a bar chart.
        utf-8 characters are heigths, 1/8th, 2/8th etc...
        :param value:  A number between 0 and 1
        :type value: int|float
        """
        if value < 0 or value > 1:
            raise ValueError("Value must be >=0 and <=1")
        # Get a number between 0 and 8
        heigths = round(value / (1 / 8))
        chars = ['', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
        return chars[heigths]


class TopList(object):

    @classmethod
    def display(cls, data, title=None, unit='hits', top=10):
        """

        :param data:
        :type data: dict[Any,int|float]
        :param title: Header to display
        :param unit: Unit of the values, if the unit is "bytes", it will be formatted automatically
        :type unit: str
        :param top: Reduce the number of entries to specified number
        :type top: int
        """
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)[0:top]
        if title:
            header(title + f" Top {top}" if top is not None else "")

        for index, value in enumerate(data):
            formatted_value = f"{value[1]} {unit}"
            if unit == 'bytes':
                formatted_value = size_format(value[1])
            print(f"    #{index + 1}: {value[0]} {Colors.OKGREEN}{formatted_value}{Colors.ENDC}")
