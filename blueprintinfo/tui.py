"""
A TUI for inspecting Factorio blueprints directly (no parsing into draftsman).

Inspired by Textual's ``json_tree.py`` example.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import zipfile

from draftsman import utils

from rich.text import Text

from textual import log
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Tree, Button
from textual.widgets.tree import TreeNode

@dataclass
class BPUnzipper:
    path_to_blueprint:str
    _blueprint_text:str = None
    _error_msg:str = None

    def unzip(self) -> dict:
        self._error_msg = None
        p = Path(self.path_to_blueprint).expanduser()
        if p.exists():
            self._blueprint_text = p.read_text()
            # Convert from ??? to ???.
            return utils.string_to_JSON(self._blueprint_text)
        else:
            self._error_msg = f'Failed to find this file: {self.path_to_blueprint}.'

    def get_error_msg(self):
        return self._error_msg

class AlertScreen(Screen):
    def compose(self, msg_text) -> ComposeResult:
        yield Grid(
            Static(msg_text, id="msg"),
            Button("OK", variant="error", id="ok"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class BlueprintTUI(App):

    _bpunzipper:BPUnzipper = None
    _bp_data:dict = None

    BINDINGS = [
        ("t", "toggle_all", "Toggle all"),
        ("l", "load", "Load data")
    ]

    def compose(self) -> ComposeResult:
        # path = "./" if len(sys.argv) < 2 else sys.argv[1]
        self._bpunzipper = BPUnzipper(sys.argv[1]) # TODO: Make explicit.
        yield Header()
        yield Footer()
        yield Tree("Root", id="root_node")

    @classmethod
    def add_json(cls, node: TreeNode, json_data: object) -> None:
        """Adds JSON data to a node.

        Args:
            node (TreeNode): A Tree node.
            json_data (object): An object decoded from JSON.
        """

        from rich.highlighter import ReprHighlighter

        highlighter = ReprHighlighter()

        def use_node(name: str, data: object=None) -> bool:
            if name in ('icons', 'entities', 'version', 'index', 'active_index', 'item', 'snap-to-grid', 'tiles'):
                return False

            return True

        def add_node(name: str, node: TreeNode, data: object) -> None:
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
            if isinstance(data, dict):
                node._label = Text(f"{{}} {name}")
                for key, value in data.items():
                    if use_node(key, value):
                        new_node = node.add("")
                        add_node(key, new_node, value)
            elif isinstance(data, list):
                node._label = Text(f"[] {name}")
                for index, value in enumerate(data):
                    if use_node(name, data):
                        new_node = node.add("")
                        add_node(str(index), new_node, value)
            else:
                node._allow_expand = False
                if name:
                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(data))
                    )
                else:
                    label = Text(repr(data))
                node._label = label

        add_node("JSON", node, json_data)


    def on_mount(self) -> None:
        """Load the given JSON file."""
        self.log(self._bpunzipper)

    def action_load(self) -> None:
        """Add a node to the tree."""
        tree = self.query_one(Tree)
        json_node = tree.root.add("JSON")
        self._bp_data = self._bpunzipper.unzip()
        if self._bp_data is not None:
            log(self._bp_data.keys())
            self.add_json(json_node, self._bp_data)
            tree.root.expand()
        else:
            self.log('Parsing failed.')
            self.push_screen(AlertScreen(self._bpunzipper.get_error_msg()))

    def action_toggle_all(self) -> None:
        tree = self.query_one(Tree)
        root_node = tree.get_node_at_line(0)
        if root_node is not None:
            self.log(root_node)
            self.log(dir(root_node))
            # The docs say these are available, but the code fails out.
            # Because I'm on 0.10.1, and the docs reference **unreleased** 0.11.0.
            root_node.toggle_all()

if __name__ == "__main__":
    app = BlueprintTUI()
    app.run()
