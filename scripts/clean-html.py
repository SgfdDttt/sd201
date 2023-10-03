import sys
from html.parser import HTMLParser
import re
import codecs

input_file = sys.argv[1]
output_file = sys.argv[2]

html_content = ''.join(open(input_file,'r', encoding='utf-8'))

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.record = False
        self.in_style = False
        self.content = []

    def handle_starttag(self, tag, attrs):
        """print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)"""
        if tag == 'p':
            assert not self.record
            self.record = True
        if tag == 'style':
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == 'p':
            assert self.record
            self.record = False
            self.content.append('\n')
        if tag == 'style':
            self.in_style = False
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if not self.record:
            return
        if self.in_style:
            return
        output = data.strip()
        if len(output):
            self.content.append(output)

# keep only relevant HTML
parser = MyHTMLParser()
parser.feed(html_content)
text = ' '.join(parser.content)

# remove things in brackets: generally they are links
bracket_regexp = re.compile(r"\[.*?\]")
text = bracket_regexp.sub('', text)

# fix punctuation
punctuation = ['.', ',', '?', ';', '.', ':', '/', '!', ')']
for p in punctuation:
    issue = ' ' + p
    while issue in text:
        text = text.replace(issue, p)
p='('
issue = p + ' '
while issue in text:
    text = text.replace(issue, p)

# fix double spaces
double_space = '  '
while double_space in text:
    text = text.replace(double_space, ' ')

# remove empty lines
def empty_line(line):
    test = len(line.strip()) == 0
    return test

def fix_line(line):
    return line.strip()

text = text.split('\n')
text = map(fix_line, text)
text = filter(lambda x: not empty_line(x), text)
text = '\n\n'.join(text)

# write to file
with open(output_file, 'w') as f:
    f.write(text.strip() + '\n')
