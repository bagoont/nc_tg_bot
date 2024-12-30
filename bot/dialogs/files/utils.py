from nc_py_api import AsyncNextcloud, FsNode


async def fetch_fsnodes(nc: AsyncNextcloud, path: str | FsNode) -> list[FsNode]:
    fsnodes = await nc.files.listdir(path, exclude_self=False)
    return [fsnodes[0], *sorted(fsnodes[1:], key=lambda fsnode: fsnode.is_dir, reverse=True)]
