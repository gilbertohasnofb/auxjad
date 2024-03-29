import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.getcwd()))
import auxjad  # noqa: E402

# the pattern below looks for any line containing '..  docs::', then captures
# all the next lines until a '..  figure:: ../_images/xxx.png' shows up
pattern = r"""\.\. {1,2}docs::\s+
([\s\S\n]+?)
\s*\.\. {1,2}figure:: \.\./_images/([\w-]*)\.png"""

# header for lilypond file
ly_header = r"""
\version "2.24"

\include "lilypond-book-preamble.ly"
\language "english"

#(ly:set-option 'tall-page-formats 'eps,png,pdf)
#(ly:set-option 'separate-page-formats 'eps,png,pdf)

\paper {
    line-width = 17\cm
}

\layout{
    indent = 0
    \numericTimeSignature
    tupletFullLength = ##t
    \override Flag.stencil = #flat-flag
    \override Tie.layer = #-2
    \override Staff.TimeSignature.layer = #-1
    \override Staff.TimeSignature.whiteout = ##t
    \context {
        \Score
        \override SpacingSpanner.base-shortest-duration =
            #(ly:make-moment 1/12)
        \omit BarNumber
    }
}

"""

output_directory = './_images/lilypond-files/'

namespaces = [auxjad,
              auxjad.CartographySelector,
              auxjad.CrossFader,
              auxjad.Fader,
              auxjad.GeneticAlgorithm,
              auxjad.Hocketer,
              auxjad.LeafLooper,
              auxjad.ListLooper,
              auxjad.Phaser,
              auxjad.PitchRandomiser,
              auxjad.Repeater,
              auxjad.Shuffler,
              auxjad.TenneySelector,
              auxjad.WindowLooper,
              auxjad.TimeSignature,
              auxjad.ArtificialHarmonic,
              auxjad.HarmonicNote,
              auxjad.GeneticAlgorithmMusicMaker,
              auxjad.LeafDynMaker,
              auxjad.Score,
              auxjad.piano_pedal,
              auxjad.get,
              auxjad.mutate,
              ]

# generating lilypond files from docstrings
for namespace in namespaces:
    for member in dir(namespace):
        docstring = getattr(namespace, member).__doc__
        if docstring is not None:
            matches = re.findall(pattern, docstring)
            if matches is not None:
                for match in matches:
                    contents = match[0]
                    filename = match[1] + '.ly'
                    with open(output_directory + filename, 'x') as f:
                        f.write(ly_header)
                        contents = textwrap.dedent(contents)
                        if r'\new' in contents:
                            f.write(contents)
                        elif contents[0] == '{' and contents[-1] == '}':
                            f.write(r'\new Staff' + '\n')
                            f.write(contents)
                        else:  # wrap in {} otherwise
                            contents = textwrap.indent(contents, '    ')
                            f.write(r'\new Staff' + '\n')
                            f.write('{\n')
                            f.write(contents)
                            f.write('\n}')

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
                    with open(output_directory + filename, 'w+') as f:
                        f.write(ly_header)
                        contents = textwrap.dedent(contents)
                        if r'\new' in contents:
                            f.write(contents)
                        elif contents[0] == '{' and contents[-1] == '}':
                            f.write(r'\new Staff' + '\n')
                            f.write(contents)
                        else:  # wrap in {} otherwise
                            contents = textwrap.indent(contents, '    ')
                            f.write(r'\new Staff' + '\n')
                            f.write('{\n')
                            f.write(contents)
                            f.write('\n}')
