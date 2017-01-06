from itertools import izip
from collections import OrderedDict
from summarizr import summarize
import wikipedia
import json
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_search_data(query):
    search_data = wikipedia.search(query, results=10)
    if search_data:
        json_data = json.dumps(search_data)
        return json_data
    else:
        return None

def print_content(query):
    arr = query.content_dict
    for a in arr:
        print a
        print '\n'
    return arr


class WikiPage:
    def __init__(self, search_string):
        self.page = wikipedia.page(search_string)
        self.url = self.page.url
        self.images = self.page.images
        self.content = self.page.content.decode('unicode_escape').encode('ascii', 'ignore')
        self.content_dict = self._get_content_dict(self.content)
        self.content_summary = self._summarize_content(self.content_dict)

    def _remove_newlines(self, content):
        replacements = {'\n': '', '\r': ''}
        substrs = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))

        return regexp.sub(lambda match: replacements[match.group(0)], content)

    def _get_content_dict(self, content):
        content = self._remove_newlines(content)
        # Remove See Also links and other page metadata
        content = re.split('== See also ==', content)[0]
        arr = re.split('(=+ [a-zA-Z0-9 .()]+ =+)', content)
        # Insert title into content summary list
        arr.insert(0, self.page.title)
        for idx, a in enumerate(arr):
            if "==" in a:
                arr[idx] = re.findall('[a-zA-Z0-9 .()]+', a)[0]
        i = iter(arr)
        content_dict = OrderedDict(izip(i, i))
        return content_dict

    def _summarize_content(self, content_dict):
        for (key, value) in content_dict.iteritems():
            content_dict[key] = summarize(value)
        return content_dict
