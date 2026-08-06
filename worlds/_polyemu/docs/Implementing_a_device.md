# Implementing a Device

Devices can be emulators (which either connect directly, having a scripting language, a plugin, etc.),
physical hardware (such as connecting directly to a GameCube or Wii), or anything else similar. Each device has its 
own unique 8-byte **Device ID**. Connections can be anything, such as a JavaScript or Lua script that 
talks directly to the emulator, a native plugin in the emulator, networking code on a hardware device, etc.
This document specifies what a device must implement to be considered valid. If you are trying to implement a game,
see [Writing a Game Handler](./Writing_a_game_handler.md). It is recommended to also read 
[Message Format](./Message_Format.md) at the same time, which explains the byte behavior.

## Transport and framing

- The device **connects out** to the broker over TCP at `127.0.0.1:43031` (`DEVICE_PORT`).
  The broker is the server; the device is the client of that socket. (If you talk to a client
  directly without a broker, you take the broker's place on this socket instead.)
- Every message — in both directions — is prefixed with a **2-byte big-endian length**,
  giving the number of bytes that follow:

  ```
  ┌────────────┬───────────────────────────┐
  │ size (2 B) │chain bytes (`size` bytes) │
  └────────────┴───────────────────────────┘
  ```
  
So reading a message is always: read 2 bytes → interpret as big-endian length `n` → read
  `n` more bytes. A read of 0 bytes means the peer closed the connection.
- All multibyte integers in the protocol are **big-endian**.
- The exchange is strictly **request → response, one for one**. For every request in an
  incoming chain you emit exactly one response, in the same order.
- Incoming requests require an 8-byte Device ID, but responses do not, however both require a 1-byte
  type code followed by the type-specific body.

## Device IDs

Each device should manage and handle creating unique device IDs, which will be used
to uniquely identify connections, such as two different BizHawk connections
simultaneously running on your computer. It is recommended that devices use something
stable, yet related to a running game, such as a hash of a game name, save file 
guids, in-rom checksums, etc.

## The registration handshake (do this first)

As soon as a device connects, the broker sends it a chain addressed to the **all-zero
device ID** containing a single **List Devices** request, and expects a **List Devices
response** back. The broker takes `devices[0]` from that response as *the* ID for this
connection. Concretely (from `broker.py:request_id`):

```
broker → device :  [size][ 00 00 00 00 00 00 00 00 ][ 04 ]              (List Devices request)
device → broker :  [size][ 84 ][ 01 ][ <your 8-byte id> ]               (List Devices response)
                            └─ 0x84 = LIST_DEVICES response
                                   └─ count = 1
```

If your first response isn't a List Devices response, the broker discards the connection. So
**a device must answer List Devices before anything else will happen.**

After that, the broker records your ID and begins forwarding client request chains to you.

## Handling the device-ID header

Every forwarded request chain begins with an 8-byte device ID. Two cases you must honor:

- **All-zero ID** — a "don't check" or broadcast address, which fulfills a request without
  verifying identity.
- **A specific ID** — you should compare it to your own. If it does **not** match, respond with a single
  `Mismatched Device` error (`0x02`) instead of processing the chain. In practice the broker
  only routes matching chains to you, but the check is part of the contract.

## Processing Request Chains

See the aforementioned [Message Format](./Message_Format.md) for the various request types that are supported. 
You do **not** have to support every type of request. Advertise what you do support via `Supported Operations`; 
for anything you don't implement, respond with an `Unsupported Operation` error (`0x01`) whose body is the 
unsupported request type byte.

### Reads and writes
`domain` is a 1-byte domain ID scoped to your platform (see
[platforms](#platforms-and-domains)). `address` is 8 bytes; `size` (read) and data length
(write) are 2 bytes. Map `(domain, address)` onto the appropriate emulated memory region and
read/write raw bytes. A read response is the 2-byte length of the data followed by the data
itself.

### Guards — the skip mechanism
A `Guard` request compares the `size` bytes at `(domain, address)` against the request's expected
bytes.

If the request:
- **Matches:** your device should emit `0x92` with `validated = 1`, then processing the chain normally.
- **Mismatches:** your device should emit `0x92` with `validated = 0`, and **skip every remaining request in the
  chain**. Each skipped request should also get a `0x92` guard response with `validated = 0` rather than its normal 
  response. 

If the RAM state changes values or moves while trying to write, then the write request fais. Once a guard fails, 
respond to all subsequent requests with a guard response and do nothing else / stop processing further requests.

### Lock or Unlock
`Lock` should halt emulation but **continue processing the current chain**. An example request chain would look like:
`guard, lock, read, write, and then finally unlock` in one go. `Unlock` resumes emulation;
requests after it in the same chain are still processed on this frame.

## Platforms and domains

Report your platform via the Platform request using the IDs in `core/platforms.py`. Each platform defines its 
own domain IDs (e.g. GBA: `EWRAM = 0x02`, `IWRAM = 0x03`, `ROM = 0x08`, etc. see the table in 
[Writing a Game Handler](./Writing%20a%20Game%20Handler.md)). Your read, write, or guard handling must interpret domain IDs the same way. 
There is also a special `SYSTEM` domain (`0x00`) meaning a flattened whole-system address space, if your
device exposes one. `Memory Size` should report the size of each domain you support (and
omit those you don't).

## Staying connected

The broker expects timely responses from the various connected devices. If it sends a
request and doesn't get a response within ~5 seconds it treats the device as gone and drops
it, so don't block your game_watcher loop on long device operations without answering.