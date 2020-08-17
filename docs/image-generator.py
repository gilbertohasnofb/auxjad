import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.getcwd()))
import auxjad  # noqa: E402

# the pattern below looks for any line containing '>>> abjad.f', then captures
# all the next lines until either an empty line appears (i.e. a line with just
# a \n on it) or until the next line contains more Python documentation, which
# will start with a bunch of spaces followed by '>>>'.
pattern = r""">>> abjad\.f.*
([\s\S\n]+?)
 *\.\. figure:: \.\./_images/([\w-]*)\.png"""

# header for lilypond file
ly_header = r"""
\include "lilypond-book-preamble.ly"
\language "english"

\paper {
    line-width = 17\cm
}

\layout{
    indent = 0
    \numericTimeSignature
    \override Flag.stencil = #flat-flag
    \context {
        \Score
        \override SpacingSpanner.base-shortest-duration =
            #(ly:make-moment 1/12)
        \omit BarNumber
    }
}

"""

directory = './_images/lilypond-files/'

# generating lilypond files from docstrings
for namespace in (auxjad, auxjad.Mutation, auxjad.Inspection):
    for member in dir(namespace):
        docstring = getattr(namespace, member).__doc__
        if docstring is not None:
            matches = re.findall(pattern, docstring)
            if matches is not None:
                for match in matches:
                    contents = match[0]
                    filename = match[1] + '.ly'
                    with open(directory + filename, 'w+') as f:
                        f.write(ly_header)
                        if r'\new' in contents:
                            f.write(contents)
                        elif contents[0] == r'{' and contents[-1] == r'}':
                            f.write(r'\new Staff' + '\n')
                            f.write(contents)
                        else:  # wrap in {} otherwise
                            contents = textwrap.indent(contents, '    ')
                            f.write(r'\new Staff' + '\n')
                            f.write(r'{' + '\n')
                            f.write(contents)
                            f.write('\n' + r'}')

# generating lilypond files from example-n.rst files
for read_file in os.listdir('./examples'):
    if read_file.startswith('example-'):
        with open('./examples/' + read_file, 'r') as example_file:
            example_file_contentss = example_file.read()
            # finding lilypond code
            matches = re.findall(pattern, example_file_contentss)
            if matches:
                for match in matches:
                    contents = match[0]
                    filename = match[1] + '.ly'
                    with open(directory + filename, 'w+') as f:
                        f.write(ly_header)
                        if r'\new' in contents:
                            f.write(contents)
                        elif contents[0] == r'{' and contents[-1] == r'}':
                            f.write(r'\new Staff' + '\n')
                            f.write(contents)
                        else:  # wrap in {} otherwise
                            contents = textwrap.indent(contents, '    ')
                            f.write(r'\new Staff' + '\n')
                            f.write(r'{' + '\n')
                            f.write(contents)
                            f.write('\n' + r'}')
