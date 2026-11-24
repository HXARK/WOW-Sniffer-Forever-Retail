"""Persist the selected WoW executable path."""
import json
import os
from pathlib import Path
import tempfile

from .updates import safe_store, read_bounded


def candidates(wow):
    """Find Retail and Forever beside the selected installation."""
    wow = Path(wow)
    paths = [wow]
    if wow.parent.name.lower() in ('_retail_', '_forever_'):
        paths.extend(wow.parent.parent/name/'Wow.exe' for name in ('_retail_', '_forever_'))
    return tuple(dict.fromkeys(path.resolve() for path in paths if path.is_file()))


def _validated(value):
    if type(value) is not str or not value or len(value) > 4096:
        raise ValueError('invalid_wow_location')
    path = Path(value)
    if not path.is_absolute() or path.name.lower() != 'wow.exe' or not path.is_file():
        raise ValueError('invalid_wow_location')
    return path.resolve(strict=True)


def load(root):
    try:
        path = Path(root) / 'wow-location.json'
        if path.stat().st_size > 8192:
            return None
        value = json.loads(read_bounded(path))
        if type(value) is not dict or set(value) != {'path'}:
            return None
        return _validated(value['path'])
    except (OSError, ValueError, TypeError):
        return None


def save(root, wow):
    path = _validated(str(wow))
    root = safe_store(root)
    target = root / 'wow-location.json'
    if target.is_symlink() or (target.exists() and
            (target.stat().st_nlink != 1 or getattr(target.stat(), 'st_file_attributes', 0) & 0x400)):
        raise ValueError('linked_wow_location')
    # A failed write leaves the previous selection intact.
    fd, name = tempfile.mkstemp(prefix='wow-location-', suffix='.tmp', dir=root)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump({'path': str(path)}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return path
