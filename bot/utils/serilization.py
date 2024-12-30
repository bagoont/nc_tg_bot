from typing import Any

from aiogram.types import Document
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from nc_py_api import FsNode


def as_obj(dct: dict[Any, Any]) -> FsNode | dict[Any, Any]:
    if dct.get("__class__") == Document.__name__:
        del dct["__class__"]
        return Document.model_validate(dct)
    if dct.get("__class__") == FsNode.__name__:
        return FsNode(**dct)
    return dct


def default(obj: Any) -> Any:
    if isinstance(obj, Document):
        dct = deserialize_telegram_object_to_python(obj)
        dct["__class__"] = Document.__name__
        return dct
    if isinstance(obj, FsNode):
        dct = {
            "__class__": FsNode.__name__,
            "full_path": obj.full_path,
            "file_id": obj.file_id,
            "etag": obj.etag,
            "content_length": obj.info.content_length,
            "size": obj.info.size,
            "permissions": obj.info.permissions,
            "mimetype": obj.info.mimetype,
            "favorite": obj.info.favorite,
            "fileid": obj.info.fileid,
            "last_modified": obj.info.last_modified.isoformat(),
            "is_locked": obj.lock_info.is_locked,
            "lock_owner_type": obj.lock_info.type.value,
            "lock_owner": obj.lock_info.owner,
            "owner_display_name": obj.lock_info.owner_display_name,
            "lock_owner_editor": obj.lock_info.owner_editor,
            "lock_time": obj.lock_info._lock_time,  # noqa: SLF001
            "_lock_ttl": obj.lock_info.lock_ttl,
        }

        if obj.info.trashbin_filename:
            dct["trashbin_filename"] = obj.info.trashbin_filename

        if obj.info.trashbin_original_location:
            dct["trashbin_original_location"] = obj.info.trashbin_original_location

        if obj.info.trashbin_deletion_time:
            dct["trashbin_deletion_time"] = obj.info.trashbin_deletion_time
        return dct
    msg = f"Object of type {obj.__class__.__name__} " f"is not JSON serializable"
    raise TypeError(msg)
