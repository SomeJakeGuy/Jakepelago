# Implementing an Adapter

Adapters are meant to be PolyEmu's transport protocol, handling translations between
devices that have connection methods that are non-traditional, such as SNI's gRPA API, 
a python SDK implementation that connects to an emulator like Dolphin, talking to a 
device over USB, etc. Adapters are required to handle translations of RequestChains
and ResponseChains into read, write, guard, etc. requests that devices can understand.

## When you would need an adapter

- Need a new game? See [game handler's](./Writing_a_Game_Handler.md). 
  Adapters don't know or care what game is running.
-  A new emulator that can run its own connector/plugin? If the emulator 
  can host a Lua script, native plugin, or core patch that speaks to PolyEmu 
  protocol directly, that's a new [device](./Implementing_a_Device.md) talking 
  to the *existing* `DefaultAdapter` and broker. No new adapter code needed
  the broker already routes any device that answers `List Devices` correctly, 
  regardless of which emulator it's embedded in.

## Folder / File Structure

Ideally, adapters should live in their own subdirectory in `worlds/_polyemu/adapters/`, but a dev can ship
their own adapter in their own APWorld, since Adapters are auto-registered (see `Adapter Skeleton` below). 
It is highly encouraged that you do eventually PR your adapter into polyemu after some testing is completed so 
others can use the adapter (if need be). If you do, ensure you try and follow the folder structure below:

```
worlds/_polyemu/adapters/
├── default/
│   ├── __init__.py       # from .adapter import *; __all__ = adapter.__all__
│   ├── adapter.py         # DefaultAdapter
│   └── broker.py          # the broker process this adapter talks to
├── sni/
│   ├── __init__.py
│   ├── adapter.py         # SNIAdapter
│   ├── sni.proto           # protocol definition for the bridge
│   └── sni_pb2*.py         # generated gRPC/protobuf code
└── your_adapter/
    ├── __init__.py
    └── adapter.py
```

## Adapter Skeleton

After making a subdirectory for your Adapter, simply define a class with the Adapter subclass, and it
will automatically register it. It is captured by `AutoAdapterRegister` by your adapter name, which 
must be unique across all adapters. You can easily look up adapters by performing 
`AutoAdapterRegister.get_adapter("Adapter Name")`. Additionally, you require four methods to be defined:

```python
from worlds._polyemu.core.adapter import Adapter

class ExampleAdapter(Adapter):
    name = "Example Adapter"
    
    def is_connected(self):
        ...

    async def connect(self):
        ...

    async def disconnect(self):
        ...

    async def send_message(self, message) -> bytes:
        ...
```

- `is_connected` -> Simple synchronous method that returns whether a live connection still exists. Is called
every internal `_game_watcher` iteration before passing over to game handlers
- `connect` -> Establishes a connection with a device, where True is a successful connection and False is a failure.
- `disconnect` -> Closes a connection gracefully; Needs to be safe to call even if already disconnected.
- `send_messages` -> Takes one full outgoing request chain, which are 8-byte Device ID prefixed followed by requests
  to read, write, guard etc. and returns one full response chain in return.

After defining your methods, you should create your `__init__.py` within your subdirectory and define what methods
and details are allowed to be exposed / imported via the `__all__` declaration. Once completed, ensure
that your new adapter is weired into the main init at `worlds/_polyemu/adapters/__init__.py`:
```python
from .default import *
from .sni import *
from .your_adapter import *

__all__ = (
   default.__all__ +
   sni.__all__ +
   your_adapter.__all__
)
```

## `send_messages` in further detail

### Scenario 1 - Default Adapter Style

The default adapter and its broker already understand / handle requests natively, the
only thing is that the adapter adds is the TCP length-prefix described in 
[Message Format](./Message_Format.md). In short, `send_message`: 

1. Prefixes a message with the 2-byte big-endian length and writes it.
2. Reads 2 bytes, interprets it as a length, then reads that many more bytes.
3. Returns those bytes untouched as a valid ResponseChain.

### Scenario 2 - Other Adapters

SNI adapter for example has its own request and response shapes and has no native concept
of chains or guards for example. Here instead, `send_message` acts as the PolyEmu protocol
translator. A short list of recommendations for an implementation would look like:

1. Parse incoming bytes into chains (there are classes in `worlds\_polyemu\core\requests.py`
    that can be reused for parsing).
2. Handle `DEFAULT_DEVICE_ID` cases yourself if the protocol has no concept/equivalent method.
    For Example, SNI handles `NoOp`, `SupportedOperations`, `ListDevices`, and `Platform` locally.
3. Translate each `Request` into whatever the adapter protocol exposes (address-space
   translation, batching multiple reads into one bulk call, etc. as needed)
4. Build a single `Response` per input request in the same order received, including any
    UNSUPPORTED_OPERATION requests for anything your adapter cannot handle (i.e. Lock or Unlock).
5. Serialize the resulting `ResponseChain` back into bytes before returning it.

If the target device software is closer to raw memory-mapped access for example, you may not need
to do translation, pushing yourself closer to being in Scenario 1. Translation is only really
required when your creating a bridge to something that already has its own fixed protocol.

## Errors

PolyEmu exposes a base `PolyEmuBaseError` class that can be adapted to provide your own errors
as needed. However, there are some errors that already exist, like `NotConnectedError` or
`ConnectionLostError` that already exist for connection related failures.