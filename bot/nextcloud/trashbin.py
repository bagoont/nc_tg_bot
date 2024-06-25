from typing import Self

from nc_py_api import AsyncNextcloud, FsNode

from bot.nextcloud.factory import FactorySubject


class BaseTrashbinService:
    def __init__(self, nc: AsyncNextcloud, trashbin: list[FsNode]) -> None:
        self.nc = nc
        self.trashbin = trashbin

    def _get_trashbin_item_by_id(self, file_id: str) -> FsNode | None:
        for trashbin_item in self.trashbin:
            if trashbin_item.file_id == file_id:
                return trashbin_item
        return None

    async def delete(self, file_id: str) -> None:
        trashbin_item = self._get_trashbin_item_by_id(file_id)
        if trashbin_item is None:
            raise ValueError

        await self.nc.files.trashbin_delete(trashbin_item)
        self.trashbin.remove(trashbin_item)

    async def restore(self, file_id: str) -> None:
        print("YOOOOOOLLLOOO")
        trashbin_item = self._get_trashbin_item_by_id(file_id)
        if trashbin_item is None:
            raise ValueError

        await self.nc.files.trashbin_restore(trashbin_item)
        self.trashbin.remove(trashbin_item)

    async def cleanup(self) -> None:
        await self.nc.files.trashbin_cleanup()
        self.trashbin = []


class TrashbinService(BaseTrashbinService, FactorySubject):
    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud) -> Self:
        trashbin = await nc.files.trashbin_list()
        return cls(nc, trashbin)
