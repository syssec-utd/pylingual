"""
Module implementing an exporter for TeX.
"""
import os
from PyQt6.Qsci import QsciScintilla
from eric7 import Preferences
from eric7.EricGui.EricOverrideCursor import EricOverrideCursor
from eric7.EricWidgets import EricMessageBox
from .ExporterBase import ExporterBase

class ExporterTEX(ExporterBase):
    """
    Class implementing an exporter for TeX.
    """
    CHARZ = 26

    def __init__(self, editor, parent=None):
        """
        Constructor

        @param editor reference to the editor object (QScintilla.Editor.Editor)
        @param parent parent object of the exporter (QObject)
        """
        ExporterBase.__init__(self, editor, parent)

    def __getTexRGB(self, color):
        """
        Private method to convert a color object to a TeX color string.

        @param color color object to convert (QColor)
        @return TeX color string (string)
        """
        rf = color.red() / 256.0
        gf = color.green() / 256.0
        bf = color.blue() / 256.0
        r = int(rf * 10 + 0.5)
        g = int(gf * 10 + 0.5)
        b = int(bf * 10 + 0.5)
        return '{0:d}.{1:d}, {2:d}.{3:d}, {4:d}.{5:d}'.format(r // 10, r % 10, g // 10, g % 10, b // 10, b % 10)

    def __texStyle(self, style):
        """
        Private method to calculate a style name string for a given style
        number.

        @param style style number (integer)
        @return style name string (string)
        """
        buf = ''
        if style >= 0:
            start = ord('a')
        else:
            start = ord('A')
            style = abs(style)
        if style == 0:
            buf = 'a'
        else:
            while style > 0:
                buf += chr(start + style % self.CHARZ)
                style //= self.CHARZ
        return buf

    def __defineTexStyle(self, font, color, paper, file, istyle):
        """
        Private method to define a new TeX style.

        @param font the font to be used (QFont)
        @param color the foreground color to be used (QColor)
        @param paper the background color to be used (QColor)
        @param file reference to the open file to write to (file object)
        @param istyle style number (integer)
        """
        closing_brackets = 3
        file.write('\\newcommand{{\\eric{0}}}[1]{{\\noindent{{\\ttfamily{{'.format(self.__texStyle(istyle)))
        if font.italic():
            file.write('\\textit{')
            closing_brackets += 1
        if font.bold():
            file.write('\\textbf{')
            closing_brackets += 1
        if color != self.defaultColor:
            file.write('\\textcolor[rgb]{{{0}}}{{'.format(self.__getTexRGB(color)))
            closing_brackets += 1
        if paper != self.defaultPaper:
            file.write('\\colorbox[rgb]{{{0}}}{{'.format(self.__getTexRGB(paper)))
            closing_brackets += 1
        file.write('#1{0}\n'.format('}' * closing_brackets))

    def exportSource(self):
        """
        Public method performing the export.
        """
        filename = self._getFileName(self.tr('TeX Files (*.tex)'))
        if not filename:
            return
        self.editor.recolor(0, -1)
        tabSize = self.editor.getEditorConfig('TabWidth')
        if tabSize == 0:
            tabSize = 4
        onlyStylesUsed = Preferences.getEditorExporter('TeX/OnlyStylesUsed')
        titleFullPath = Preferences.getEditorExporter('TeX/FullPathAsTitle')
        lex = self.editor.getLexer()
        self.defaultPaper = lex and lex.paper(QsciScintilla.STYLE_DEFAULT) or self.editor.paper().name()
        self.defaultColor = lex and lex.color(QsciScintilla.STYLE_DEFAULT) or self.editor.color().name()
        self.defaultFont = lex and lex.color(QsciScintilla.STYLE_DEFAULT) or Preferences.getEditorOtherFonts('DefaultFont')
        lengthDoc = self.editor.length()
        styleIsUsed = {}
        if onlyStylesUsed:
            for index in range(QsciScintilla.STYLE_MAX + 1):
                styleIsUsed[index] = False
            pos = 0
            while pos < lengthDoc:
                styleIsUsed[self.editor.styleAt(pos) & 127] = True
                pos += 1
        else:
            for index in range(QsciScintilla.STYLE_MAX + 1):
                styleIsUsed[index] = True
        styleIsUsed[QsciScintilla.STYLE_DEFAULT] = True
        with EricOverrideCursor(), open(filename, 'w', encoding='utf-8') as f:
            try:
                f.write('\\documentclass[a4paper]{article}\n')
                f.write('\\usepackage[a4paper,margin=1.5cm]{geometry}\n')
                f.write('\\usepackage[T1]{fontenc}\n')
                f.write('\\usepackage{color}\n')
                f.write('\\usepackage{alltt}\n')
                f.write('\\usepackage{times}\n')
                if self.editor.isUtf8():
                    f.write('\\usepackage[utf8]{inputenc}\n')
                else:
                    f.write('\\usepackage[latin1]{inputenc}\n')
                if lex:
                    istyle = 0
                    while istyle <= QsciScintilla.STYLE_MAX:
                        if (istyle <= QsciScintilla.STYLE_DEFAULT or istyle > QsciScintilla.STYLE_LASTPREDEFINED) and styleIsUsed[istyle] and (lex.description(istyle) or istyle == QsciScintilla.STYLE_DEFAULT):
                            font = lex.font(istyle)
                            colour = lex.color(istyle)
                            paper = lex.paper(istyle)
                            self.__defineTexStyle(font, colour, paper, f, istyle)
                            (subs_start, subs_count) = self.editor.getSubStyleRange(istyle)
                            for subs_idx in range(subs_count):
                                font = lex.font(subs_start + subs_idx)
                                colour = lex.color(subs_start + subs_idx)
                                paper = lex.paper(subs_start + subs_idx)
                                self.__defineTexStyle(font, colour, paper, f, subs_idx - subs_start)
                        istyle += 1
                else:
                    colour = self.editor.color()
                    paper = self.editor.paper()
                    font = Preferences.getEditorOtherFonts('DefaultFont')
                    self.__defineTexStyle(font, colour, paper, f, 0)
                    self.__defineTexStyle(font, colour, paper, f, QsciScintilla.STYLE_DEFAULT)
                f.write('\\begin{document}\n\n')
                title = self.editor.getFileName() if titleFullPath else os.path.basename(self.editor.getFileName())
                f.write('Source File: {0}\n\n\\noindent\n\\tiny{{\n'.format(title.replace('_', '\\_')))
                styleCurrent = self.editor.styleAt(0)
                f.write('\\eric{0}{{'.format(self.__texStyle(styleCurrent)))
                lineIdx = 0
                pos = 0
                utf8 = self.editor.isUtf8()
                utf8Ch = b''
                utf8Len = 0
                while pos < lengthDoc:
                    ch = self.editor.byteAt(pos)
                    style = self.editor.styleAt(pos)
                    if style != styleCurrent:
                        f.write('}}\n\\eric{0}{{'.format(self.__texStyle(style)))
                        styleCurrent = style
                    if ch == b'\t':
                        ts = tabSize - lineIdx % tabSize
                        lineIdx += ts - 1
                        f.write('\\hspace*{{{0:d}em}}'.format(ts))
                    elif ch == b'\\':
                        f.write('{\\textbackslash}')
                    elif ch in [b'>', b'<', b'@']:
                        f.write('${0}$'.format(ch.decode()))
                    elif ch in [b'{', b'}', b'^', b'_', b'&', b'$', b'#', b'%', b'~']:
                        f.write('\\{0}'.format(ch.decode()))
                    elif ch in [b'\r', b'\n']:
                        lineIdx = -1
                        if ch == b'\r' and self.editor.byteAt(pos + 1) == b'\n':
                            pos += 1
                        styleCurrent = self.editor.styleAt(pos + 1)
                        f.write('}} \\\\\n\\eric{0}{{'.format(self.__texStyle(styleCurrent)))
                    elif ch == b' ':
                        if self.editor.byteAt(pos + 1) == b' ':
                            f.write('{\\hspace*{1em}}')
                        else:
                            f.write(' ')
                    elif ord(ch) > 127 and utf8:
                        utf8Ch += ch
                        if utf8Len == 0:
                            if utf8Ch[0] & 240 == 240:
                                utf8Len = 4
                            elif utf8Ch[0] & 224 == 224:
                                utf8Len = 3
                            elif utf8Ch[0] & 192 == 192:
                                utf8Len = 2
                        elif len(utf8Ch) == utf8Len:
                            ch = utf8Ch.decode('utf8')
                            f.write(ch)
                            utf8Ch = b''
                            utf8Len = 0
                    else:
                        f.write(ch.decode())
                    lineIdx += 1
                    pos += 1
                f.write('}\n} %end tiny\n\n\\end{document}\n')
            except OSError as err:
                EricMessageBox.critical(self.editor, self.tr('Export source'), self.tr('<p>The source could not be exported to <b>{0}</b>.</p><p>Reason: {1}</p>').format(filename, str(err)))

def createExporter(editor, parent=None):
    """
    Function to instantiate an exporter object.

    @param editor reference to the editor object
    @type QScintilla.Editor.Editor
    @param parent parent object of the exporter (defaults to None)
    @type QObject (optional)
    @return exporter object
    @rtype ExporterTEX
    """
    return ExporterTEX(editor, parent=parent)