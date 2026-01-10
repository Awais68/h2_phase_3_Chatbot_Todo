"""Simple test to validate CLI components work."""
from src.cli.themes import get_current_theme, set_theme, get_theme_names
from src.cli import ui_components as ui

print("Testing themes...")
print(f"Current theme: {get_current_theme().name}")
print(f"Available themes: {get_theme_names()}")

set_theme("hacker")
print(f"Changed to: {get_current_theme().name}")

print("\nTesting UI components...")
ui.display_success("Success message works!")
ui.display_error("Error message works!")
ui.display_warning("Warning message works!")
ui.display_info("Info message works!")

print("\nAll CLI components loaded successfully! ✓")
