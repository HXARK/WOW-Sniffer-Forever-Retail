"""Persist and check the selected capture folder."""
import json
import os
from pathlib import Path
import tempfile

from .updates import safe_store, read_bounded


def _path(value):
    if type(value) is not str or not value or len(value) > 4096:
        raise ValueError('invalid_capture_folder')
    path = Path(value)
    if not path.is_absolute():
        raise ValueError('invalid_capture_folder')
    return path


def load(settings):
    target = Path(settings)/'capture-folder.json'
    if not target.exists():
        return Path(settings)
    value = json.loads(read_bounded(target))
    if type(value) is not dict or set(value) != {'path'}:
        raise ValueError('invalid_capture_folder')
    return _path(value['path'])


def prepare(root):
    root = _path(str(root))
    # A disconnected or removed drive must not redirect captures elsewhere.
    if not root.is_dir():
        raise ValueError('capture_folder_unavailable')
    root = safe_store(root)
    captures, dumps = safe_store(root/'captures'), safe_store(root/'dumps')
    # Final exports use atomic hard links. Check support before recording.
    fd, name = tempfile.mkstemp(prefix='.storage-', dir=dumps)
    link = name+'.check'
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(b'HXARK');stream.flush();os.fsync(stream.fileno())
        os.link(name, link)
    finally:
        Path(link).unlink(missing_ok=True)
        Path(name).unlink(missing_ok=True)
    return captures, dumps


def save(settings, root):
    root = _path(str(root))
    prepare(root)
    settings = safe_store(settings)
    target = settings/'capture-folder.json'
    if target.exists() or target.is_symlink():
        read_bounded(target)
    fd, name = tempfile.mkstemp(prefix='capture-folder-', suffix='.tmp', dir=settings)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump({'path':str(root)},stream);stream.flush();os.fsync(stream.fileno())
        os.replace(name,target)
    finally:
        Path(name).unlink(missing_ok=True)
    return root
