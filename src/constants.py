"""
Constants for interacting with Factorio's blueprint data.

Basics:

A blueprint book's ``item`` is ``blueprint-book``.  A blueprint's ``item`` is ``blueprint``.
"""
BLUEPRINTBOOK_KEYS = (
    'item', 'label', 'label_color', 'blueprints',
    'active_index', 'version'
)

BLUEPRINT_KEYS = (
    'item', 'label', 'label_color', 'entities',
    'tiles', 'icons', 'schedules', 'description',
    'snap-to-grid', 'absolute-snapping', 'position-relative-to-grid', 'version')

#: The primary object in the blueprintbook's blueprints array.  The blueprint key's value is the blueprint object.
BLUEPRINT_CONTAINER_KEYS = ('blueprint', 'index')

#: All known container keys.  Any may be the root for a single object, and ``blueprint_book`` may have them in its ``blueprints`` array.
KNOWN_CONTAINERS = ('blueprint_book', 'blueprint', 'upgrade_planner', 'deconstruction_planner')
