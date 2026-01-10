"""
Theme Configuration Module
Provides color themes for the Todo CLI application.
"""

from dataclasses import dataclass
from typing import Dict
from rich.style import Style


@dataclass
class Theme:
    """
    Theme configuration with color definitions.

    Attributes:
        name: Theme name
        primary: Primary accent color
        secondary: Secondary accent color
        success: Success state color
        warning: Warning state color
        error: Error state color
        info: Info state color
        text: Default text color
        muted: Muted/dimmed text color
    """
    name: str
    primary: str
    secondary: str
    success: str
    warning: str
    error: str
    info: str
    text: str
    muted: str


# Predefined themes
THEMES: Dict[str, Theme] = {
    "dark": Theme(
        name="Dark",
        primary="cyan",
        secondary="magenta",
        success="green",
        warning="yellow",
        error="red",
        info="blue",
        text="white",
        muted="#808080",
    ),
    "light": Theme(
        name="Light",
        primary="blue",
        secondary="purple",
        success="green",
        warning="orange3",
        error="red",
        info="cyan",
        text="black",
        muted="grey50",
    ),
    "hacker": Theme(
        name="Hacker",
        primary="bright_green",
        secondary="green",
        success="bright_green",
        warning="yellow",
        error="red",
        info="cyan",
        text="bright_green",
        muted="dark_green",
    ),
}


_current_theme: str = "dark"


def get_current_theme() -> Theme:
    """
    Get the currently active theme.

    Returns:
        Current Theme instance
    """
    return THEMES[_current_theme]


def set_theme(theme_name: str) -> None:
    """
    Set the active theme.

    Args:
        theme_name: Name of theme to activate (dark, light, hacker)

    Raises:
        ValueError: If theme name is invalid
    """
    global _current_theme

    if theme_name not in THEMES:
        valid_themes = ", ".join(THEMES.keys())
        raise ValueError(f"Invalid theme '{theme_name}'. Valid themes: {valid_themes}")

    _current_theme = theme_name


def get_theme_names() -> list[str]:
    """
    Get list of available theme names.

    Returns:
        List of theme names
    """
    return list(THEMES.keys())


def get_style(color_name: str) -> Style:
    """
    Get a Rich Style object for a theme color.

    Args:
        color_name: Name of color from theme (primary, success, error, etc.)

    Returns:
        Rich Style instance
    """
    theme = get_current_theme()
    color = getattr(theme, color_name, theme.text)
    return Style(color=color)
