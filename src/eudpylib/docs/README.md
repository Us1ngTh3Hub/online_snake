# eudpylib

This is the documentation for the extended UDP Python librabry (eudpylib).

## functionality

The library defines a network protocol, which is based on UDP but offers a lot more functionality. It is connection oriented, includes a crc checksum for the packets and splits data, which would be too long to send, in multiple packets. It also includs functions for sending keep alive packets and for checking, whether a keep alive packet has been reiceived in a given interval. The general receive function detects keep alive packets when called and calls itself again to receive the data it was intended to use. If there has been no keep alive packet in that time interval, the socket closes. Sending keep alive packets is not automated yet and still has to be implemented by the user themself, using the given functions.

## structure

The library includes three classes: a base class, a eudpyClient class and a eudpyServer class. Only the client and server class are exported and can be used by the user. The base class defines functions, which are used by both clients and servers (i. e. for sending and receiving packets) and specific functions (i. e. for establishing a connection) are defined in their respective classes. The client can use all functions as the classes eudpyClient and eudpyServer derive functionality from the base class, while still maintaining a logical seperation for the user.

## usage

The classes eudpyClient and eudpyServer each contain functions for establishing a connection, sending and receiving data aswell as closing the connection. In the folder examples you will find a simple documented program utilizing the functionality of the library.
