import sys
from typing import Sequence

from .adapter import Adapter
from .errors import AutoPolyEmuErrorRegister, PolyEmuError
from .requests import Request, NoOpRequest, ListDevicesRequest, ReadRequest, WriteRequest, GuardRequest, LockRequest, \
    UnlockRequest, SupportedOperationsRequest, PlatformRequest, MemorySizeRequest, DisplayMessageRequest, \
    PointerReadRequest, PointerWriteRequest
from .responses import ResponseType, Response, ResponseChain, ErrorResponse, ListDevicesResponse, ReadResponse, \
    GuardResponse, MemorySizeResponse, SupportedOperationsResponse, LockResponse, UnlockResponse, PlatformResponse, \
    DisplayMessageResponse


__all__ = [
    "DEFAULT_DEVICE_ID", "PolyEmuContext", "send_requests", "no_op", "list_devices",
    "get_memory_size", "get_platform", "get_supported_operations",
    "guarded_read", "read", "write", "lock", "unlock", "display_message", "pointer_read", "pointer_write"
]


DEFAULT_DEVICE_ID = b"\x00\x00\x00\x00\x00\x00\x00\x00"


class PolyEmuContext:
    adapter: Adapter
    selected_device_id: bytes

    def __init__(self, adapter_type: type[Adapter]):
        self.adapter = adapter_type()
        self.selected_device_id = DEFAULT_DEVICE_ID


async def send_requests(ctx: PolyEmuContext, request_list: list[Request]) -> list[Response]:
    message = bytes()
    for request in request_list:
        message += request.to_bytes()
    message = ctx.selected_device_id + message

    received = await ctx.adapter.send_message(message)
    response_list = ResponseChain.from_bytes(received).responses

    error_list: list[PolyEmuError] = []

    for response in response_list:
        if response.type == ResponseType.ERROR:
            assert isinstance(response, ErrorResponse)
            error_list.append(AutoPolyEmuErrorRegister.get_error_type(response.error_code).from_response(response))

    if error_list:
        if len(error_list) == 1 or sys.version_info < (3, 11, 0):
            raise error_list[0]
        else:
            raise ExceptionGroup("Emulator returned errors", error_list)  # noqa

    return response_list


async def no_op(ctx: PolyEmuContext) -> None:
    await send_requests(ctx, [NoOpRequest()])


async def list_devices(ctx: PolyEmuContext) -> list[bytes]:
    original_device_id = ctx.selected_device_id
    ctx.selected_device_id = DEFAULT_DEVICE_ID
    res: ListDevicesResponse = (await send_requests(ctx, [ListDevicesRequest()]))[0]
    ctx.selected_device_id = original_device_id
    return res.devices


async def get_memory_size(ctx: PolyEmuContext) -> dict[int, int]:
    res: MemorySizeResponse = (await send_requests(ctx, [MemorySizeRequest()]))[0]
    return res.memory_sizes


async def get_platform(ctx: PolyEmuContext) -> int:
    res: PlatformResponse = (await send_requests(ctx, [PlatformRequest()]))[0]
    return res.platform_id


async def get_supported_operations(ctx: PolyEmuContext) -> list[int]:
    res: SupportedOperationsResponse = (await send_requests(ctx, [SupportedOperationsRequest()]))[0]
    return res.supported_operations[:]


async def _send_guarded(ctx: PolyEmuContext, requests: list[Request],
    guard_list: Sequence[tuple[int, Sequence[int], int]]) -> list[Response] | None:

    guards = [GuardRequest(domain, address, expected_data) for address, expected_data, domain in guard_list]
    response_list = await send_requests(ctx, guards + requests)
    guard_responses: list[GuardResponse] = response_list[:len(guards)]
    remaining = response_list[len(guards):]

    for res in guard_responses:
        if not res.validated:
            return None

    return remaining


async def guarded_read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, int, int]],
    guard_list: Sequence[tuple[int, Sequence[int], int]]) -> list[bytes] | None:
    """
    Performs a Guarded read request using the provided read list.
    Expects an order of tuple[int, int, int]: ram address, size of bytes to read, and which domain to read from.
    """

    reads = [ReadRequest(domain, address, size) for address, size, domain in read_list]
    responses: list[ReadResponse | GuardResponse] = await _send_guarded(ctx, reads, guard_list)
    return None if responses is None else [res.data for res in responses]


async def guarded_pointer_read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, Sequence[int], int, int]],
    guard_list: Sequence[tuple[int, Sequence[int], int]]) -> list[bytes] | None:
    """
    Performs a Guarded read request using the provided read list and any related pointer offset chains.
    Expects an order of tuple[int, Sequence[int], int, int]: ram address, offsets from the pointer address that was
        last read, size of bytes to read, and which domain to read from.
    """

    reads = [PointerReadRequest(domain, base_address, offsets, size) for base_address, offsets, size, domain in read_list]
    responses: list[ReadResponse | GuardResponse] = await _send_guarded(ctx, reads, guard_list)
    return None if responses is None else [res.data for res in responses]


async def read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, int, int]]) -> list[bytes]:
    """
    Performs a Read request using the provided read list.
    Expects an order of tuple[int, int, int]: ram address, size of bytes to read, and which domain to read from.
    """
    return await guarded_read(ctx, read_list, [])


async def pointer_read(ctx: PolyEmuContext, read_list: Sequence[tuple[int, Sequence[int], int, int]]) -> list[bytes]:
    """
    Performs a Read request using the provided read list and any related pointer offset chains.
    Expects an order of tuple[int, Sequence[int], int, int]: ram address, offsets from the pointer address that was
        last read, size of bytes to read, and which domain to read from.
    """
    return await guarded_pointer_read(ctx, read_list, [])


async def guarded_write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], int]],
    guard_list: Sequence[tuple[int, Sequence[int], int]]) -> bool:
    """
    Performs a Guarded write request using the provided read list.
    Expects an order of tuple[int, Sequence[int], int]: ram address, bytes as an int Sequence to write back to the
        ram address, and which domain to read from.
    """

    writes = [WriteRequest(domain, address, data) for address, data, domain in write_list]
    return await _send_guarded(ctx, writes, guard_list) is not None


async def guarded_pointer_write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], Sequence[int], int]],
    guard_list: Sequence[tuple[int, Sequence[int], int]]) -> bool:
    """
    Performs a Guarded write request using the provided read list and any related pointer offset chains.
    Expects an order of tuple[int, Sequence[int], Sequence[int], int]: ram address, offsets from the pointer address
        that was last read, bytes as an int Sequence to write back to the ram address, and which domain to read from.
    """

    writes = [PointerWriteRequest(domain, base_address, offsets, data) for base_address, offsets, data, domain in write_list]
    return await _send_guarded(ctx, writes, guard_list) is not None


async def write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], int]]) -> None:
    """
    Performs a Write request using the provided read list.
    Expects an order of tuple[int, Sequence[int], int]: ram address, bytes as an int Sequence to write back to the
        ram address, and which domain to read from.
    """
    await guarded_write(ctx, write_list, [])


async def pointer_write(ctx: PolyEmuContext, write_list: Sequence[tuple[int, Sequence[int], Sequence[int], int]]) -> None:
    """
    Performs a Write request using the provided read list and any related pointer offset chains.
    Expects an order of tuple[int, Sequence[int], Sequence[int], int]: ram address, offsets from the pointer address
        that was last read, bytes as an int Sequence to write back to the ram address, and which domain to read from.
    """

    await guarded_pointer_write(ctx, write_list, [])


async def lock(ctx: PolyEmuContext) -> None:
    res: LockResponse = (await send_requests(ctx, [LockRequest()]))[0]


async def unlock(ctx: PolyEmuContext) -> None:
    res: UnlockResponse = (await send_requests(ctx, [UnlockRequest()]))[0]


async def display_message(ctx: PolyEmuContext, message: str) -> None:
    res: DisplayMessageResponse = (await send_requests(ctx, [DisplayMessageRequest(message)]))[0]
