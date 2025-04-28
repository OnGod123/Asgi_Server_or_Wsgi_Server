
async def reader_read_frame(reader: StreamReader):
    header = await reader.readexactly(2)
    b1, b2 = header; length = b2 & 0x7F
    if length==126: ext = await reader.readexactly(2); length = int.from_bytes(ext,'big')
    mask = await reader.readexactly(4) if (b2>>7) else None
    data = await reader.readexactly(length)
    if mask: data = bytes(b ^ mask[i%4] for i,b in enumerate(data))
