"""
Auto-discover and import all screen modules.
Any Python file in this directory (except __init__.py) will be imported,
and any class ending with 'Screen' will be exported.
"""
import importlib
import pkgutil
from pathlib import Path

# Auto-discover all screen modules
_package_path = Path(__file__).parent
_screen_classes = {}

for importer, modname, ispkg in pkgutil.iter_modules([str(_package_path)]):
    if not ispkg and not modname.startswith('_'):
        module = importlib.import_module(f'{__name__}.{modname}')
        # Find all Screen classes in the module
        for attr_name in dir(module):
            if attr_name.endswith('Screen') and not attr_name.startswith('_'):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    _screen_classes[attr_name] = attr
                    # Make it available at package level
                    globals()[attr_name] = attr

__all__ = list(_screen_classes.keys())
