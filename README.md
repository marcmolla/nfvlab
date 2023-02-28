# NFV laboratory session 12 and 13
This repository contains the basic scripts and skeletons for the NFV laboratory seasson 12 and 13. 
## Installation
For installing the lab environment, please execute:
```bash
student@uk8s:~/nfvlab$ sudo ./bootsrap/bootstrap-nfvlab12-13.bash
```
After the installation, please check that your environment has the new groups:
```bash
student@uk8s:~/nfvlab$ newgrp snap_microk8s
student@uk8s:~/nfvlab$ newgrp lxd
```