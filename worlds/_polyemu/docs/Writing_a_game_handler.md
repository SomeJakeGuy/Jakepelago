# Writing a Game Handler

A **game handler** is created to handle supporting a given game.
Game Handlers are created by making subclasses of `PolyEmuClient` (`worlds/_polyemu/client.py`) that live 
in your world package. You do not need to write any networking or device discovery or the protocol to communicate
to a given device. Instead, all you need to focus on is managing the addresses for locations, receiving items from
the Multiserver, or other client implemented protocols like DeathLink.

## The Skeleton

```python
import worlds._polyemu as polyemu

class MyGameClient(polyemu.PolyEmuClient):
    game = "My Game"                       # must match your world's game name
    platform = polyemu.PLATFORMS.GBA       # one platform, or a tuple of platforms
    patch_suffix = ".apmygame"             # patch extension(s) this client opens, or None

    async def validate_rom(self, ctx) -> bool: ...
    async def game_watcher(self, ctx) -> None: ...
```

Simply defining the subclass registers it. `AutoPolyEmuClientRegister` (the metaclass for `PolyEmuClient`) files 
your class under its `platform`, and `patch_suffix` is automatically added to the launcher so 
double-clicking a matching patch file opens the PolyEmu client.

## Methods to implement

### `validate_rom(ctx) -> bool`
This function is called when PolyEmu thinks it found a device on your platform and needs to know whether 
*this* handler is allowed to use it. Ideally, the best thing you can do is read some information such as the
ROM Header, the game ID, or something that validates the ROM loaded is the game you expected. Note: PolyEmu
will handle validating if the device is on your system, so you only need to validate the game.

An Example based on Pokemon Emerald's implementation:
```python
async def validate_rom(self, ctx) -> bool:
    rom_name_bytes = (await polyemu.read(ctx.polyemu_ctx, [(RAM_ADDR, 32, DOMAINS.ROM)]))[0]
    rom_name = bytes(b for b in rom_name_bytes if b != 0).decode("ascii")
    if not rom_name.startswith("pokemon emerald version"):
        return False
    # ... version checks ...

    ctx.game = self.game
    ctx.items_handling = 0b001      # how the server should send items, see world api.md
    ctx.want_slot_data = True
    ctx.watcher_timeout = 1         # how often game_watcher runs, in seconds
    self.initialize_client()        # reset your per-connection state
    return True
```

### `game_watcher(ctx) -> None`

This is the main per-game loop body, which is called repeatedly in between a delay that is 
configured via `ctx.watcher_timeout`, but only if the ROM has been validated and if a device is connected.
In this loop, this is where you would:
- read game memory to detect newly checked locations and report them to the server,
- write items the server has sent you into the game's memory,
- handle features like DeathLink, goal completion, etc.

### `set_auth(ctx) -> None` (optional)

If you store the slot name in your patched ROM, PolyEmu exposes this function to easily set ctx.auth, allowing
a player to have their slot name automatically retrieved rather than having them type it.

An Example:
```python
async def set_auth(self, ctx) -> None:
    auth_raw = (await polyemu.read(ctx.polyemu_ctx, [(RAM_ADDR, 16, DOMAINS.ROM)]))[0]
    ctx.auth = auth_raw.decode("utf-8")
```

### `on_package(ctx, cmd, args) -> None` (optional)

This function helps to route various packets and commands that are sent from the server to a client on a conected slot.
This includes things like, on connection to server, items received from server, deathlink, etc.

## How it works once implemented

1. PolyEmu connects to a device and asks it for its **platform**.
2. It calls `AutoPolyEmuClientRegister.get_handler`, which tries every handler registered for
   that platform and returns the first whose `validate_rom` returns `True`.
3. From then on, it calls that handler's `game_watcher` every `watcher_timeout` seconds,
   and routes server packets to `on_package`.

So the minimum viable handler is: declare `game` and `platform`, identify your
ROM in `validate_rom`, and do your sync work in `game_watcher`. Everything else is optional.

## Other Important Notes

When reading and writing to memory, as mentioned you will be passing a **list** of operations and you get
your results back in the same order, however all values are raw bytes, so you are responsible for converting back
to your game's endianness. Additionally, if you have a game that tends to update its RAM address frequently, PolyEmu
provides you with guarded reads and writes, which ensures that the RAM address has an expected value prior to 
reading or writing, otherwise the operation(s) are skipped.

An Example from Pokemon Emerald:
```python
guards = {
    "IN OVERWORLD": int(1).to_bytes(4, "little"), DOMAINS.SYSTEM),
}

read_result = await polyemu.guarded_read(
    ctx.polyemu_ctx,
    [(addr, 2, DOMAINS.SYSTEM)],       # what to read
    [guards["IN OVERWORLD"]],          # guards that must hold
)
if read_result is None:
    return   # a guard failed (e.g. player left the overworld) — try again next loop
```

`guarded_read` returns `None` if any guard failed (otherwise a `list[bytes]`);
`guarded_write` returns `False` if any guard failed (otherwise `True`). 
PolyEmu also supports lock / unlock functionality, which will completely freeze an emulator to adjust RAM,
but in general it is preferable to use guards instead. Note: Not every device in PolyEmu
can support guards or lock / unlock functionality.

Other supported functionality includes `polyemu.display_message`, `polyemu.get_memory_size`,
and `polyemu.get_supported_operations`.