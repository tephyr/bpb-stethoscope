"""
A TUI for inspecting Factorio blueprints directly (no parsing into draftsman).

Inspired by Textual's ``json_tree.py`` example.
"""
from dataclasses import dataclass
import json
import zipfile

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, TreeNode
# from textual.widgets.tree import TreeNode

@dataclass
class BPUnzipper:
    path_to_blueprint:str

    def unzip(self) -> dict:
        pass

class BlueprintTUI(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Tree("Root")
