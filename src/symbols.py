# Keypirinha launcher (keypirinha.com)

from enum import Enum

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

from .symbols_list import SymbolList


class SuggestionType(Enum):
    SYMBOL = 1
    EMOJI = 2

class Symbols(kp.Plugin):
    """
    One-line description of your plugin.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """

    ACTION_COPY = "copy"
    FIND_SYMBOLS_TARGET = "find_symbols"
    FIND_EMOJI_TARGET = "find_emoji"

    def __init__(self):
        super().__init__()
        self._debug = True

    def on_start(self):
        self._read_config()

    def on_catalog(self):
        catalog = [
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Symbols",
                short_desc="Find UNICODE symbol",
                target=self.FIND_SYMBOLS_TARGET,
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.KEEPALL
            ),
            # self.create_item(
            #     category=kp.ItemCategory.KEYWORD,
            #     label="Emoji",
            #     short_desc="Find emoji",
            #     target=self.FIND_EMOJI_TARGET,
            #     args_hint=kp.ItemArgsHint.REQUIRED,
            #     hit_hint=kp.ItemHitHint.KEEPALL
            # )
        ]
        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if not user_input or not items_chain:
            return

        suggestions = []

        if items_chain[-1].target() == self.FIND_SYMBOLS_TARGET:
            suggestions = self._create_suggestions(SuggestionType.SYMBOL)
        elif items_chain[-1].target() == self.FIND_EMOJI_TARGET:
            suggestions = self._create_suggestions(SuggestionType.EMOJI)

        self.set_suggestions(suggestions)
        self._create_actions()

    def on_execute(self, item, action):
        if item.category() != kp.ItemCategory.KEYWORD:
            return

        if not action or action.name() == self.ACTION_COPY:
            kpu.set_clipboard(item.short_desc())
            return

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        self._read_config()

    def _create_actions(self):
        actions = [
            self.create_action(name=self.ACTION_COPY,
                               label="Copy symbol",
                               short_desc="Copy symbol to clipboard"),
        ]
        self.set_actions(kp.ItemCategory.KEYWORD, actions)

    def _read_config(self):
        settings = self.load_settings()

    def _create_suggestions(self, suggestion_type: SuggestionType):
        suggestions = []

        source = {}
        if suggestion_type == SuggestionType.SYMBOL:
            source = SymbolList.symbols
        elif suggestion_type == SuggestionType.EMOJI:
            source = SymbolList.emoji

        for entry in source.keys():
            if len(entry) != 1:
                continue

            suggestions.append(self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label=source[entry],
                short_desc=entry,
                target=source[entry],
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE
            ))

        return suggestions
