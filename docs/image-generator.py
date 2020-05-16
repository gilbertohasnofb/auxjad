import re
import os
import sys
import shutil


querry = input('Regenerate all images? (y/n) ')
if querry.lower() in ('y', 'yes'):

    # importing auxjad from the directory one level up
    auxjad_directory = os.path.dirname(os.getcwd())
    sys.path.insert(0, auxjad_directory)
    import auxjad

    # the pattern below looks for any line containing '>>> abjad.f', then
    # captures all the next lines until either an empty line appears (i.e. a
    # line with just  a \n on it) or until the next line contains more Python
    # documentation, which will start with a bunch of spaces followed by '>>>'.
    pattern = (r'''>>> abjad\.f.*
([\s\S]*?)
(?:\n| *>>>)''')

    # creating export directory
    if not os.path.exists('./_images'):
        os.makedirs('./_images')
    else:
        shutil.rmtree('./_images')
        os.makedirs('./_images')
    os.chdir('./_images')
    if not os.path.exists('./lilypond-files'):
        os.makedirs('./lilypond-files')

    # header for lilypond file
    ly_header = '\\include "lilypond-book-preamble.ly"\n' + \
                '\\language "english"\n\n'

    for member in dir(auxjad):
        docstring = getattr(auxjad, member).__doc__
        if docstring:
            matches = re.findall(pattern, docstring)
            if matches:
                for n, match in enumerate(matches):
                    directory = './lilypond-files/'
                    filename = 'image-' + str(member) + '-' +str(n + 1) + '.ly'
                    with open(directory + filename, 'w+') as f:
                        f.write(ly_header)
                        # removing comments from time signatures
                        match = match.replace(r'%%% ', '')
                        match = match.replace(r'%%%', '')
                        if r'\new Staff' in match:
                            f.write(match)
                        else:  # wrap in {} when not starting with \new Staff
                            f.write('{\n')
                            f.write(match)
                            f.write('\n}')
                    # compiling each newly created lilypond file
                    os.system('lilypond '
                              '-ddelete-intermediate-files '
                              '$include --png '
                              '-dbackend=eps '
                              '-dresolution=150 '
                              '-danti-alias-factor=1 '
                              + directory + filename)

    files_in_directory = os.listdir('./')
    for filename in files_in_directory:
        if any(filename.endswith(extension) for extension in ('.eps',
                                                              '.count',
                                                              '.tex',
                                                              '.texi',
                                                              )):
            os.remove(filename)
