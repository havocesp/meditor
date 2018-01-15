import re
import os.path
import logging

from PyQt5 import Qsci, QtGui, QtCore
from PyQt5.Qsci import QsciScintilla

from .. import __home_data_path__, __data_path__, globalvars

logger = logging.getLogger(__name__)


class QsciLexerRest(Qsci.QsciLexerCustom):
    keyword_list = [
        'attention',
        'caution',
        'danger',
        'error',
        'hint',
        'important',
        'note',
        'tip',
        'warning',
        'admonition',
        'image', 'figure',
        'topic',
        'sidebar',
        'code',
        'math',
        'rubric',
        'epigraph',
        'highlights',
        'compound',
        'container',
        'table',
        'csv-table',
        'list-table',
        'contents',
        'sectnum', 'section-autonumbering',
        'section-numbering',
        'header', 'footer',
        'target-notes',
        'meta',
        'include',
        'raw',
        'class',
        'role',
        'default-role',
    ]
    styles = {
        'string': 0,
        'colon': 0,
        'newline': 31,
        'comment': 1,
        'title': 2,
        'section': 2,
        'transition': 3,
        'bullet': 4,
        'enumerated': 4,
        'definition': 5,
        'field': 0,
        'option': 7,
        'literal': 8,
        'literal2': 8,
        'literal3': 8,
        'line': 9,
        'line2': 9,
        'quote': 10,
        'doctest': 11,
        'table': 12,
        'table1': 12,
        'table2': 12,
        'footnote': 13,
        'target': 14,
        'target1': 14,
        'target2': 14,
        'directive': 0,
    }
    inline_styles = {
        'in_field': 6,
        'in_directive': 15,
        'in_emphasis': 16,
        'in_strong': 17,
        'in_literal': 18,
        'in_url': 19,
        'in_url1': 19,
        'in_url2': 19,
        'in_url3': 19,
        'in_link': 20,
        'in_link1': 20,
        'in_link2': 20,
        'in_footnote': 21,
        'in_substitution': 22,
        'in_target': 23,
        'in_reference': 24,
        'in_unusedspace': 25,
    }
    properties = {
        0:  'fore:#000000',
        1:  'fore:#4e9a06',
        2:  'fore:#204a87,bold',
        3:  'fore:#888a85',
        4:  'fore:#5c3566',
        5:  'fore:#845902',
        6:  'fore:#a40000',
        7:  'fore:#3465a4,back:#eeeeec',
        8:  'fore:#3465a4,back:#eeeeec,$(font.Monospace)',
        9:  'fore:#8f5902',
        10: 'fore:#8f5902',
        11: 'fore:#3465a4,back:#eeeeec',
        12: 'fore:#ce5c00',
        13: 'fore:#555753',
        14: 'fore:#4e9a06',
        15: 'fore:#a40000',
        16: 'italic',
        17: 'bold',
        18: 'fore:#3465a4,back:#eeeeec,$(font.Monospace)',
        19: 'fore:#4e9a06,underline',
        20: 'fore:#4e9a06,underline',
        21: 'fore:#555753',
        22: 'fore:#4e9a06',
        23: 'fore:#4e9a06',
        24: 'fore:#4e9a06',
        25: 'back:#ef2929',
        31: 'fore:#000000',
    }
    token_regex = [
        ('title',       r'''^([=`'"~^_*+#-]+)(\r\n?|\n).+\2\1\2'''),
        ('section',     r'''^\w.*(\r\n?|\n)[=`'"~^_*+#-]+\1'''),
        ('transition',  r'''^(\r\n?|\n)[=`'"~^_*+#-]{4,}\1\1'''),
        ('bullet',      r'''^[\-+*] +.+([\r\n]+ {2,}.+)*(\r\n?|\n)'''),
        ('enumerated',  r'''^(\(?(#|\w+)[.)] +)\S.*([\r\n]+ {2,}.+)*(\r\n?|\n)'''),
        ('field',       r'''^:[ \w\-]+:.*([\r\n]+ +.*)*(\r\n?|\n)'''),
        ('option',      r'''^[\-/]+\w[^\r\n]+([\r\n]+ +.*)*(\r\n?|\n)'''),
        ('line',        r'''^\| .*((\r\n?|\n) .*)*(\r\n?|\n)'''),
        ('line2',       r'''^( +\|) .*(\r\n?|\n)'''),
        ('quote',       r'''^( {2,})\w.+([\r\n]+\1.+)*(\r\n?|\n)'''),
        ('definition',  r'''^\w.*(\r\n?|\n) +.*([\r\n]+ +.*)*\1'''),
        ('doctest',     r'''^>>> .+(\r\n?|\n)'''),
        ('table1',      r'''^( *)[\-=+]{2,}((\r\n?|\n)\1[\|+].+)+(\r\n?|\n)'''),
        ('table2',      r'''^( *)[\-=]{2,} [\-= ]+((\r\n?|\n)\1.+)+(\r\n?|\n)'''),

        ('literal3',    r'''^\.\. +code::.*(\r\n?|\n)([\r\n]+ {2,}.+)*\1'''),
        ('directive',   r'''^\.\. +[\-\w]+::.*([\r\n]+ {2,}.+)*(\r\n?|\n)'''),
        ('footnote',    r'''^\.\. \[[^\]]+\] .+([\r\n]+ {3,}.+)*(\r\n?|\n)'''),
        ('target1',     r'''^\.\. _[^:]+: .*(\r\n?|\n)'''),
        ('comment',     r'''^\.\. +[\-\w].*([\r\n]+ {2,}.+)*(\r\n?|\n)'''),
        ('target2',     r'''^__ .+(\r\n?|\n)'''),
        # ^ only match from line beginning
        ('literal',     r'''::(\r\n?|\n)([\r\n]+ +.*)+\1'''),
        ('literal2',    r'''::(\r\n?|\n)([\r\n]+>+.*)+\1'''),
        ('newline',     r'''[\r\n]+'''),
        ('colon',       r''':+'''),
        ('string',      r'''[^:\r\n]+'''),

        # inline markup
        ('in_emphasis', r'''(\*\w[^*\r\n]*\*)'''),
        ('in_strong',   r'''(\*{2}\w[^*\r\n]*\*{2})'''),
        ('in_literal',  r'''(`{2}\w[^`\r\n]*`{2})'''),
        ('in_url1',     r'''\W(\w+://[\w\-\.:/]+)\W'''),
        ('in_url2',     r'''(`[^<\r\n]+<[^>\r\n]+>`_)'''),
        ('in_url3',     r'''^(\w+://[\w\-\.:/]+)\W'''),
        ('in_link1',    r'''\W(\w+_)\W'''),
        ('in_link2',    r'''(`\w[^`\r\n]*`_)'''),
        ('in_footnote', r'''(\[[\w*#]+\]_)'''),
        ('in_substitution', r'''(\|\w[^\|]*\|)'''),
        ('in_target',    r'''(_`\w[^`\r\n]*`)'''),
        ('in_reference', r'''(:\w+:`\w+`)'''),
        ('in_directive', r'''^\.{2} +(%s):{2}''' % '|'.join(keyword_list)),
        ('in_field',     r'''^:([^:]+):[ \r\n]'''),
        ('in_unusedspace', r'''( +)(\r\n?|\n)'''),
    ]
    block_tokens = None
    inline_tokens = None

    def __init__(self, parent=None):
        super(QsciLexerRest, self).__init__(parent)
        self.rstyles = dict(zip(*(self.styles.values(), self.styles.keys())))
        self.inline_rstyles = dict(zip(*(self.inline_styles.values(), self.inline_styles.keys())))

        self.setDefaultColor(QtGui.QColor('#000000'))
        self.setDefaultPaper(QtGui.QColor('#ffffff'))

        self.block_tokens = []
        self.inline_tokens = []
        for key, regex in self.token_regex:
            if key.startswith('in_'):
                self.inline_tokens.append((key, re.compile(
                    regex,
                    re.UNICODE | re.IGNORECASE,
                )))
            else:
                self.block_tokens.append((key, re.compile(
                    regex,
                    re.UNICODE | re.MULTILINE | re.IGNORECASE,
                )))

        self.setDebugLevel(globalvars.logging_level)

        logger.debug('Loading properties')
        self.readProperties()

        rst_prop_files = [
            os.path.join(__home_data_path__, 'rst.properties'),
            os.path.join(__data_path__, 'rst.properties'),
        ]
        for rst_prop_file in rst_prop_files:
            if os.path.exists(rst_prop_file):
                break
        if os.path.exists(rst_prop_file):
            logger.debug('Loading %s', rst_prop_file)
            self.readConfig(rst_prop_file)

    def language(self):
        return 'reStructuredText'

    def description(self, style):
        return self.rstyles.get(style) or self.inline_rstyles.get(style)

    def do_StylingText(self, start, end):
        text = self.parent().text(start, end)
        self.startStyling(start)
        offset = 0
        while offset < len(text):
            # logger.debug('try match: %s %s' % (offset, repr(text[offset:])))
            mo = None
            for key, tok in self.block_tokens:
                mo = tok.match(text, offset)
                if mo:
                    break
            assert mo, text[offset:]
            # !! must match a style
            m_string = mo.group(0)
            length = len(m_string.encode('utf8'))
            logger.debug('match: %s, %s, %s' % (key, length, m_string))
            self.setStyling(length, self.styles[key])
            offset = mo.end()
        self.do_InlineStylingText(start, end)

    def do_InlineStylingText(self, start, end):
        start_line, _ = self.editor().lineIndexFromPosition(start)
        end_line, _ = self.editor().lineIndexFromPosition(end)
        for x in range(start_line, end_line + 1):
            pos = self.editor().positionFromLineIndex(x, 0)
            if self.parent().getStyleAt(pos) == self.styles['literal']:
                continue
            text = self.editor().text(x)
            for key, tok in self.inline_tokens:
                mo_list = tok.finditer(text)
                for mo in mo_list:
                    m_string = mo.group(1)
                    length = len(m_string.encode('utf8'))
                    m_start = self.editor().positionFromLineIndex(x, mo.start(1))
                    logger.debug('inline match: %s, %s, %s' % (key, length, repr(m_string)))
                    self.startStyling(m_start)
                    self.setStyling(length, self.inline_styles[key])

    def styleText(self, start, end):
        """start and end is based bytes """
        if not self.editor():
            return
        if self.editor()._pauseLexer:
            return
        logger.debug('styling'.center(70, '-'))
        eol_mode = self.parent().eolMode()
        if eol_mode == QsciScintilla.EolWindows:
            eol = '\r\n'
        if eol_mode == QsciScintilla.EolUnix:
            eol = '\n'
        if eol_mode == QsciScintilla.EolMac:
            eol = '\r'
        pos = max(start - len(eol), 0)
        pre_style = self.parent().getStyleAt(pos)
        logger.debug('prev style: %s' % self.rstyles.get(pre_style) or self.inline_rstyles.get(pre_style))
        while pos > 0:
            style = self.parent().getStyleAt(pos)
            newline = self.parent().text(pos, min(pos + len(eol), self.parent().length()))
            next_pos = max(pos - len(eol), 0)
            if newline == eol \
                    and newline == self.parent().text(
                        next_pos, min(next_pos + len(eol), self.parent().length())) \
                    and style != pre_style:
                break
            pos = next_pos
        fix_start = pos
        pos = min(end + len(eol), self.parent().length())
        suf_style = self.parent().getStyleAt(pos)
        logger.debug('next style: %s' % self.rstyles.get(suf_style) or self.inline_rstyles.get(suf_style))
        while pos < self.parent().length():
            style = self.parent().getStyleAt(pos)
            next_pos = min(pos + len(eol), self.parent().length())
            newline = self.parent().text(pos, next_pos)
            if newline == eol \
                    and newline == self.parent().text(
                        next_pos, min(next_pos + len(eol), self.parent().length())) \
                    and style != suf_style:
                break
            pos = next_pos
        fix_end = pos
        text = self.parent().text(start, end)
        fix_text = self.parent().text(fix_start, fix_end)
        logger.debug('text: %s %s %s' % (start, end, text))
        logger.debug('fix range text: %s %s %s' % (fix_start, fix_end, fix_text))
        self.do_StylingText(fix_start, fix_end)

    def defaultStyle(self):
        return self.styles['string']

    def setDebugLevel(self, logging_level):
        pass

    def do_read_style(self, prop_list, style):
        font = self.font(style)
        for prop in prop_list:
            if prop.startswith('face:'):
                fgcolor = QtGui.QColor(prop.split(':')[1])
                self.setColor(fgcolor, style)
            elif prop.startswith('back:'):
                bgcolor = QtGui.QColor(prop.split(':')[1])
                self.setPaper(bgcolor, style)
            else:
                if ':' in prop:
                    continue
                if prop.startswith('$(font.'):
                    mo = re.match(r'^\$\(font\.(.+)\)', prop)
                    font = QtGui.QFont(mo.group(1))
                elif prop == 'bold':
                    font.setBold(True)
                elif prop == 'italic':
                    font.setItalic(True)
                elif prop == 'underline':
                    font.setUnderline(True)
                self.setFont(font, style)

    def readProperties(self):
        for style, value in self.properties.items():
            self.do_read_style(value.split(','), style)

    def readConfig(self, rst_prop_file):
        prop_settings = QtCore.QSettings(rst_prop_file, QtCore.QSettings.IniFormat)
        for style in self.properties.keys():
            value = prop_settings.value('style.rst.%s' % style, type=str)
            if not value:
                continue
            if isinstance(value, str):
                v = value.split(',')
            else:
                v = value
            self.do_read_style(v, style)
