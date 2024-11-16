"""Services that provides methods to interact with a Nextcloud fsnode."""

import io
import pathlib
from typing import BinaryIO, Self

from aiogram.types import BufferedInputFile
from nc_py_api import AsyncNextcloud, FsNode

from bot.core import settings
from bot.nextcloud._base import BaseService
from bot.nextcloud.exceptions import FsNodeNotFoundError


class BaseFsNodeService:
    """Base class for all fsnode services.

    :param nc: The Nextcloud client object.
    :param fsnode: The fsnode object.
    :param attached_fsnodes: The list of attached fsnodes.
    """

    def __init__(self, nc: AsyncNextcloud, fsnode: FsNode, attached_fsnodes: list[FsNode]) -> None:
        self.nc = nc
        self.fsnode = fsnode
        self.attached_fsnodes = attached_fsnodes

    @staticmethod
    async def _check_is_root_id(nc: AsyncNextcloud, file_id: str) -> FsNode:
        """Check if the given file id is the id of the root fsnode.

        :param nc: The Nextcloud client object.
        :param fsnode: The fsnode object.
        :return: Tuple with root fsnode and attached to root fsnodes.
        """
        fsnodes_list = await nc.files.listdir(exclude_self=False)
        if fsnodes_list[0].file_id == file_id:
            return fsnodes_list[0], fsnodes_list[1:]
        raise FsNodeNotFoundError

    def _generate_unique_name(self, name: str) -> str:
        """Generate a unique name for a fsnode.

        :param name: The proposed name for the file.
        :return: Unique name for a fsnode.
        """
        i = 1
        path = pathlib.Path(name)
        while name in [fsnode.name for fsnode in self.attached_fsnodes]:
            name = f"{path.stem} ({i}){path.suffix}"
            i += 1
        return name

    async def mkdir(self, name: str) -> FsNode:
        """Create a new directory in the current fsnode.

        :param name: The name of the new directory.
        :return: The created directory.
        """
        if not self.fsnode.is_dir:
            msg = "Cannot create directory because the parent node is not a directory."
            raise ValueError(msg)

        name = self._generate_unique_name(name)
        new_dir = await self.nc.files.mkdir(f"{self.fsnode.user_path}{name}")

        self.attached_fsnodes.append(new_dir)

        return new_dir

    async def delete(self) -> None:
        """Delete the current fsnode."""
        await self.nc.files.delete(self.fsnode)

    async def download(self) -> BufferedInputFile:
        """Download the current fsnode.

        :return: The downloaded fsnode.
        """
        buff = io.BytesIO()
        await self.nc.files.download2stream(self.fsnode, buff, chunk_size=settings.nc.CHUNKSIZE)

        buff.seek(0)
        return BufferedInputFile(buff.read(), filename=self.fsnode.name)

    async def upload(self, buff: BinaryIO, name: str) -> FsNode:
        """Upload a file to the current fsnode.

        :param buff: The file to upload.
        :param name: The name of the file.
        :return: The newly uploaded file.
        """
        if not self.fsnode.is_dir:
            msg = "Cannot upload file because the parent node is not a directory."
            raise ValueError(msg)

        name = self._generate_unique_name(name)

        buff.seek(0)
        return await self.nc.files.upload_stream(
            f"{self.fsnode.user_path}{name}",
            buff,
            chunk_size=settings.nc.CHUNKSIZE,
        )


class RootFsNodeService(BaseService[BaseFsNodeService], BaseFsNodeService):
    """Service for the root fsnode."""

    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud) -> Self:
        """Create a RootFsNodeService object for the root fsnode.

        :param nc: The Nextcloud client object.
        :return: The RootFsNodeService object.
        """
        fsnodes_list = await nc.files.listdir(exclude_self=False)
        return cls(nc, fsnodes_list[0], fsnodes_list[1:])


class FsNodeService(BaseService[BaseFsNodeService], BaseFsNodeService):
    """Service for a non root fsnode."""

    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, file_id: str) -> Self:
        """Create a FsNodeService object for the given fsnode.

        The function does an additional check for root fsnode because
        AsynNextcloud does not return root fsnode by file_id.

        :param nc: The Nextcloud client object.
        :param file_id: The file id of the fsnode.
        :return: The FsNodeService object.
        """
        fsnode = await nc.files.by_id(file_id)
        if fsnode is None:
            fsnode, attached_fsnodes = await cls._check_is_root_id(nc, file_id)
            return cls(nc, fsnode, attached_fsnodes)
        attached_fsnodes = await nc.files.listdir(fsnode)
        return cls(nc, fsnode, attached_fsnodes)


class PrevFsNodeService(BaseService[BaseFsNodeService], BaseFsNodeService):
    """Service for a fsnode that is the parent of the current fsnode."""

    @classmethod
    async def create_instance(cls, nc: AsyncNextcloud, file_id: str) -> Self:
        """Create a PrevFsNodeService object for the given fsnode.

        The function does an additional check for root fsnode because
        AsynNextcloud does not return root fsnode by file_id.

        :param nc: The Nextcloud client object.
        :param file_id: The file id of the fsnode.
        :return: The PrevFsNodeService object.
        """
        fsnode = await nc.files.by_id(file_id)
        if fsnode is None:
            fsnode, attached_fsnodes = await cls._check_is_root_id(nc, file_id)
            return cls(nc, fsnode, attached_fsnodes)

        path = pathlib.Path(fsnode.user_path)
        prev_path = str(path.parent) if str(path.parent) != "." else ""

        fsnode = await nc.files.by_path(prev_path)
        attached_fsnodes = await nc.files.listdir(fsnode)
        return cls(nc, fsnode, attached_fsnodes)
