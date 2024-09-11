A peer-to-peer file transfer application, comprising one manager and multiple peers.

1. Manager
(i) A manager is an always-ON server, which maintains the list of currently active peers across the network at all times [1 mark].
(ii) A newly arrived peer connects to the manager
[1 mark] The manager adds this newly arrived peer to its list of active peers, and, 
      b)   [1 mark] broadcasts the updated list.
(iii) The manager periodically:
[1 mark] checks availability of active peers from its list, 
[1 mark] updates the same, if some peer(s) leave(s) the network, and,
[1 mark] broadcasts the updated list.
(iv) A peer informs the manager when it leaves the network
[1 mark] The manager deletes this peer from its list of active peers, and,
[1 mark] broadcasts the updated list.

2. Peer
(i) A new peer is expected to know the manager’s IP and port. It pings the manager [1 mark], and saves the list of active peers sent by the manager [1 mark]. 
(ii) It also maintains a list of shareable files [1 mark].
(iii) Before going offline, a peer informs the manager [1 mark].

(iv)To fetching a file from other peer(s), a peer:
[1 mark] broadcasts its requirement to all peers (from its list of active peers)
[2 marks] based on received responses, parallely fetches different fragments of the required file from available peers
[2 marks] if any of the transmitting peers go offline, the requesting peer fetches its missing fragments from the remaining available peers

(v) On being requested to share a file by another peer, a peer:
[1 mark] informs the requesting peer of its availability
[1 mark] transmits the requested fragment(s) of one of its shareable files
