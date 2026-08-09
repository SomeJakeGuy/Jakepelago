from ...core.api import DEFAULT_DEVICE_ID
from ...core.platforms import PLATFORMS
from ...core.adapter import Adapter
from ...core.requests import (RequestType, RequestChain, NoOpRequest, PlatformRequest, ListDevicesRequest, ReadRequest,
    WriteRequest, SupportedOperationsRequest, PointerReadRequest, PointerWriteRequest)
from ...core.responses import (Response, ResponseChain, ResponseChainHeader, ErrorResponse, NoOpResponse,
    PlatformResponse, ListDevicesResponse, ReadResponse, WriteResponse, SupportedOperationsResponse)
from ...core.errors import ErrorType

import dolphin_memory_engine as dme

__all__ = [
    "DMEAdapter",
]

SUPPORTED_OPERATIONS = [RequestType.NO_OP, RequestType.SUPPORTED_OPERATIONS, RequestType.PLATFORM,
    RequestType.LIST_DEVICES, RequestType.READ, RequestType.WRITE]

class DMEAdapter(Adapter):
    name = "DME Adapter"
    game_id_length: int = 6
    _platform_id: int
    _device_id: bytes

    def __init__(self):
        super().__init__()

    def is_connected(self) -> bool:
        return dme.is_hooked()

    async def connect(self) -> None:
        # if game_id and not dolphin_str:
        #    self.game_id_length = len(game_id)
        #    dme.hook_by_game_id(game_id)
        # elif not game_id and dolphin_str:
        #    dmeIDs: list[int] = dme.get_process_ids(dolphin_str)
        #    dme.hook(dmeIDs[0])
        # elif game_id and dolphin_str:
        #    self.game_id_length = len(game_id)
        #    dme.get_process_id_by_game_id(game_id, dolphin_str)
        # else:
        #    dme.hook()
        dme.hook()
        dolphin_status: str = dme.get_status().name

        if not (dme.is_hooked() and dolphin_status == "hooked"):
            dme.un_hook()
            return None

        self._platform_id, self._device_id = self._read_header()

        # Dolphin either didn't load properly or DME hooked into some ghost instance of dolphin and needs to try again.
        if self._platform_id == -1 or not self._device_id:
            dme.un_hook()

        return dme.is_hooked()

    async def disconnect(self) -> None:
        dme.un_hook()

    async def send_message(self, messages: bytes) -> bytes:
        req_chain = RequestChain.from_bytes(messages)
        dev_id = req_chain.header.device_id

        if self.is_connected():
            self._platform_id, self._device_id = self._read_header()

        if dev_id not in [DEFAULT_DEVICE_ID, self._device_id]:
            return ResponseChain(ResponseChainHeader(), [
                ErrorResponse(ErrorType.MISMATCHED_DEVICE, (self._device_id if self._device_id
                    else DEFAULT_DEVICE_ID) + dev_id)]).to_bytes()

        responses: list[Response] = []

        for reqMsg in req_chain.requests:
            match reqMsg:
                case NoOpRequest():
                    responses.append(NoOpResponse())
                case SupportedOperationsRequest():
                    responses.append(SupportedOperationsResponse(SUPPORTED_OPERATIONS))
                case PlatformRequest():
                    responses.append(PlatformResponse(self._platform_id))
                case ListDevicesRequest():
                    responses.append(ListDevicesResponse([self._device_id]))
                case ReadRequest():
                    if dev_id == DEFAULT_DEVICE_ID:
                        responses.append(ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes(reqMsg.type)))
                        continue

                    responses.append(ReadResponse(dme.read_bytes(reqMsg.address, reqMsg.size)))
                case WriteRequest():
                    if dev_id == DEFAULT_DEVICE_ID:
                        responses.append(ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes(reqMsg.type)))
                        continue

                    dme.write_bytes(reqMsg.address, reqMsg.data)
                    responses.append(WriteResponse())

                case PointerReadRequest():
                    if dev_id == DEFAULT_DEVICE_ID:
                        responses.append(ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes(reqMsg.type)))
                        continue

                    responses.append(ReadResponse(dme.read_bytes(
                        dme.follow_pointers(reqMsg.base_address, reqMsg.offsets), reqMsg.size)))
                case PointerWriteRequest():
                    if dev_id == DEFAULT_DEVICE_ID:
                        responses.append(ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes(reqMsg.type)))
                        continue

                    dme.write_bytes(dme.follow_pointers(reqMsg.base_address, reqMsg.offsets), reqMsg.data)
                    responses.append(WriteResponse())
                case _:
                    responses.append(ErrorResponse(ErrorType.UNSUPPORTED_OPERATION, bytes(reqMsg.type)))

        return ResponseChain(ResponseChainHeader(), responses).to_bytes()

    def _read_header(self) -> tuple[int, bytes]:
        game_header: bytes = dme.read_bytes(0x80000000, 0x20)
        game_id_size: int = 0x06 if not self.game_id_length else self.game_id_length
        game_id: bytes = game_header[0x00:game_id_size]
        wii_magic: int = int.from_bytes(game_header[0x18:0x1C], "big")
        gc_magic: int = int.from_bytes(game_header[0x1C:0x20], "big")
        platform_id: int = -1
        if wii_magic == 0x5D1C9EA3:
            platform_id = PLATFORMS.WII._ID
        elif gc_magic == 0xC2339F3D:
            platform_id = PLATFORMS.GC._ID
        device_id = game_id.ljust(8, b"\x00")
        return platform_id, device_id