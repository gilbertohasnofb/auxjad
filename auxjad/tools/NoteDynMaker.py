import abjad


class NoteDynMaker(abjad.NoteMaker):
    r"""An extansion of NoteMaker which also takes one dynamic per note."""

    def __call__(self, pitches, durations, dyns,
                 *, no_repeat=False) -> abjad.Selection:
        note_maker = abjad.NoteMaker()
        result = note_maker(pitches, durations)
        tied_leaves = abjad.select(result).logical_ties()
        previous_dyn = ''
        _dyns = dyns[:]
        while len(_dyns) < max(len(pitches), len(durations)):
            _dyns.append(None)
        for item, dyn in zip(tied_leaves, _dyns):
            if (not no_repeat or dyn != previous_dyn) and dyn:
                abjad.attach(abjad.Dynamic(dyn), item[0])
                previous_dyn = dyn
        return abjad.Selection(result)

