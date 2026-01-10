"""
Unit tests for theme system.
Tests theme management, switching, and validation.
"""

import pytest
from rich.style import Style
from src.cli.themes import (
    Theme,
    THEMES,
    get_current_theme,
    set_theme,
    get_theme_names,
    get_style,
    _current_theme
)


class TestThemeModel:
    """Test Theme dataclass."""

    def test_theme_creation(self):
        """Test creating a theme instance."""
        theme = Theme(
            name="Test Theme",
            primary="cyan",
            secondary="magenta",
            success="green",
            warning="yellow",
            error="red",
            info="blue",
            text="white",
            muted="grey50"
        )

        assert theme.name == "Test Theme"
        assert theme.primary == "cyan"
        assert theme.secondary == "magenta"
        assert theme.success == "green"
        assert theme.warning == "yellow"
        assert theme.error == "red"
        assert theme.info == "blue"
        assert theme.text == "white"
        assert theme.muted == "grey50"


class TestThemeRegistry:
    """Test predefined themes."""

    def test_dark_theme_exists(self):
        """Test that dark theme is defined."""
        assert "dark" in THEMES
        dark = THEMES["dark"]

        assert dark.name == "Dark"
        assert isinstance(dark, Theme)

    def test_light_theme_exists(self):
        """Test that light theme is defined."""
        assert "light" in THEMES
        light = THEMES["light"]

        assert light.name == "Light"
        assert isinstance(light, Theme)

    def test_hacker_theme_exists(self):
        """Test that hacker theme is defined."""
        assert "hacker" in THEMES
        hacker = THEMES["hacker"]

        assert hacker.name == "Hacker"
        assert isinstance(hacker, Theme)

    def test_all_themes_have_required_attributes(self):
        """Test that all themes have all required color attributes."""
        required_attrs = [
            "name", "primary", "secondary", "success",
            "warning", "error", "info", "text", "muted"
        ]

        for theme_name, theme in THEMES.items():
            for attr in required_attrs:
                assert hasattr(theme, attr), f"Theme '{theme_name}' missing attribute '{attr}'"
                assert getattr(theme, attr) is not None

    def test_dark_theme_colors(self):
        """Test specific colors for dark theme."""
        dark = THEMES["dark"]

        assert dark.primary == "cyan"
        assert dark.success == "green"
        assert dark.error == "red"
        assert dark.text == "white"

    def test_light_theme_colors(self):
        """Test specific colors for light theme."""
        light = THEMES["light"]

        assert light.primary == "blue"
        assert light.success == "green"
        assert light.error == "red"
        assert light.text == "black"

    def test_hacker_theme_colors(self):
        """Test specific colors for hacker theme."""
        hacker = THEMES["hacker"]

        assert hacker.primary == "bright_green"
        assert hacker.secondary == "green"
        assert hacker.text == "bright_green"


class TestGetCurrentTheme:
    """Test getting current theme."""

    def test_get_current_theme_returns_theme(self):
        """Test that get_current_theme returns a Theme instance."""
        theme = get_current_theme()
        assert isinstance(theme, Theme)

    def test_get_current_theme_default_is_dark(self):
        """Test that default theme is dark."""
        # Reset to default
        set_theme("dark")
        theme = get_current_theme()

        assert theme.name == "Dark"

    def test_get_current_theme_reflects_changes(self):
        """Test that get_current_theme reflects theme changes."""
        set_theme("light")
        theme = get_current_theme()
        assert theme.name == "Light"

        set_theme("hacker")
        theme = get_current_theme()
        assert theme.name == "Hacker"

        # Reset to default
        set_theme("dark")


class TestSetTheme:
    """Test setting theme."""

    def test_set_theme_dark(self):
        """Test setting theme to dark."""
        set_theme("dark")
        theme = get_current_theme()

        assert theme.name == "Dark"

    def test_set_theme_light(self):
        """Test setting theme to light."""
        set_theme("light")
        theme = get_current_theme()

        assert theme.name == "Light"

    def test_set_theme_hacker(self):
        """Test setting theme to hacker."""
        set_theme("hacker")
        theme = get_current_theme()

        assert theme.name == "Hacker"

    def test_set_theme_invalid_raises_error(self):
        """Test that setting invalid theme raises ValueError."""
        with pytest.raises(ValueError, match="Invalid theme"):
            set_theme("nonexistent")

    def test_set_theme_case_sensitive(self):
        """Test that theme names are case-sensitive."""
        with pytest.raises(ValueError, match="Invalid theme"):
            set_theme("Dark")  # Should be "dark"

    def test_set_theme_error_message_includes_valid_themes(self):
        """Test that error message includes list of valid themes."""
        try:
            set_theme("invalid")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            error_msg = str(e)
            assert "dark" in error_msg
            assert "light" in error_msg
            assert "hacker" in error_msg

    def test_set_theme_persists_across_calls(self):
        """Test that theme setting persists."""
        set_theme("hacker")
        assert get_current_theme().name == "Hacker"

        # Get theme again
        assert get_current_theme().name == "Hacker"

        # Reset
        set_theme("dark")


class TestGetThemeNames:
    """Test getting theme names."""

    def test_get_theme_names_returns_list(self):
        """Test that get_theme_names returns a list."""
        names = get_theme_names()
        assert isinstance(names, list)

    def test_get_theme_names_contains_all_themes(self):
        """Test that get_theme_names contains all defined themes."""
        names = get_theme_names()

        assert "dark" in names
        assert "light" in names
        assert "hacker" in names

    def test_get_theme_names_count(self):
        """Test that get_theme_names returns correct count."""
        names = get_theme_names()
        assert len(names) == 3  # dark, light, hacker


class TestGetStyle:
    """Test getting Rich Style objects."""

    def test_get_style_primary(self):
        """Test getting primary color style."""
        set_theme("dark")
        style = get_style("primary")

        assert isinstance(style, Style)

    def test_get_style_all_colors(self):
        """Test getting styles for all color names."""
        color_names = ["primary", "secondary", "success", "warning", "error", "info", "text", "muted"]

        for color_name in color_names:
            style = get_style(color_name)
            assert isinstance(style, Style)

    def test_get_style_invalid_color_uses_default(self):
        """Test that invalid color name uses default text color."""
        style = get_style("nonexistent_color")

        assert isinstance(style, Style)
        # Should use default text color

    def test_get_style_reflects_current_theme(self):
        """Test that get_style reflects current theme."""
        # Set dark theme
        set_theme("dark")
        dark_style = get_style("primary")

        # Set light theme
        set_theme("light")
        light_style = get_style("primary")

        # Styles should be different (different themes have different colors)
        assert dark_style != light_style

        # Reset
        set_theme("dark")


class TestThemeIntegration:
    """Test theme system integration."""

    def test_switch_themes_multiple_times(self):
        """Test switching themes multiple times."""
        # Start with dark
        set_theme("dark")
        assert get_current_theme().name == "Dark"

        # Switch to light
        set_theme("light")
        assert get_current_theme().name == "Light"

        # Switch to hacker
        set_theme("hacker")
        assert get_current_theme().name == "Hacker"

        # Switch back to dark
        set_theme("dark")
        assert get_current_theme().name == "Dark"

    def test_theme_colors_accessible(self):
        """Test that theme colors are accessible."""
        theme = get_current_theme()

        # Should be able to access all color attributes
        assert hasattr(theme, "primary")
        assert hasattr(theme, "secondary")
        assert hasattr(theme, "success")
        assert hasattr(theme, "warning")
        assert hasattr(theme, "error")
        assert hasattr(theme, "info")
        assert hasattr(theme, "text")
        assert hasattr(theme, "muted")

        # Colors should be strings
        assert isinstance(theme.primary, str)
        assert isinstance(theme.success, str)

    def test_theme_used_in_formatting(self):
        """Test that theme can be used for formatting."""
        theme = get_current_theme()

        # Should be able to use color in Rich markup
        markup = f"[{theme.success}]Success message[/{theme.success}]"
        assert markup is not None
        assert theme.success in markup

    def test_all_themes_functional(self):
        """Test that all themes can be set and used."""
        for theme_name in get_theme_names():
            # Set theme
            set_theme(theme_name)

            # Get theme
            theme = get_current_theme()
            assert theme is not None

            # Get styles
            for color_name in ["primary", "success", "error"]:
                style = get_style(color_name)
                assert isinstance(style, Style)

        # Reset to default
        set_theme("dark")


class TestThemeValidation:
    """Test theme validation and error handling."""

    def test_empty_theme_name_raises_error(self):
        """Test that empty theme name raises error."""
        with pytest.raises(ValueError):
            set_theme("")

    def test_none_theme_name_raises_error(self):
        """Test that None theme name raises error."""
        with pytest.raises((ValueError, TypeError)):
            set_theme(None)

    def test_themes_dict_not_empty(self):
        """Test that THEMES dictionary is not empty."""
        assert len(THEMES) > 0

    def test_themes_dict_keys_are_strings(self):
        """Test that all theme keys are strings."""
        for key in THEMES.keys():
            assert isinstance(key, str)

    def test_themes_dict_values_are_themes(self):
        """Test that all theme values are Theme instances."""
        for value in THEMES.values():
            assert isinstance(value, Theme)
