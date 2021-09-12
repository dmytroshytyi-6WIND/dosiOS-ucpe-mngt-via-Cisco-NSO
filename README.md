# dosiOS-ucpe-mngt-via-Cisco-NSO
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fdmytroshytyi%2FdosiOS-mngt-by-Cisco-NSO&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

Using ietf-ucpe models Cisco NSO manages the dosiOS ucpe.

This repository contains the NSO package to manage the ["dosiOS ucpe software"](https://github.com/dmytroshytyi/dosiOS-uCPE)

This package includes a set of yang modules provided by the next repository: ["ucpe-ietf"](https://github.com/dmytroshytyi/ucpe-ietf) and described by this IETF internet Draft: ["draft-shytyi-opsawg-vysm"](https://datatracker.ietf.org/doc/draft-shytyi-opsawg-vysm)

In the folder "config-examples" you may find an example of XML payload that may be submitted in the NSO to use the provided package.

You may load this example with "ncs\_load -l -m" command

Before the configuration commit you MUST create a device named "ucpe" under "devices device" part of the tree.

Before the configuration commit you MUST configure the WEB server with IP "10.0.0.200" and supply the WEB server with iso image named "vRouter.iso"

Before the configuration commit you MUST increase write/read time from NSO to device:

```
devices device ucpe
 write-timeout 1000
```

```
devices device ucpe
read-timeout 1000
```
