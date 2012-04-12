import mimetypes
import optparse
import os
import re
import sys

from lxml import etree
from lxml.cssselect import CSSSelector
from lxml.html import document_fromstring
import markdown

mimetypes.add_type('text/markdown', '.md', True)
mimetypes.add_type('text/markdown', '.markdown', True)

RULE_RE = re.compile(r'^(?P<selector>.+?) \{(?P<rules>.*?)\}', re.M | re.S)

INVALID_PSEUDO_CLASSES = (
    ':active',
    ':disabled',
    ':enabled',
    ':focus',
    ':hover',
    ':indeterminate',
    ':link',
    ':target',
    ':visited',
)

#
# selector and rules methods
#

def valid_selector(sel):
    """ Check to see if selector can be applied and in-lined. :hover and other
        selectors do not inline properly.
    """
    for cls in INVALID_PSEUDO_CLASSES:
        if cls in sel:
            return False
    return True

def parse_rules(s):
    """ Parse a rule string into a dict.
        Duplicate properties will be overwritten.
    """
    rules = {}
    for rule in s.split(';'):
        rule = rule.strip()
        if rule:
            (prop, val) = rule.split(":", 1)
            rules[prop.strip()] = val.strip()
    return rules

def rule_str(rules):
    """ Convert a rule dict into a string.
    """
    rule_set = []
    for prop, val in rules.iteritems():
        rule_set.append("%s: %s;" % (prop, val.replace("\"", "'")))
    return " ".join(rule_set)

#
# html object
#

class Html(object):
    """ The main HTML object that allows CSS rules to modify elements.
    """

    def __init__(self, content):
        self._doc = document_fromstring(content)

    def apply(self, css, collapse=False):
        """ Apply CSS rules to elements matching the selectors.

            css: string of CSS
            collapse: recurring properties will overrite previous values
        """

        for m in RULE_RE.finditer(css):

            (selector, rules) = m.groups()

            selector = selector.strip()
            rules = parse_rules(rules)

            if valid_selector(selector):

                sel = CSSSelector(selector)
                for elem in sel(self._doc):

                    if collapse:
                        elem_rules = parse_rules(elem.attrib.get('style', ''))
                        elem_rules.update(rules)
                        elem.attrib['style'] = rule_str(elem_rules)
                    else:
                        elem_rules = elem.attrib.get('style', '')
                        elem_rules += " " + rule_str(rules)
                        elem.attrib['style'] = elem_rules.strip()

    def to_string(self):
        """ Convert document to a string.
        """
        return etree.tostring(self._doc)

class Garberizer(object):

    def __init__(self, *args, **kwargs):

        self._parser = optparse.OptionParser(usage="usage: %prog [options] inputfile")
        self._parser.add_option("-c", "--css", dest="css",
                                help="path to css file", metavar="PATH")
        self._parser.add_option("-o", "--out", dest="out",
                                help="path to output file, stdout if not specified", metavar="PATH")

        (options, args) = self._parser.parse_args()

        if not args:
            parser.error("inputfile is required")

        self.options = options
        self.input_path = args[0]

    def process(self):

        html = self.load_html(self.input_path)

        if self.options.css:
            css = self.load_css(self.options.css)
            html.apply(css)

        self.write(html)

    def load_html(self, path):

        inpath = os.path.abspath(path)

        mt = mimetypes.guess_type(inpath)[0]

        if mt not in ('text/html', 'text/markdown'):
            self._parser.error("input file must be either HTML or markdown")

        with open(inpath) as infile:
            content = infile.read()

        if mt == 'text/markdown':
            content = markdown.markdown(content)

        return Html(content)
    
    def load_css(self, path):

        csspath = os.path.abspath(self.options.css)

        mt = mimetypes.guess_type(csspath)[0]
        if mt != 'text/css':
            parser.error("css file must be of type text/css")

        with open(csspath) as infile:
            css = infile.read()

        return css

    def write(self, html):

        rendered = html.to_string() + "\n"

        if self.options.out:
            out_path = os.path.abspath(self.options.out)
            with open(out_path, 'w') as outfile:
                outfile.write(rendered)
        else:
            sys.stdout.write(rendered)

class CommandLineGarberizer(Garberizer):

    def __init__(self, *args, **kwargs):
        super(CommandLineGarberizer, self).__init__(*args, **kwargs)


if __name__ == "__main__":

    # g = CommandLineGarberizer()
    # g.process()

    CommandLineGarberizer().process()
