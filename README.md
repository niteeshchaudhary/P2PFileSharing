A peer-to-peer file transfer application, comprising one manager and multiple peers.

1. Manager
(i) A manager is an always-ON server, which maintains the list of currently active peers across the network at all times.
(ii) A newly arrived peer connects to the manager
 The manager adds this newly arrived peer to its list of active peers, and, 
      b)   broadcasts the updated list.
(iii) The manager periodically:
 checks availability of active peers from its list, 
 updates the same, if some peer(s) leave(s) the network, and,
 broadcasts the updated list.
(iv) A peer informs the manager when it leaves the network
 The manager deletes this peer from its list of active peers, and,
 broadcasts the updated list.

2. Peer
(i) A new peer is expected to know the manager’s IP and port. It pings the manager , and saves the list of active peers sent by the manager . 
(ii) It also maintains a list of shareable files .
(iii) Before going offline, a peer informs the manager .

(iv)To fetching a file from other peer(s), a peer:
 broadcasts its requirement to all peers (from its list of active peers)
 based on received responses, parallely fetches different fragments of the required file from available peers
 if any of the transmitting peers go offline, the requesting peer fetches its missing fragments from the remaining available peers

(v) On being requested to share a file by another peer, a peer:
 informs the requesting peer of its availability
transmits the requested fragment(s) of one of its shareable files
