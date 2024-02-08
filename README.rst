blueprintbook-stethoscope
=========================

TUI development
+++++++++++++++
Two emulators::

    textual console
    # In other, from project root:
    textual run --dev src/tui.py

Test/debug notes
++++++++++++++++

Print a trace of the variables changed in a function::
    @snoop(depth=1) # depth is optional
    def filter(self)->dict:

Print a trace, focusing on the ``result`` variable::
    @snoop(depth=1, watch=('result'))
    def _filter_bp(self, bp:dict)->dict:


Skip a test::

    @pytest.mark.skip
    def test_single_blueprintbook_custom_value_keys(self, original_data, get_data):
