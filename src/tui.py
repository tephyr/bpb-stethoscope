"""
A TUI for inspecting Factorio blueprints directly (no parsing into draftsman).

Inspired by Textual's ``json_tree.py`` example.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import zipfile

from rich.text import Text

from textual import log
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Tree, Button
from textual.widgets.tree import TreeNode

from bptree import BPTree

IGNORE_KEYS = ('icons', 'entities', 'version', 'active_index', 'item', 'snap-to-grid', 'tiles', 'schedules')

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
    TITLE = "Stethoscope"

    BINDINGS = [
        ("t", "toggle_all", "Toggle all"),
        ("l", "load", "Load data")
    ]

    def compose(self) -> ComposeResult:
        self._bp_tree = None # BPTree instance
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
                    new_node = node.add("")
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                node._label = Text(f"[] {name}")
                for index, value in enumerate(data):
                    new_node = node.add("")
                    add_node(str(index), new_node, value)
            else:
                node._allow_expand = False
                if name:
                    # label_parts = [
                    #     Text.from_markup(f"[b]{name}[/b]="),
                    #     *Text(data).split()
                    # ]

                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(data))
                        )
                        # Text.split(highlighter(repr(data)))
                        # *tuple(label_parts)
                    # )
                    # label = Text(f'{name}={data}')
                else:
                    label = Text(repr(data))
                node._label = label

        add_node(node.label, node, json_data)


    def on_mount(self) -> None:
        """Load the given JSON file."""
        self._bp_tree = BPTree(sys.argv[1])
        self._bp_tree.adjust_keys_to_return(keep=('index', 'active_index'), drop=IGNORE_KEYS)
        self.log(self._bp_tree.get_error_msg())
        self.action_load()

    def action_load(self) -> None:
        """Add all nodes to the tree."""
        tree = self.query_one(Tree)
        root_key = self._bp_tree.get_root_key()
        tree.reset(root_key) # This wipes the tree, including the root node.
        if self._bp_tree.get_error_msg() is None:
            self.add_json(tree.get_node_at_line(0), self._bp_tree.get_filtered_data()[root_key])
            tree.root.toggle_all()
        else:
            self.log('Parsing failed.')
            self.push_screen(AlertScreen(self._bp_tree.get_error_msg()))

    def action_toggle_all(self) -> None:
        tree = self.query_one(Tree)
        root_node = tree.get_node_at_line(0)
        if root_node is not None:
            self.log(root_node)
            root_node.toggle_all()

if __name__ == "__main__":
    app = BlueprintTUI()
    app.run()
