# eudpylib

This is the documentation for the extended UDP Python librabry (eudpylib).

## functionality

The library defines a network protocol, which is based on UDP but offers a lot more functionality. It is connection oriented, includes a crc checksum for the packets and splits data, which would be too long to send, in multiple packets.

## structure

The library includes three classes: a base class, a eudpyClient class and a eudpyServer class. Only the client and server class are exported and can be used by the user. The base class defines functions, which are used by both clients and servers (i. e. for sending and receiving packets) and specific functions (i. e. for establishing a connection) are defined in their respective classes. The client can use all functions as the classes eudpyClient and eudpyServer derive functionality from the base class, while still maintaining a logical seperation for the user.

## usage

The classes eudpyClient and eudpyServer each contain functions for establishing a connection, sending and receiving data aswell as closing the connection. In the folder examples you will find a simple documented program utilizing the full functionality of the library.