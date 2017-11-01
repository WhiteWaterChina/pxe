#!/usr/bin/env python2.7
# -*- coding:cp936 -*-
"""
author:yanshuo@inspur.com
"""

import re
import os
import subprocess
import paramiko
import time
import sys

'''
���������
1.����KS�ļ�(gen)��ɾ��KS�ļ�(del)������PXE������boottopxe)��gen��Ҫ�����߸�����(BIOS MODE/MAC ADDR/OS VERSION/OS SUB VERSION/OS BITS/ OS DISK)��del��Ҫ����������BIOS MODE��MAC ADDR����PXE������Ҫ�ĸ�������BIOS MODE/BMCIP/BMC USERNAME/BMC PASSWORD)
2.BIOSģʽ��legacy����uefi��
3.MAC��ַ����ʽΪ6C-92-BF-11-22-33)
4.OS�汾.��redhat/centos/ubuntu/windows/suse
5.OSС�汾��redhat��centos����Ϊ6.4��7.2��suse����Ϊ11.2-12.2��ubuntu����Ϊ14.04.5,16.10��17.04��windows����Ϊ'2016-datacenter-cn', '2016-datacenter-en', '2016-standard-en', '2016-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn'
6.OSλ����64��
7.ϵͳ���̷�,��sda/nvme0n1/sdb/sdc/sdd/sde/sdf/sdg��������ѡһ��
8.BMC IP��ַ
9.BMC�û���
10.BMC�û�����

'''


def run_command(command, timeout=2):
    cmd = command.split(" ")
    child_run = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    begin_time = time.time()
    deadline = begin_time + timeout
    while True:
        Flag = child_run.poll()
        if Flag is not None:
            break
        if timeout and time.time() > deadline:
            child_run.kill()
            break
        time.sleep(0.5)
    return child_run.returncode, child_run.stdout.read()

def generate_menu_redhat(os_version_sub, os_sub_version_max_sub, os_sub_version_min_sub, os_bit_sub, bios_mode_sub, ipaddress_dhcp_sub, mac_net_pxe_sub, mac_boot_device_rhel6_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        if os_sub_version_max_sub == "7":
            string_to_write.append(
                "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img initrd=initrd.imgmodprobe.blacklist=qat_c62x inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        elif os_sub_version_max_sub == "6":
            string_to_write.append(
                "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz initrd=initrd.img ramdisk_size=8192 ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append("initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd.img".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append("menuentry '{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}' --class os ".format(os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub, os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + '{' + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append("set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        if os_sub_version_max_sub == "7":
            string_to_write.append(
                "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz modprobe.blacklist=qat_c62x inst.ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        elif os_sub_version_max_sub == "6":
            string_to_write.append("linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/vmlinuz ks=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg ksdevice={mac_boot_device_rhel6}".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                    mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append("initrd (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd.img".format(
                    os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                    os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    return string_to_write

def generate_menu_suse(os_version_sub, os_sub_version_max_sub, os_sub_version_min_sub, os_bit_sub, bios_mode_sub, ipaddress_dhcp_sub, mac_net_pxe_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append(
            "kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/linux initrd=initrd splash=silent showopts edd=off  install=http://100.2.36.3/iso/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit} autoyast=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.xml".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,ipaddress_dhcp=ipaddress_dhcp_sub, os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub, os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,  mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append("menuentry '{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}' --class os ".format(os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub, os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + "{" + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append("set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        string_to_write.append(
            "linux (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/linux splash=silent showopts install=http://{ipaddress_dhcp}/iso/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit} autoyast=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.xml".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub,
                mac_net_pxe=mac_net_pxe_sub) + os.linesep)
        string_to_write.append(
            "initrd (http)/images-uefi/{os_version}/{os_version}{os_sub_version_max}-{os_sub_version_min}_{os_bit}/initrd".format(
                os_version=os_version_sub, os_sub_version_max=os_sub_version_max_sub,
                os_sub_version_min=os_sub_version_min_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    return string_to_write

def generate_menu_ubuntu(os_version_sub, os_string_version_sub, os_bit_sub, bios_mode_sub, ipaddress_dhcp_sub, mac_net_pxe_sub, mac_boot_device_rhel6_sub):
    string_to_write = []
    if bios_mode_sub == "legacy":
        string_to_write.append("#!ipxe" + os.linesep)
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append("kernel http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/linux initrd=initrd.gz devfs-nomount ramdisksize=16384 vga=normal url=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg netcfg/get_nameservers={ipaddress_dhcp} ks=http://{ipaddress_dhcp}/ks/ks_template/{os_version}/{bios_mode}/{os_version}{os_string_version}_{os_bit}-{bios_mode}.cfg ksdevice={mac_boot_device_rhel6}".format(
            os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub, mac_net_pxe=mac_net_pxe_sub, mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_dhcp}/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/initrd.gz ".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub, ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot")
    elif bios_mode_sub == "uefi":
        string_to_write.append("set timeout=1" + os.linesep)
        string_to_write.append("menuentry '{os_version}{os_string_version}_{os_bit}' --class os ".format(os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub) + "{" + os.linesep)
        string_to_write.append("insmod net" + os.linesep)
        string_to_write.append("insmod efinet" + os.linesep)
        string_to_write.append("insmod tftp" + os.linesep)
        string_to_write.append("insmod gzio" + os.linesep)
        string_to_write.append("insmod part_gpt" + os.linesep)
        string_to_write.append("insmod efi_gop" + os.linesep)
        string_to_write.append("insmod efi_uga" + os.linesep)
        string_to_write.append("set net_default_server={ipaddress_dhcp}".format(ipaddress_dhcp=ipaddress_dhcp_sub) + os.linesep)
        string_to_write.append("net_add_addr eno0 efinet0 100.2.36.4" + os.linesep)
        string_to_write.append("net_add_addr eno1 efinet1 100.2.36.5" + os.linesep)
        string_to_write.append("net_add_addr eno2 efinet2 100.2.36.6" + os.linesep)
        string_to_write.append("net_add_addr eno3 efinet3 100.2.36.7" + os.linesep)
        string_to_write.append("net_add_addr eno4 efinet4 100.2.36.8" + os.linesep)
        string_to_write.append("net_add_addr eno5 efinet5 100.2.36.9" + os.linesep)
        string_to_write.append("net_add_addr eno6 efinet6 100.2.36.11" + os.linesep)
        string_to_write.append("net_add_addr eno7 efinet7 100.2.36.12" + os.linesep)
        string_to_write.append("net_add_addr eno8 efinet8 100.2.36.13" + os.linesep)
        string_to_write.append("net_add_addr eno9 efinet9 100.2.36.14" + os.linesep)
        string_to_write.append("net_add_addr eno10 efinet10 100.2.36.15" + os.linesep)
        string_to_write.append("net_add_addr eno11 efinet11 100.2.36.16" + os.linesep)
        string_to_write.append("net_add_addr eno12 efinet12 100.2.36.17" + os.linesep)
        string_to_write.append("net_add_addr eno13 efinet13 100.2.36.18" + os.linesep)
        string_to_write.append("net_add_addr eno14 efinet14 100.2.36.19" + os.linesep)
        string_to_write.append(
            "linux (http)/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/linux devfs-nomount ramdisksize=16384 vga=normal url=http://{ipaddress_dhcp}/ks/ks_all/{mac_net_pxe}.cfg netcfg/get_nameservers={ipaddress_dhcp} ks=http://{ipaddress_dhcp}/ks/ks_template/{os_version}/{bios_mode}/{os_version}{os_string_version}_{os_bit}-{bios_mode}.cfg ksdevice={mac_boot_device_rhel6}".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_dhcp=ipaddress_dhcp_sub, bios_mode=bios_mode_sub, mac_net_pxe=mac_net_pxe_sub,
                mac_boot_device_rhel6=mac_boot_device_rhel6_sub) + os.linesep)
        string_to_write.append(
            "initrd (http)/images-uefi/{os_version}/{os_version}{os_string_version}_{os_bit}/initrd.gz".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub) + os.linesep)
        string_to_write.append("boot")
        string_to_write.append("}")
    return string_to_write

def generate_menu_windows(os_version_sub, os_string_version_sub, os_bit_sub, bios_mode_sub, ipaddress_windows_sub):
    string_to_write = []
    string_to_write.append("#!ipxe" + os.linesep)
    string_to_write.append("set timeout=1" + os.linesep)
    string_to_write.append("kernel tftp://{ipaddress_dhcp_temp}/wimboot".format(ipaddress_dhcp_temp=ipaddress_dhcp) + os.linesep)
    if bios_mode_sub == "legacy":
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/bcd BCD".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/bootmgr bootmgr".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/boot.sdi boot.sdi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/sources/boot.wim boot.wim".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot" + os.linesep)
    elif bios_mode_sub == "uefi":
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/EFI/Boot/bootx64.efi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/EFI/Microsoft/Boot/BCD".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/boot/boot.sdi".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append(
            "initrd http://{ipaddress_windows}:8080/auto-windows/{os_version}/{os_version}{os_string_version}_{os_bit}/sources/boot.wim".format(
                os_version=os_version_sub, os_string_version=os_string_version_sub, os_bit=os_bit_sub,
                ipaddress_windows=ipaddress_windows_sub, bios_mode=bios_mode_sub) + os.linesep)
        string_to_write.append("boot" + os.linesep)
    return string_to_write

def generate_ks_redhat_centos(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk):
    flag_ks_status = 1
    flag_ks_local_exists = 0
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_sub_version_max = os_sub_version.split(".")[0]
    os_sub_version_min = os_sub_version.split(".")[1]
    os_string_version = "-".join(os_sub_version.split("."))
    filename_ks_template = "%s%s_%s-%s.cfg" % (os_version, os_string_version, os_bit, bios_mode)
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/%s/%s/' % (os_version, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_rhel = "%s.cfg" % (mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_rhel)
    remote_path_ks = r'/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)
    local_path_pre = os.path.join(os.getcwd(), "pre.txt")
    filename_remote_pre = "auto-partition-%s.sh" % bios_mode

    # download ks_template & rhel_pre
    try:
        down_ks_template = paramiko.Transport('%s:22' % ipaddress_dhcp)
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            # download_pre
            remote_dir_pre = r"/var/www/html/ks/auto_partition/redhat/"
            remote_path_pre = os.path.join(remote_dir_pre, filename_remote_pre)
            sftp_down_ks.get(localpath=local_path_pre, remotepath=remote_path_pre)
            sftp_down_ks.close()
            flag_ks_local_exists = 1
        except IOError:
            #message_error("δ��TFTP�������ҵ���Ӧ��OS��KSģ�壡�������������ϵ����Ա��飡".decode('gbk'))
            flag_ks_status = 0
            os._exit(255)
        down_ks_template.close()
    except paramiko.ssh_exception.SSHException:
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)
        # change ks with pre
    if flag_ks_local_exists == 0:
        #message_error("û�гɹ�����KS�ļ������أ�".decode('gbk'))
        os._exit(255)
    else:
        if len(os_disk) != 0:
            handler_ks_change = open(local_path_pre, mode='rb')
            pattern_os_disk = re.compile(r'firstdisk=sda')
            string_pre = ''
            for item_data_pre in handler_ks_change:
                if re.search(pattern_os_disk, item_data_pre):
                    item_data_pre = re.sub(pattern_os_disk, "firstdisk=%s" % os_disk, item_data_pre)
                    string_pre += item_data_pre
                else:
                    string_pre += item_data_pre
            handler_ks_change.close()
            handler_ks_change = open(local_path_pre, mode='wb')
            handler_ks_change.write(string_pre)
            handler_ks_change.close()
            handler_ks = open(local_path_ks, mode='ab+')
            handler_pre = open(local_path_pre, mode='rb')
            data_pre = handler_pre.readlines()
            handler_ks.write("%pre --interpreter=/bin/bash\n")
            handler_ks.writelines(data_pre)
            handler_ks.write("%end")
            handler_pre.close()
            handler_ks.close()
        else:
            pass

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_redhat(os_version, os_sub_version_max, os_sub_version_min, os_bit, bios_mode, ipaddress_dhcp, mac_net_pxe, mac_boot_device_rhel6)
        file_menu.writelines(data_menu)

    # upload menu file & ks
    flag_upload_ks_menu = 1
    try:
        remote_path_menu = ''
        if bios_mode == "legacy":
            remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/', mac_boot_device_rhel6 + ".cfg")
        elif bios_mode == "uefi":
            remote_path_menu = os.path.join(r'/opt/config/', mac_boot_device_rhel6 + ".cfg")
        upload_menu = paramiko.Transport('%s:22' % ipaddress_dhcp)
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        # upload_menu
        sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
        # upload_ks
        sftp_upload_ks.put(localpath=local_path_ks, remotepath=os.path.join(remote_path_ks, filename_ks_local_rhel))
        sftp_upload_ks.close()
        upload_menu.close()
        os.remove(local_path_ks)
        os.remove(local_path_menu)
        os.remove(local_path_pre)

        # generate uefi menu for remote server
        if bios_mode == "uefi" :
            try:
                ssh_gen_uefi_menu = paramiko.SSHClient()
                ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                ssh_gen_uefi_menu.exec_command(command='cp /opt/config/grub-generate.sh /opt/config/%s.sh' % mac_boot_device_rhel6)
                ssh_gen_uefi_menu.exec_command(command='/opt/config/{mac}.sh {mac}'.format(mac=mac_boot_device_rhel6))
                ssh_gen_uefi_menu.close()
            except paramiko.SSHException:
                flag_upload_ks_menu = 0
                #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
                os._exit(255)
    except paramiko.ssh_exception.SSHException:
        flag_upload_ks_menu = 0
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)
    if flag_upload_ks_menu == 1:
        #message_ok("KS�ļ������ɹ���".decode('gbk'))
        os._exit(255)

def generate_ks_suse(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit):
    flag_ks_status = 1
    flag_ks_local_exists = 0
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_sub_version_max = os_sub_version.split(".")[0]
    os_sub_version_min = os_sub_version.split(".")[1]
    os_string_version = "-".join(os_sub_version.split("."))
    filename_ks_template = "%s%s_%s-%s.xml" % (os_version, os_string_version, os_bit, bios_mode)
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/%s/%s/' % (os_version, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_suse = "%s.xml" % (mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_suse)
    remote_path_ks = r'/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)
    # download ks_template
    try:
        down_ks_template = paramiko.Transport('%s:22' % ipaddress_dhcp)
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            sftp_down_ks.close()
        except IOError:
            #message_error("δ��TFTP�������ҵ���Ӧ��OS��KSģ�壡�������������ϵ����Ա��飡".decode('gbk'))
            flag_ks_status = 0
            os._exit(255)
        down_ks_template.close()
    except paramiko.ssh_exception.SSHException:
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)


    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_suse(os_version, os_sub_version_max, os_sub_version_min, os_bit, bios_mode, ipaddress_dhcp, mac_net_pxe)
        file_menu.writelines(data_menu)

    # upload menu file & ks
    flag_upload_ks_menu = 1
    try:
        remote_path_menu = ''
        if bios_mode == "legacy":
            remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/',
                                            mac_boot_device_rhel6 + ".cfg")
        elif bios_mode == "uefi":
            remote_path_menu = os.path.join(r'/opt/config/',
                                            mac_boot_device_rhel6 + ".cfg")
        upload_menu = paramiko.Transport('%s:22' % ipaddress_dhcp)
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
        # upload_menu
        sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
        # upload_ks
        sftp_upload_ks.put(localpath=local_path_ks,
                           remotepath=os.path.join(remote_path_ks,
                                                   filename_ks_local_suse))
        sftp_upload_ks.close()
        upload_menu.close()
        os.remove(local_path_ks)
        os.remove(local_path_menu)

        # generate uefi menu for remote server
        if bios_mode == "uefi":
            try:
                ssh_gen_uefi_menu = paramiko.SSHClient()
                ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp,
                                          password=password_dhcp)
                ssh_gen_uefi_menu.exec_command(
                    command='cp /opt/config/grub-generate.sh /opt/config/%s.sh' % mac_boot_device_rhel6)
                ssh_gen_uefi_menu.exec_command(
                    command='/opt/config/{mac}.sh {mac}'.format(
                        mac=mac_boot_device_rhel6))
                ssh_gen_uefi_menu.close()
            except paramiko.SSHException:
                flag_upload_ks_menu = 0
                #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
                os._exit(255)
    except paramiko.ssh_exception.SSHException:
        flag_upload_ks_menu = 0
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)
    if flag_upload_ks_menu == 1:
        #message_ok("KS�ļ������ɹ���".decode('gbk'))
        os._exit(255)

def generate_ks_ubuntu(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk):
    flag_ks_status = 1
    flag_ks_local_exists = 0
    mac_net_pxe = mac_net_pxe_temp.upper()
    filename_menu_to_gen = mac_net_pxe + "-menu.cfg"
    os_string_version = "-".join(os_sub_version.split("."))
    filename_ks_template = "preseed-%s%s_%s-%s.cfg" % (os_version, os_string_version, os_bit, bios_mode)
    remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/%s/%s/' % (os_version, bios_mode)
    remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)
    filename_ks_local_rhel = "%s.cfg" % (mac_net_pxe)
    local_path_ks = os.path.join(os.getcwd(), filename_ks_local_rhel)
    remote_path_ks = r'/var/www/html/ks/ks_all/'
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)

    # download ks_template & rhel_pre
    try:
        down_ks_template = paramiko.Transport('%s:22' % ipaddress_dhcp)
        down_ks_template.connect(username=username_dhcp, password=password_dhcp)
        sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
        try:
            # download_ks
            sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
            sftp_down_ks.close()
            flag_ks_local_exists = 1
        except IOError:
            #message_error("δ��TFTP�������ҵ���Ӧ��OS��KSģ�壡�������������ϵ����Ա��飡".decode('gbk'))
            flag_ks_status = 0
            os._exit(255)
        down_ks_template.close()
    except paramiko.ssh_exception.SSHException:
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)

        # change ks with pre
    if flag_ks_local_exists == 0:
        #message_error("û�гɹ�����KS�ļ������أ�".decode('gbk'))
        os._exit(255)
    else:
        if len(os_disk) != 0:
            handler_ks_change = open(local_path_ks, mode='rb')
            pattern_os_disk = re.compile(r'/dev/sda')
            string_pre = ''
            for item_data_pre in handler_ks_change:
                if re.search(pattern_os_disk, item_data_pre):
                    item_data_pre = re.sub(pattern_os_disk, "/dev/%s" % os_disk, item_data_pre)
                    string_pre += item_data_pre
                else:
                    string_pre += item_data_pre
            handler_ks_change.close()
            handler_ks_change = open(local_path_ks, mode='wb')
            handler_ks_change.write(string_pre)
            handler_ks_change.close()
        else:
            pass

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_ubuntu(os_version, os_string_version, os_bit, bios_mode, ipaddress_dhcp, mac_net_pxe, mac_boot_device_rhel6)
        file_menu.writelines(data_menu)

    # upload menu file & ks
    if flag_ks_status == 1:
        flag_upload_ks_menu = 1
        try:
            remote_path_menu = ''
            if bios_mode == "legacy":
                remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/', mac_boot_device_rhel6 + ".cfg")
            elif bios_mode == "uefi":
                remote_path_menu = os.path.join(r'/opt/config/', mac_boot_device_rhel6 + ".cfg")
            upload_menu = paramiko.Transport('%s:22' % ipaddress_dhcp)
            upload_menu.connect(username=username_dhcp, password=password_dhcp)
            sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
            # upload_menu
            sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
            # upload_ks
            sftp_upload_ks.put(localpath=local_path_ks, remotepath=os.path.join(remote_path_ks, filename_ks_local_rhel))
            sftp_upload_ks.close()
            upload_menu.close()
            os.remove(local_path_ks)
            os.remove(local_path_menu)

            # generate uefi menu for remote server
            if bios_mode == "uefi":
                try:
                    ssh_gen_uefi_menu = paramiko.SSHClient()
                    ssh_gen_uefi_menu.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_gen_uefi_menu.connect(ipaddress_dhcp, 22, username=username_dhcp,
                                              password=password_dhcp)
                    ssh_gen_uefi_menu.exec_command(
                        command='cp /opt/config/grub-generate.sh /opt/config/%s.sh' % mac_boot_device_rhel6)
                    ssh_gen_uefi_menu.exec_command(
                        command='/opt/config/{mac}.sh {mac}'.format(
                            mac=mac_boot_device_rhel6))
                    ssh_gen_uefi_menu.close()
                except paramiko.SSHException:
                    flag_upload_ks_menu = 0
                    #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
                    os._exit(255)
        except paramiko.ssh_exception.SSHException:
            flag_upload_ks_menu = 0
            #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
            os._exit(255)
        if flag_upload_ks_menu == 1:
            #message_ok("KS�ļ������ɹ���".decode('gbk'))
            os._exit(255)

def generate_ks_windows(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit):
    filename_menu_to_gen = mac_net_pxe_temp + "-menu.cfg"
    local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)

    # generate_menu
    with open(local_path_menu, mode='wb') as file_menu:
        data_menu = generate_menu_windows(os_version, os_sub_version, os_bit, bios_mode, ipaddress_windows)
        file_menu.writelines(data_menu)

    # upload menu file & ks
    flag_upload_ks_menu = 1
    try:
        remote_path_menu = ''
        if bios_mode == "legacy":
            remote_path_menu = os.path.join(r'/var/www/html/ipxe-legacy.cfg/',
                                            mac_boot_device_rhel6 + ".cfg")
        elif bios_mode == "uefi":
            remote_path_menu = os.path.join(r'/var/www/html/ipxe-uefi.cfg/',
                                            mac_boot_device_rhel6 + ".efi")
        upload_menu = paramiko.Transport('%s:22' % ipaddress_dhcp)
        upload_menu.connect(username=username_dhcp, password=password_dhcp)
        sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)

        # upload_menu
        sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
        sftp_upload_ks.close()
        upload_menu.close()
        os.remove(local_path_menu)
    except paramiko.ssh_exception.SSHException:
        flag_upload_ks_menu = 0
        #message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        os._exit(255)
    if flag_upload_ks_menu == 1:
        #message_ok("KS�ļ������ɹ���".decode('gbk'))
        os._exit(255)

def generate_ks():
    os_version = os_verison_temp.lower()
    # os_sub_version = combox_os_sub_version.GetValue().strip()
    mac_boot_device_rhel6 = re.sub(r'-', ':', mac_net_pxe_temp.lower())
    bios_mode = bios_mode_temp.lower()
    # os_bit = combox_os_bit.GetValue().strip()
    # os_disk_temp = combox_os_disk.GetValue().strip()
    os_disk = os_disk_temp.lower()

    if len(os_version) == 0:
        #message_error("����ϵͳ�汾δѡ��".decode('gbk'))
        flag_ks_status = 0
        os._exit(255)
    else:
        if len(os_sub_version) == 0:
            # message_error("����ϵͳС�汾δѡ��".decode('gbk'))
            flag_ks_status = 0
            os._exit(255)
        else:
            if len(mac_net_pxe_temp) == 0:
                #message_error("MAC��ַδ���룡������ˢ�룡".decode('gbk'))
                flag_ks_status = 0
                os._exit(255)
            else:
                if len(bios_mode) == 0:
                    #message_error("BIOSģʽδѡ����ѡ��".decode('gbk'))
                    flag_ks_status = 0
                    os._exit(255)
                else:
                    if len(os_bit) == 0:
                        #message_error("OS��λ��δѡ����ѡ��".decode('gbk'))
                        flag_ks_status = 0
                        os._exit(255)
                    else:
                        if os_version == "redhat" or os_version == "centos":
                            generate_ks_redhat_centos(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk)
                        elif os_version == "suse":
                            generate_ks_suse(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit)
                        elif os_version == "ubuntu":
                            generate_ks_ubuntu(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit, os_disk)
                        elif os_version == "windows":
                            generate_ks_windows(os_version, os_sub_version, mac_net_pxe_temp, mac_boot_device_rhel6, bios_mode, os_bit)
                        else:
                            pass

def delete_ks():
    bios_mode = bios_mode_temp.lower()
    mac_net_pxe = mac_net_pxe_temp.upper()
    mac_boot_device_rhel6 = re.sub(r'-', ':', mac_net_pxe_temp.lower())
    if len(bios_mode) == 0:
        #message_error("BIOSģʽδѡ����ѡ��".decode('gbk'))
        os._exit(255)
    else:
        if len(mac_net_pxe_temp) == 0:
            #message_error("MAC��ַδ���룬�����룡".decode('gbk'))
            os._exit(255)
        else:
            filename_ks = "%s.*" % mac_net_pxe
            try:
                ssh_del_ks = paramiko.SSHClient()
                ssh_del_ks.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_del_ks.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                if bios_mode == "uefi":
                    ssh_del_ks.exec_command(command='rm -rf /var/www/html/ipxe-uefi.cfg/%s.efi' % mac_boot_device_rhel6 )
                    ssh_del_ks.exec_command(command='rm -rf /opt/config/%s.sh' % mac_boot_device_rhel6)
                elif bios_mode == "legacy":
                    ssh_del_ks.exec_command(command='rm -rf /var/www/html/ipxe-legacy.cfg/%s' % mac_boot_device_rhel6 + ".cfg")
                # if os_version != "windows":
                ssh_del_ks.exec_command(command='rm -rf /var/www/html/ks/ks_all/%s' % filename_ks)
                ssh_del_ks.close()
                #message_ok("KS�ļ��ӷ�����ɾ���ɹ���".decode('gbk'))
            except paramiko.SSHException:
                os._exit(255)
                # message_error("TFTP����������ʧ�ܣ������������ӣ�".decode('gbk'))

def setpxe(bios_mode_sub, bmc_ip_sub, bmc_username_sub, bmc_password_sub):
    set_pxe_boot = ""
    bios_mode = bios_mode_temp.lower()
    # if len(bmc_ip_sub) is not 0 and len(bmc_username_sub) is not 0 and len(bmc_password_sub) is not 0:
    if bios_mode_sub == "legacy":
        set_pxe_boot, output_1  = run_command("ipmitool -I lanplus -H %s -U %s -P %s chassis bootdev pxe" % (bmc_ip_sub, bmc_username_sub, bmc_password_sub))
    elif bios_mode == "uefi":
        set_pxe_boot, output_1 = run_command("ipmitool -I lanplus -H %s -U %s -P %s raw 0x00 0x08 0x05 0xa0 0x04 0x00 0x00 0x00" % (bmc_ip_sub, bmc_username_sub, bmc_password_sub))
    if set_pxe_boot != 0:
        #self.message_error('PXE��������ʧ�ܣ��������룡'.decode('gbk'))
        os._exit(255)
    else:
        check_power_status, output_power_status = run_command("ipmitool -I lanplus -H %s -U %s -P %s chassis power status" % (bmc_ip_sub, bmc_username_sub, bmc_password_sub))
        if check_power_status != 0:
            #self.message_error('���������ػ�״̬��ȡʧ�ܣ�����BMC���ã�'.decode('gbk'))
            os._exit(255)
        else:
            power_status = output_power_status.split(" ")[3].strip()
            if power_status == 'off':
                set_server_on, output_3 = run_command("ipmitool -I lanplus -H %s -U %s -P %s chassis power on" % (bmc_ip_sub, bmc_username_sub, bmc_password_sub))
                if set_server_on != 0:
                    #self.message_error('����������ʧ�ܣ�����BMC����״̬��'.decode('gbk'))
                    os._exit(255)
                else:
                    #self.message_ok('�����������ɹ���'.decode('gbk'))
                    print "power on sucessfully!"
            elif power_status == 'on':
                set_server_reset, output_2 = run_command("ipmitool -I lanplus -H %s -U %s -P %s chassis power reset" % (bmc_ip_sub, bmc_username_sub, bmc_password_sub))
                if set_server_reset != 0:
                    #self.message_error('����������ʧ�ܣ�����BMC����״̬��'.decode('gbk'))
                    os._exit(255)
                else:
                    #self.message_ok('�����������ɹ���'.decode('gbk'))
                    print "power reset sucessfully!"
            else:
                #self.message_error('��ȡ��������ǰ״̬�쳣������BMC����״̬��'.decode('gbk'))
                os._exit(255)
#else:
#    self.message_error('����ȱʧ���������룡'.decode('gbk'))

ipaddress_dhcp = "100.2.36.2"
ipaddress_windows = '100.2.38.14'
username_dhcp = "root"
password_dhcp = "Testing"


if len(sys.argv) == 0:
    print "����Ϊ0".decode('gbk')
    os._exit(255)
else:
    gen_or_del_ks = sys.argv[1]
    if gen_or_del_ks == "gen":
        if len(sys.argv) != 8:
            print "gen���벻��7".decode('gbk')
            os._exit(255)
        else:
            bios_mode_temp = sys.argv[2]
            mac_net_pxe_temp = sys.argv[3]
            os_verison_temp = sys.argv[4]
            os_sub_version = sys.argv[5]
            os_bit = sys.argv[6]
            os_disk_temp = sys.argv[7]
            generate_ks()
    elif gen_or_del_ks == "del":
        if len(sys.argv) != 4:
            print "del���벻��3".decode('gbk')
            os._exit(255)
        else:
            bios_mode_temp = sys.argv[2]
            mac_net_pxe_temp = sys.argv[3]
            delete_ks()
    elif gen_or_del_ks == "boottopxe":
        if len(sys.argv) != 6:
            print "del���벻��5".decode('gbk')
            os._exit(255)
        else:
            bios_mode_temp = sys.argv[2]
            bmc_ip = sys.argv[3]
            bmc_username = sys.argv[4]
            bmc_password = sys.argv[5]
            setpxe(bios_mode_temp, bmc_ip, bmc_username, bmc_password)
    else:
        print "����1��Ϊgen����del����boottopxe".decode('gbk')
        os._exit(255)
