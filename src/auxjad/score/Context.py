import copy

import abjad


class Context(abjad.Context):
    r"""Context."""

    __slots__ = (
        "_lilypond_type",
        "_consists_commands",
        "_dependent_wrappers",
        "_remove_commands",
        "_context_commands",
    )

    ### INITIALIZER ###

    # TODO: make keywords mandatory
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self._context_commands: list[str] = []
        super().__init__(*args, **kwargs)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        """
        Shallow copies context.

        Copies indicators.

        Does not copy children.

        Returns new component.
        """
        new_context = super().__copy__(*args)
        new_context._context_commands = copy.copy(self.context_commands)
        return new_context

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        indent = abjad.LilyPondFormatBundle.indent
        result = []
        if self.simultaneous:
            if self.identifier:
                open_bracket = f"<<  {self.identifier}"
            else:
                open_bracket = "<<"
        else:
            if self.identifier:
                open_bracket = f"{{   {self.identifier}"
            else:
                open_bracket = "{"
        brackets_open = [open_bracket]
        remove_commands = self._format_remove_commands()
        consists_commands = self._format_consists_commands()
        context_commands = self._context_commands
        overrides = bundle.grob_overrides
        settings = bundle.context_settings
        if remove_commands or consists_commands or context_commands or overrides or settings:
            contributions = [self._format_invocation(), r"\with", "{"]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in remove_commands]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("engraver removals", "remove_commands")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in consists_commands]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("engraver consists", "consists_commands")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in context_commands]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("engraver consists", "context_commands")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in overrides]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("overrides", "overrides")
            result.append((identifier_pair, contributions))
            contributions = [indent + _ for _ in settings]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("settings", "settings")
            result.append((identifier_pair, contributions))
            contributions = [f"}} {brackets_open[0]}"]
            contributions = ["}", open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        else:
            contribution = self._format_invocation()
            contribution += f" {brackets_open[0]}"
            contributions = [contribution]
            contributions = [self._format_invocation(), open_bracket]
            contributions = self._tag_strings(contributions)
            contributions = tuple(contributions)
            identifier_pair = ("context_brackets", "open")
            result.append((identifier_pair, contributions))
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def context_commands(self):
        r"""
        Unordered set of LilyPond settings to be included in the context.

        Usage:
            Manage with add, update, other standard set commands:

            >>> staff = abjad.Staff([])
            >>> staff.context_commands.append(r"\RemoveEmptyStaves")
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \RemoveEmptyStaves"
            }
            {
            }

            >>> voice = abjad.Voice([])
            >>> voice.context_commands.append(r"\voiceOne")
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            \with
            {
                \voiceOne
            }
            {
            }

            >>> staff_group = abjad.StaffGroup([])
            >>> staff_group.context_commands.append(r"\RemoveEmptyStaves")
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \new StaffGroup
            \with
            {
                \RemoveEmptyStaves
            }
            <<
            >>

            >>> score = abjad.Score([])
            >>> score.context_commands.append(r"\RemoveEmptyStaves")
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                \RemoveEmptyStaves
            }
            <<
            >>
        """
        return self._context_commands


class Staff(Context, abjad.Staff):  # noqa: D101
    pass


class StaffGroup(Context, abjad.StaffGroup):  # noqa: D101
    pass


class Voice(Context, abjad.Voice):  # noqa: D101
    pass


### EXTENSION METHODS ###

abjad.Context.context_commands = Context.context_commands
abjad.Staff = Staff
abjad.StaffGroup = StaffGroup
abjad.Voice = Voice
