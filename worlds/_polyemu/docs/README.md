# PolyEmu

## What is PolyEmu?

PolyEmu is a general purpose client that can talk to many different devices and platforms.
Its purpose is to provide a single client to handle the connection / integration between Archipelago (AP) and your
Device of choice. Devices can be emulators (which either connect directly, having a scripting language, a plugin, etc.),
physical hardware (such as connecting directly to a GameCube or Wii), or anything else similar. Each device has its 
own unique 8-byte **Device ID**. PolyEmu provides a single protocol that needs to be adapted per device, 
allowing for support of multiple emulators / devices for free.

## For players, what do you do to run this?

As a player, you should be able to open one or more PolyEmu clients to connect to your device of choice.
Once open, PolyEmu should automatically detect the device running and "hook" into it. Once hooked, you can then
connect as you normally would to Archipelago (type the url and port, provide slot name and password, then connect.)

## As a developer, what does this mean for me?

As a developer, as long as the connection for a given device already exists, you don't have to worry about writing
the connection details between an device and your client, you can simply make your client and use the provided
functionality to send checks, receive items, etc. You also get multi-emulator support for free, without having to make
any further changes to your client at all. Instead, you just have to extend this client and overwrite the required 
functions to, for example, read various RAM address to detect if a location has been checked.

If you are making a new game for an existing platform / handler, see: [Writing a Game Handler](./Writing_a_game_handler.md)

The current list of supported platforms are:
- Game Boy (GB)
- Game Boy Color (GBC)
- Game Boy Advance (GBA)
- Super Nintendo Entertainment System (SNES)
- Wii
- GameCube (GC)

If a device doesn't exist yet, see: [Implementing a Device](./Implementing_a_device.md) Note: If a device can connect 
to the broker server (see below), such as a lua script for BizHawk, no separate implementation is required.

### At a high level, how does this work?

PolyEmu works as a three-way pair of processes all talking to each other across various ports on your system:

```
AP Client                  Broker            
(PolyEmuClient) <------->  (router) <-------> Device
Port: 43030                Port: 43031       
```

The **Client** handles communication between the Archipelago server and the devices. 
PolyEmu's client is CommonClient based and extends all functionality already provided 
(see [Archipelago CommonClient](https://github.com/ArchipelagoMW/Archipelago/blob/main/CommonClient.py)) 
Additionally, it also handles finding one or more devices, determining its platform, finds a matching **game handler**
(aka a client for a given game), then loops forever until the user closes the AP connection or their device.

The **broker** is a small local router. It handles the following:
* Device registration
* Providing a list available devices to a PolyEmuClient
* Requests sent to a given Device ID
* Communication between Client and Devices.

By using a broker, it also allows for multiple connections and multiple devices to co-exist. It should be noted that 
some devices can handle connections on their own directly to PolyEmuClient, rather than using the broker.

PolyEmu handles communication via a **request chain**, which consists of a target Device ID followed by a batch of 
requests (read, writes, guards, etc.). Chains can be conditionally aborted mid-way through with "guard" requests.

