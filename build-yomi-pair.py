from html.parser import HTMLParser
import requests
import re

pattern = re.compile("javascript:playmp3.playFile")
url = 'http://dokochina.com/katakana.php'

class find_katakana(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.yomi = False
        self.hanzi = False
        self.yomi_result = ''
        self.hanzi_result = ''
        self.value = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for attr in attrs:
                if 'class' in attr and 'hanzi' in attr:
                    self.hanzi = True
        elif tag == 'a':
            for attr in attrs:
                for item in attr:
                    if type(item) == str and pattern.match(item):
                        self.yomi = True

    def handle_data(self, data):
        if self.yomi:
            self.yomi_result += data
        elif self.hanzi:
            self.hanzi_result += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.yomi:
            self.yomi = False
        elif tag == 'nobr' and self.hanzi:
            self.hanzi = False
    
    def dump_yomi(self):
        return self.yomi_result
    def dump_hanzi(self):
        return self.hanzi_result

form = {'text1': input()}
source = requests.post(url, data=form)
parser = find_katakana()
parser.feed(source.text)
print(parser.dump_hanzi())
print(parser.dump_yomi())
