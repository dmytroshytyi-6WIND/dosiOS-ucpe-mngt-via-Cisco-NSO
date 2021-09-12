# ucpe-ietf

# YANG data model for uCPE management https://datatracker.ietf.org/doc/draft-shytyi-opsawg-vysm/

Together modules represent this tree

```
module: ietf-network
  +--rw networks
     +--rw network* [network-id]                                        <<< networks
        +--rw network-id            network-id
        +--rw network-types
        |  +--rw tet:te-topology!
        |     +--rw tet-sf:sf!
        +--rw supporting-network* [network-ref]
        |  +--rw network-ref    -> /networks/network/network-id
        +--rw node* [node-id]                                            <<< nodes
           +--rw node-id                 node-id
           +--rw supporting-node* [network-ref node-ref]                 <<< allows us to assing VNF nodes to physical (uCPE) nodes
           |  +--rw network-ref    ->
           |  |         ../../../supporting-network/network-ref
           |  +--rw node-ref       -> /networks/network/node/node-id
           +--rw nt:termination-point* [tp-id]                           <<< node ports
           |  +--rw nt:tp-id                           tp-id
           |  +--rw nt:supporting-termination-point*
           |     |      [network-ref node-ref tp-ref]
           |     +--rw nt:network-ref
           |     |      -> ../../../nw:supporting-node/network-ref
           |     +--rw nt:node-ref
           |     |      -> ../../../nw:supporting-node/node-ref
           |     +--rw nt:tp-ref
           |            -> /nw:networks/network[nw:network-id=
           |            current()/../network-ref]/node
           |            [nw:node-id=current()/../node-ref]/
           |            termination-point/tp-id
           +--rw tet:te-node-id?         te-types:te-node-id
           +--rw tet:te!
           +--rw tet:te-node-template*
              |         -> ../../../../te/templates/
              |         node-template/name {template}?
              +--rw tet:te-node-attributes
                 |           
                 +--rw tet-sf:service-function                            
                    +--rw tet-sf:connectivity-matrices
                    |  +--rw tet-sf:connectivity-matrix* [id]                    <<< Interconnection between VNF-VNF,VNF-SW,etc...
                    |     +--rw tet-sf:id                 uint32                 
                    |     +--rw tet-sf:from                                      
                    |     |  +--rw tet-sf:service-function-id?    string         <<< VNF or Switch ID
                    |     |  +--rw tet-sf:sf-connection-point-id? string
                    |     +--rw tet-sf:to
                    |     |  +--rw tet-sf:service-function-id?    string         <<< VNF or Switch ID
                    |     |  +--rw tet-sf:sf-connection-point-id? string
                    |     +--rw tet-sf:enabled?           boolean
                    |     +--rw tet-sf:direction? connectivity-direction
                    |     +--rw tet-sf:virtual-link-id?   string
                    +--rw tet-sf:link-terminations
                       +--rw tet-sf:link-termination* [id]
                          +--rw tet-sf:id           uint32                        
                          +--rw tet-sf:from
                          |  +--rw tet-sf:tp-ref?   -> ../../../../
                          |     ../../../nt:termination-point/tp-id             <<< Phy port of equipment
                          +--rw tet-sf:to
                          |  +--rw tet-sf:service-function-id?    string        <<< VNF or Switch ID
                          |  +--rw tet-sf:sf-connection-point-id? string
                          +--rw tet-sf:enabled?   boolean
                          +--rw tet-sf:direction? connectivity-direction
ietf-network-instance                                                            <<< Switches          
  +--rw network-instances
     +--rw network-instance* [name]                                              <<< Switch ID
        +--rw name                 string
        +--rw enabled?             boolean
        +--rw description?         string
        +--rw (ni-type)?
        +--rw (root-type)
           +--:(vrf-root)
           |  +--rw vrf-root
           +--:(vsi-root)
           |  +--rw vsi-root
           |  +--rw ietf-ucpe-ni:network-instance-properties                     <<< Switch properties
           |     +--rw ietf-ucpe-ni:sf-connection-points*
           |     |  |              [sf-connection-point-id]
           |     |  +--rw ietf-ucpe-ni:sf-connection-point-id
           |     |  |              string
           |     |  +--rw ietf-ucpe-ni:dot1q-vlan
           |     |     +--rw ietf-ucpe-ni:access-tag?
           |     |     |           d1q:vid-range
           |     |     +--rw ietf-ucpe-ni:trunk-allowed-vlans?
           |     |     |           d1q:vid-range
           |     |     +--rw ietf-ucpe-ni:port-mode?
           |     |                 enumeration
           |     +--rw ietf-ucpe-ni:supporting-node?
           |        -> /nw:networks/network/node/node-id
           +--:(vv-root)
              +--rw vv-root
              
   logical-network-elements                                                      <<< VNFs
     +--rw logical-network-element* [name]
        +--rw name           string                                              <<< VNF ID
        +--rw managed?       boolean
        +--rw description?   string
        +--rw root
        +--rw logical-network-elements-properties                                <<< VNFs properties
               +--rw sf-connection-points* [sf-connection-point-id]
               |  +--rw sf-connection-point-id   string
               +--rw vnfd                                                        <<< ETSI SOL006 vnfd
               +--rw simplified-lne-props                                        <<< simple props
               |  +--rw ram?           uint64
               |  +--rw cpu?           uint64
               |  +--rw storages* [id]
               |     +--rw id          string
               |     +--rw location?   string
               +--rw day0-config                                                 <<< day0 config
                  +--rw location?        string
                  +--rw day0-var-path?   string
                  +--rw variable* [name]
                     +--rw name     string
                     +--rw value?   string

```



Where:


(IEEE) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ieee-dot1Q-types.yang 
   - dot1.q and QinQ support

https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-ucpe-node-type%402020-02-14.yang 
   - defines network node type

(RFC 8529) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-network-instance%402019-01-21.yang 
   - defines network instances (Switches) in the uCPE

https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-ucpe-ni-properties%402019-11-27.yang 
   - adds switch properties (supporting node, dot1.q/QinQ, area(WAN/LAN))

(RFC 8530) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-logical-network-element%402019-01-25.yang 
   - adds logical network elements (VNFs) in the uCPE

https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-ucpe-lne-properties%402019-11-21.yang 
   - VNF properties (supporting node, simple props(ram/cpu/disk) and ETSI SOL006 vnfd)

(RFC 8345) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-network%402018-02-26.yang 
   - defines the general networks and nodes

(RFC 8345) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-network-topology%402018-02-26.yang 
   - defines extensions of the networks - network topology

(rfc8795) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-te-topology%402019-02-07.yang 
   - TE (Traffic Engineering) network topology types as extention of network topologies

https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-te-topology-sf%402019-11-03.yang 
   - TE topology augmented with SF (VNFs) matrices for interconnection between VNFs, etc...

https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-ucpe-lt-virtual-link-id%402020-02-14.yang 
   - SF matrices extension: Virtual link id between equipment and service function 

(rfc8776) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/ietf-te-types%402019-11-18.yang 
   - grouping/typedefs/identities as support for ietf-te
   
(ETSI SOL006) https://github.com/dmytroshytyi/ucpe-ietf/blob/master/submodules/etsi-nfv-vnf-deviation.yang
   - Virtual Network Function descriptor for Logical Elements.
   
and others...



   The uCPE as harware with x86
   capabilities that is generally running Linux distibution with
   additinal virtualisation layer.  Virtualization layer provides
   virtual compute, virtual storage and virtual network resources.  Each
   VNF runnning in the uCPE requires the amount of virtual resources
   (for example: 4 vCPUs, 4GB RAM, 40GB storege, 4 vPorts).  VNFs MAY be
   interconnected between each other and physical ports via Virtual
   Networks.  Topology construction and VM lifecycle management is
   allowed via high level interface (Configuration can be done in the
   same transaction).  The figure below presents the uCPE architecture.

         ----------------------------------------|--------------
         VNF1            VNF2            VNF3    |
         ----------------------------------------|
         Virtual         Virtual         Virtual | uCPE software
         Compute         Storage         Networks|
         ----------------------------------------|---------------
         PHY x86         RAM+PHY         PHYsical| uCPE Hardware
         processor       storage         ports   |



 # uCPE purpose

   o  uCPE replaces multiple types of equipment (Node#1 - Node#5) with 1
      unit by virtualizing them as Virtual Network Functions on the top
      of NFVIs:
```
     :      NODE #1     :   NODE #2 :  NODE #3  :NODE #4: NODE #5  :
     :    +-----------+ :  +------+ :  +------+ :  +--+ :  +-----+ :
  ...-----|Aggregation|----|CE-L2 |----| CE-L3|----|FW|----|SDWAN|---LAN
     :    |  switch   | :  |      | :  |      | :  |  | :  |     | :
     :    +-----------+ :  +------+ :  +------+ :  +--+ :  +-----+ :
```

```
    :      NODE #1   :           NODE #2                           :
    :                : +.........................................+ :
    :  +-----------+ : |  +------+    +------+    +--+   +-----+ | :
 ...---|Aggregation|---|--|CE-L2 |----| CE-L3|----|FW|---|SDWAN|-|---LAN
    :  |  switch   | : |  |      |    |      |    |  |   |     | | :
    :  +-----------+ : |  +------+    +------+    +--+   +-----+ | :
    :                : |  universal Customer-Premises Equipment  | :
    :                : +-----------------------------------------+ :
```
   o  uCPE falicitates the interconnection between the Network Funtions
      (NF) as interconnection between NF is performed via virtual
      links(that is part of the uCPE management).  That meens that no
      need to hire technichian to cable the equipment, it could be done
      via orchestrator.

   o  uCPE falicitates the 0day configuration of the VNFs as its 0day
      configuration can be putted remotely.


# uCPE VNF ecosystem example

   uCPE supports a Virtual Network Funcitons of different type:

   o  SD-WAN

   o  vRouter

   o  vFirewall

   o  vLB(vLoad Balancer)

   o  vCGNAT(vCarrier Grade NAT)

   o  virtual WAN Optimistaion

   o  vWireless LAN controller

   o  Other...
   
# Internal uCPE service example

   The VNF in the uCPE could be a vRouter or vFirewall or an SD-WAN that
   is not a default part of virtual network resources of the uCPE.
   Multiple VNFs MAY be instantiated in the uCPE.  With support of links
   and swithes, VNFs MAY participate a service chains.  Example of
   service chains (Note that virtual switch "vs(WAN)" connected to LAN
   ports and vSW(WAN) is connected to WAN ports):

   o  vSW(WAN)-l1-vRouter-l2-vSW(LAN).

   o  vSW(WAN)-l1-vRouter-l2-vSW(Service)-l3-vFirewall-l4-vSW(LAN).

   o  vSW(WAN)-l1-vRouter-l2-vSW(Service1)-l3-vFirewall-l4-
      vSW(Service2)-l5-SD-WAN-l6-vSW(LAN).

   o  vSW(WAN)-l1-SDWAN-l2-vSW(Service)-l3-vFirewall-l4-vSW(LAN).

   o

         vSW(WAN1)--vRouter--+
                             +--vLoadBalance  vFirewall--vSW(LAN)
         vSW(WAN2)--vRouter--+     |              |
                                   +-vSW(Service1)+

   o

      vSW(WAN1)--vRouter(ISP1)--+
                                +--SD-WAN        vFirewall--vSW(LAN)
      vSW(WAN2)--vRouter(ISP2)--+     |              |
                                      +-vSW(Service1)+
