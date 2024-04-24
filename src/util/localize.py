from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from disnake import Locale, LocalizationProtocol, LocalizationStore

LocalizedStr = t.NewType("LocalizedStr", str)


class Localization:
    """Handle the localization of various strings in command responses.

    Parameters
    ----------
    protocol: LocalizationStore | LocalizationProtocol
        The i18n connected to the bot which stores all the languages.
    """

    def __init__(self, protocol: LocalizationStore | LocalizationProtocol) -> None:
        self._i18n = protocol

    def get(
        self,
        default: str,
        locale: Locale,
        key: str,
        **placeholders: str,
    ) -> LocalizedStr:
        """
        Retrieve a localized version of a string based on the given locale and key.

        This function returns a localized string for the specified key and locale.
        If a localized version is not available, the default string is returned.

        Parameters
        ----------
        default : str
            The default string to return if a localized version is not found.
        locale : Locale
            The locale specifying the language and region for localization.
        key : str
            The key identifying the string to localize.

        Returns
        -------
        LocalizedStr
            The localized string corresponding to the key for the specified locale,
            or the default string if localization is not available.
        """
        localizations = self._i18n.get(key)
        if localizations is None:
            return LocalizedStr(default.format(**placeholders))

        localized_string = localizations.get(locale.value, default)
        return LocalizedStr(localized_string.format(**placeholders))
