#!/usr/bin/env python2.7
# -*- coding:cp936 -*-
"""
author:yanshuo@inspur.com
"""
import wx
import re
import os
import subprocess
import paramiko
import time


class PXEframe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"PXE BOOT", pos=wx.DefaultPosition, size=wx.Size(507, 446),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(0, 255, 0))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook1 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.panel_ks = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, -1), wx.TAB_TRAVERSAL)
        bSizer171 = wx.BoxSizer(wx.VERTICAL)

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"请在如下选择需要安装的系统的版本，然后点击右侧\"选择系统版本\"按钮",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        self.m_staticText6.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText6.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer12.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer171.Add(bSizer12, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"选择OS的版本", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer14.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        combo_os_versionChoices = [u"Redhat", u"CentOS", u"SUSE", u"Ubuntu"]
        self.combo_os_version = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"Redhat", wx.DefaultPosition, wx.DefaultSize,
                                            combo_os_versionChoices, wx.CB_DROPDOWN)
        self.combo_os_version.SetSelection(0)
        bSizer14.Add(self.combo_os_version, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_chose_os = wx.Button(self.panel_ks, wx.ID_ANY, u"选择系统版本", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.button_chose_os, 0, wx.ALL, 5)

        bSizer171.Add(bSizer14, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"选择OS的小版本", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetBackgroundColour(wx.Colour(0, 255, 0))

        bSizer16.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        combox_os_sub_versionChoices = [wx.EmptyString]
        self.combox_os_sub_version = wx.ComboBox(self.panel_ks, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.Size(323, -1), combox_os_sub_versionChoices, 0)
        self.combox_os_sub_version.SetSelection(0)
        bSizer16.Add(self.combox_os_sub_version, 0, wx.ALL, 5)

        bSizer4.Add(bSizer16, 0, wx.EXPAND, 5)

        bSizer171.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer27 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText141 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"请选择BIOS的模式", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText141.Wrap(-1)
        bSizer27.Add(self.m_staticText141, 0, wx.ALL, 5)

        combox_bios_modeChoices = [u"UEFI", u"LEGACY"]
        self.combox_bios_mode = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"UEFI", wx.DefaultPosition, wx.Size(100, -1),
                                            combox_bios_modeChoices, 0)
        bSizer27.Add(self.combox_bios_mode, 0, wx.ALL, 5)

        self.m_staticText131 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"请选择OS的位数", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.m_staticText131.Wrap(-1)
        bSizer27.Add(self.m_staticText131, 0, wx.ALL, 5)

        combox_os_bitChoices = [u"64"]
        self.combox_os_bit = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"64", wx.DefaultPosition, wx.Size(100, -1),
                                         combox_os_bitChoices, 0)
        bSizer27.Add(self.combox_os_bit, 0, wx.ALL, 5)

        bSizer171.Add(bSizer27, 0, wx.EXPAND, 5)

        bSizer28 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText142 = wx.StaticText(self.panel_ks, wx.ID_ANY,
                                             u"请选择系统盘盘符，如果不清楚系统盘用哪个则此处不用选择，保持空白或者sda即可。\n默认优先使用sda，然后使用nvme0n1。",
                                             wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_staticText142.Wrap(-1)
        self.m_staticText142.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText142.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer28.Add(self.m_staticText142, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        combox_os_diskChoices = [u"sda", u"nvme0n1", u"sdb", u"sdc", u"sdd", u"sdf", u"sdg", u"sdh", u"sdi", u"sdj",
                                 u"sdk", u"sdl", u"sdm", u"sdn", u"sdo", u"sdp", u"sdq", u"sdr", u"sds", u"sdt", u"sdu",
                                 u"sdv", u"sdw", u"sdx", u"sdy", u"sdz", u"nvme1n1", u"nvme2n1", u"nvme3n1", u"nvme4n1",
                                 u"sde", wx.EmptyString]
        self.combox_os_disk = wx.ComboBox(self.panel_ks, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          combox_os_diskChoices, 0)
        self.combox_os_disk.SetSelection(0)
        bSizer28.Add(self.combox_os_disk, 0, wx.ALL | wx.EXPAND, 5)

        bSizer171.Add(bSizer28, 0, wx.EXPAND, 5)

        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        bSizer241 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText14 = wx.StaticText(self.panel_ks, wx.ID_ANY,
                                            u"请在如下输入需要PXE安装操作系统的网口的MAC地址，格式为6c-92-bf-4c-77-90", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        self.m_staticText14.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText14.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer241.Add(self.m_staticText14, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.textctrl_write_mac = wx.TextCtrl(self.panel_ks, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(-1, -1), 0)
        bSizer241.Add(self.textctrl_write_mac, 0, wx.ALL | wx.EXPAND, 5)

        bSizer25 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText121 = wx.StaticText(self.panel_ks, wx.ID_ANY,
                                             u"如果需要PXE启动，请选择“产生KS文件”按钮，PXE启动以上指定OS永久有效！\n如果需要取消永久有效，请在开始安装系统后选择“删除KS文件“按钮",
                                             wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_staticText121.Wrap(-1)
        self.m_staticText121.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText121.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer25.Add(self.m_staticText121, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer26 = wx.BoxSizer(wx.HORIZONTAL)

        self.button_generate_ks = wx.Button(self.panel_ks, wx.ID_ANY, u"产生KS文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer26.Add(self.button_generate_ks, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.butto_del_ks = wx.Button(self.panel_ks, wx.ID_ANY, u"删除KS文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer26.Add(self.butto_del_ks, 0, wx.ALL, 5)

        bSizer25.Add(bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer241.Add(bSizer25, 1, wx.EXPAND, 5)

        bSizer24.Add(bSizer241, 0, wx.EXPAND, 5)

        bSizer171.Add(bSizer24, 0, wx.EXPAND, 5)

        self.panel_ks.SetSizer(bSizer171)
        self.panel_ks.Layout()
        self.m_notebook1.AddPage(self.panel_ks, u"配置KS文件", True)
        self.panel_pxe = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(self.panel_pxe, wx.ID_ANY,
                                           u"请在如下输入需要PXE启动的机器的BMC的IP地址、用户名和密码！\r\n然后点击右侧的\"设置PXE启动\"按钮",
                                           wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText5.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer8.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer2.Add(bSizer8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC的IP：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer10.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.textctrl_write_ip = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(200, -1), 0)
        bSizer10.Add(self.textctrl_write_ip, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer2.Add(bSizer10, 0, wx.EXPAND, 5)

        bSizer191 = wx.BoxSizer(wx.VERTICAL)

        bSizer21 = wx.BoxSizer(wx.VERTICAL)

        bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC的用户名：", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText12.Wrap(-1)
        bSizer22.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.textctrl_bmc_username = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.Size(176, -1), 0)
        bSizer22.Add(self.textctrl_bmc_username, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer21.Add(bSizer22, 1, wx.EXPAND, 5)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText13 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC的密码：", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText13.Wrap(-1)
        bSizer23.Add(self.m_staticText13, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.textctrl_bmc_password = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1),
                                                 wx.Size(189, -1), wx.TE_PASSWORD)
        bSizer23.Add(self.textctrl_bmc_password, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_pxeBoot = wx.Button(self.panel_pxe, wx.ID_ANY, u"设置PXE启动", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.button_pxeBoot, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer21.Add(bSizer23, 1, wx.EXPAND, 5)

        bSizer191.Add(bSizer21, 1, wx.EXPAND, 5)

        bSizer2.Add(bSizer191, 0, wx.EXPAND, 5)

        self.panel_pxe.SetSizer(bSizer2)
        self.panel_pxe.Layout()
        bSizer2.Fit(self.panel_pxe)
        self.m_notebook1.AddPage(self.panel_pxe, u"设置PXE启动", False)
        self.panel_info = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText8 = wx.StaticText(self.panel_info, wx.ID_ANY,
                                           u"可以在如下输入IP或者MAC地址搜索对应的MAC或者地址。\nIP地址格式为1.1.1.1；MAC地址格式为6c-92-bf-4c-77-90",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        self.m_staticText8.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText8.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer17.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer5.Add(bSizer17, 0, wx.EXPAND, 5)

        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.textctrl_ip_search = wx.TextCtrl(self.panel_info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        bSizer20.Add(self.textctrl_ip_search, 1, wx.ALL, 5)

        self.button_search = wx.Button(self.panel_info, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.button_search, 0, wx.ALL, 5)

        bSizer5.Add(bSizer20, 0, wx.EXPAND, 5)

        bSizer18.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer19 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(self.panel_info, wx.ID_ANY, u"点击右侧按钮来查看所有的IP和MAC地址的对应关系",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        self.m_staticText10.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText10.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer19.Add(self.m_staticText10, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_viewall = wx.Button(self.panel_info, wx.ID_ANY, u"View All", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer19.Add(self.button_viewall, 0, wx.ALL, 5)

        bSizer18.Add(bSizer19, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.textctrl_show_ipmac = wx.TextCtrl(self.panel_info, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                               wx.DefaultSize, wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
        self.textctrl_show_ipmac.SetBackgroundColour(wx.Colour(255, 255, 255))

        bSizer6.Add(self.textctrl_show_ipmac, 1, wx.ALL | wx.EXPAND, 5)

        bSizer18.Add(bSizer6, 1, wx.EXPAND, 5)

        self.panel_info.SetSizer(bSizer18)
        self.panel_info.Layout()
        bSizer18.Fit(self.panel_info)
        self.m_notebook1.AddPage(self.panel_info, u"信息查询", False)

        bSizer3.Add(self.m_notebook1, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_chose_os.Bind(wx.EVT_BUTTON, self.chose_os)
        self.button_generate_ks.Bind(wx.EVT_BUTTON, self.generate_ks)
        self.butto_del_ks.Bind(wx.EVT_BUTTON, self.delete_ks)
        self.button_pxeBoot.Bind(wx.EVT_BUTTON, self.setpxe)
        self.button_search.Bind(wx.EVT_BUTTON, self.searchip)
        self.button_viewall.Bind(wx.EVT_BUTTON, self.viewip)

#        pub.subscribe(self.update_ip, "update")
#        self._thread = Thread(target=self.get_all_ip, args=())
#        self._thread.daemon = True

    def __del__(self):
        pass

    @staticmethod
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

    def mac2ip(self):
        clientDic_ip_mac = {}
        clientDic_mac_ip = {}
        if os.path.exists("dhcpd.leases"):
            os.remove("dhcpd.leases")
        remote_path = r'/var/lib/dhcpd/dhcpd.leases'
        local_path = os.path.join(os.getcwd(), r'dhcpd.leases')
        try:
            get_dhcp = paramiko.Transport('%s:22' % ipaddress_dhcp)
            get_dhcp.connect(username=username_dhcp, password=password_dhcp)
            sftp = paramiko.SFTPClient.from_transport(get_dhcp)
            sftp.get(localpath=local_path, remotepath=remote_path)
            sftp.close()
            get_dhcp.close()
            try:
                with open(local_path, 'r') as file_dhcp:
                    contents = file_dhcp.read()
                    group = re.findall(r'lease\s\d+.\d+.\d+.\d+\s.*?ethernet\s.+?;', contents, re.DOTALL)
                    for each in group:
                        ipaddr = re.findall('lease (\d+.\d+.\d+.\d+) ', each)[0]
                        macaddr = re.findall('ethernet (.+?);', each)[0]
                        macaddr = re.sub(r':', '-', macaddr)
                        clientDic_ip_mac[ipaddr] = macaddr
                        clientDic_mac_ip[macaddr] = ipaddr
            except IOError:
                self.message_error("DHCP服务器信息下载失败！请检查网络连接！".decode('gbk'))
        except paramiko.ssh_exception.SSHException:
            self.message_error("无法连接至DHCP服务器，请检查网络连接！".decode('gbk'))
        try:
            os.remove(local_path)
        except Exception:
            pass
        return clientDic_ip_mac, clientDic_mac_ip

    def chose_os(self, event):
        os_version = self.combo_os_version.GetValue()
        if os_version == 'Redhat':
            relist = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0', '7.1', '7.2', '7.3']
        elif os_version == 'CentOS':
            relist = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0', '7.1', '7.2', '7.3']
        elif os_version == 'SUSE':
            relist = ['11.1', '11.2', '11.3', '12.0', '12.1', '12.2']
        elif os_version == 'Ubuntu':
            relist = ['12.04', '14.04', '16.04']
        else:
            relist = ['Not Supported']
        self.combox_os_sub_version.Set(relist)

    def generate_ks(self, event):
        os_version_temp = self.combo_os_version.GetValue().strip()
        os_version = os_version_temp.lower()
        os_sub_version = self.combox_os_sub_version.GetValue().strip()
        mac_net_pxe = self.textctrl_write_mac.GetValue().strip().lower()
        bios_mode_temp = self.combox_bios_mode.GetValue().strip()
        bios_mode = bios_mode_temp.lower()
        os_bit = self.combox_os_bit.GetValue().strip()
        os_disk_temp = self.combox_os_disk.GetValue().strip()
        os_disk = os_disk_temp.lower()
        flag_ks_status = 1
        if len(os_version) == 0:
            self.message_error("操作系统版本未选择".decode('gbk'))
            flag_ks_status = 0
        else:
            if len(os_sub_version) == 0:
                self.message_error("操作系统小版本未选择".decode('gbk'))
                flag_ks_status = 0
            else:
                if len(mac_net_pxe) == 0:
                    self.message_error("MAC地址未输入！请重新刷入！".decode('gbk'))
                    flag_ks_status = 0
                else:
                    if len(bios_mode) == 0:
                        self.message_error("BIOS模式未选择！请选择！".decode('gbk'))
                        flag_ks_status = 0
                    else:
                        if len(os_bit) == 0:
                            self.message_error("OS的位数未选择！请选择！".decode('gbk'))
                        else:
                            flag_ks_local_exists = 0
                            filename_menu_to_gen = "01-" + mac_net_pxe
                            os_sub_version_max = os_sub_version.split(".")[0]
                            os_sub_version_min = os_sub_version.split(".")[1]

                            filename_ks_template = "%s%s-%s_%s.cfg" % (os_version, os_sub_version_max, os_sub_version_min, os_bit)
                            remote_path_dir_ks_template = r'/var/www/html/ks/ks_template/%s/%s/' % (os_version, bios_mode)
                            remote_path_ks_template = os.path.join(remote_path_dir_ks_template, filename_ks_template)

                            filename_ks_local = "%s.cfg" % (mac_net_pxe)
                            local_path_ks = os.path.join(os.getcwd(), filename_ks_local)
                            remote_path_ks = r'/var/www/html/ks/ks_all/'

                            local_path_menu = os.path.join(os.getcwd(), filename_menu_to_gen)
                            local_path_pre = os.path.join(os.getcwd(), "pre.txt")
                            filename_remote_pre = "auto-partition-%s.sh" % bios_mode

                            #download ks_template & pre
                            try:
                                down_ks_template = paramiko.Transport('%s:22' % ipaddress_dhcp)
                                down_ks_template.connect(username=username_dhcp, password=password_dhcp)
                                sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
                                try:
                                    #download_ks_template
                                    sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path_ks_template)
                                    if os_version == "redhat" or os_version == "centos":
                                        remote_dir_pre = r"/var/www/html/ks/auto_partition/redhat/"
                                        remote_path_pre = os.path.join(remote_dir_pre, filename_remote_pre)
                                        sftp_down_ks.get(localpath=local_path_pre, remotepath=remote_path_pre)
                                    sftp_down_ks.close()
                                    flag_ks_local_exists = 1
                                except IOError:
                                    self.message_error("未从TFTP服务器找到对应的OS的KS模板！请检查输入或者联系管理员检查！".decode('gbk'))
                                    flag_ks_status = 0
                                down_ks_template.close()
                            except paramiko.ssh_exception.SSHException:
                                self.message_error("无法连接至DHCP服务器，请检查网络连接！".decode('gbk'))

                            #change ks
                            if flag_ks_local_exists == 0:
                                self.message_error("没有成功下载KS文件到本地！".decode('gbk'))
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
                                # for item_data_pre in data_pre:
                                #     handler_ks.write(item_data_pre + "\n")
                                handler_ks.write("%end")
                                handler_pre.close()
                                handler_ks.close()

                            #generate menu
                            file_ks = open(local_path_menu, mode='w')
                            if os_version == "redhat" or os_version == "centos":
                                file_ks.write("timeout 1" + os.linesep)
                                file_ks.write("default %s%s-%s_%s" % (os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                                file_ks.write("label %s%s-%s_%s" % (os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                                if bios_mode == "legacy":
                                    file_ks.write("kernel images/%s/%s%s-%s_%s/vmlinuz" % (os_version, os_version,os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                                elif bios_mode == "uefi":
                                    file_ks.write("kernel ../images/%s/%s%s-%s_%s/vmlinuz" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)

                                if os_sub_version_max == "7":
                                    if os_sub_version_min == "3":
                                        if bios_mode == "legacy":
                                            file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img modprobe.blacklist=qat_c62x inst.ks=http://%s/ks/ks_all/%s.cfg" % (os_version, os_version,os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                                        elif bios_mode =="uefi":
                                            file_ks.write("append initrd=../images/%s/%s%s-%s_%s/initrd.img modprobe.blacklist=qat_c62x inst.ks=http://%s/ks/ks_all/%s.cfg" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                                    else:
                                        if bios_mode == "legacy":
                                            file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img modprobe.blacklist=qat_c62x inst.ks=http://%s/ks/ks_all/%s.cfg" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                                        elif bios_mode == "uefi":
                                            file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img modprobe.blacklist=qat_c62x inst.ks=http://%s/ks/ks_all/%s.cfg" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                                elif os_sub_version_max == "6":
                                    if bios_mode == "legacy":
                                        file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img ks=http://%s/ks/ks_all/%s.cfg ksdevice=eth0" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                                    elif bios_mode == "uefi":
                                        file_ks.write("append initrd=../images/%s/%s%s-%s_%s/initrd.img ks=http://%s/ks/ks_all/%s.cfg ksdevice=eth0" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, mac_net_pxe) + os.linesep)
                            else:
                                pass
                            file_ks.close()

                            #upload menu file & ks
                            if flag_ks_status == 1:
                                try:
                                    remote_path_menu = ''
                                    if bios_mode == "legacy":
                                        remote_path_menu = os.path.join(r'/tftpboot/pxelinux.cfg/', filename_menu_to_gen)
                                    elif bios_mode == "uefi":
                                        remote_path_menu = os.path.join(r'/tftpboot/efilinux/pxelinux.cfg/', filename_menu_to_gen)
                                    upload_menu = paramiko.Transport('%s:22' % ipaddress_dhcp)
                                    upload_menu.connect(username=username_dhcp, password=password_dhcp)
                                    sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_menu)
                                    #upload_menu
                                    sftp_upload_ks.put(localpath=local_path_menu, remotepath=remote_path_menu)
                                    #uplaod_ks
                                    sftp_upload_ks.put(localpath=local_path_ks, remotepath=os.path.join(remote_path_ks, filename_ks_local))
                                    sftp_upload_ks.close()
                                    upload_menu.close()
                                    os.remove(local_path_ks)
                                    os.remove(local_path_pre)
                                    os.remove(local_path_menu)
                                    self.message_ok("KS文件产生成功！".decode('gbk'))
                                except paramiko.SSHException:
                                    self.message_error("无法连接至DHCP服务器，请检查网络连接！".decode('gbk'))

    def delete_ks(self, event):
        bios_mode = self.combox_bios_mode.GetValue().strip()
        os_bit = self.combox_os_bit.GetValue().strip()
        os_sub_version = self.combox_os_sub_version.GetValue().strip()
        os_version_temp = self.combo_os_version.GetValue().strip()
        os_version = os_version_temp.lower()
        mac_net_pxe = self.textctrl_write_mac.GetValue().strip().lower()
        filename_menu_to_del = "01-" + mac_net_pxe
        if len(bios_mode) == 0:
            self.message_error("BIOS模式未选择，请选择！".decode('gbk'))
        else:
            if len(mac_net_pxe) == 0:
                self.message_error("MAC地址未输入，请输入！".decode('gbk'))
            else:
                filename_ks = "%s.cfg" % mac_net_pxe
                try:
                    ssh_del_ks = paramiko.SSHClient()
                    ssh_del_ks.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_del_ks.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                    if bios_mode == "UEFI":
                        ssh_del_ks.exec_command(command='rm -rf /tftpboot/efilinux/pxelinux.cfg/%s' % filename_menu_to_del)
                    elif bios_mode == "LEGACY":
                        ssh_del_ks.exec_command(command='rm -rf /tftpboot/pxelinux.cfg/%s' % filename_menu_to_del)
                    ssh_del_ks.exec_command(command='rm -rf /var/www/html/ks/ks_all/%s' % filename_ks)
                    ssh_del_ks.close()
                    self.message_ok("KS文件从服务器删除成功！".decode('gbk'))
                except paramiko.SSHException:
                    self.message_error("TFTP服务器连接失败！请检查网络连接！".decode('gbk'))

    def setpxe(self, event):
        bmcip = self.textctrl_write_ip.GetValue().strip()
        username_bmc = self.textctrl_bmc_username.GetValue().strip()
        password_bmc = self.textctrl_bmc_password.GetValue().strip()
        if len(bmcip) is not 0 and len(username_bmc) is not 0 and len(password_bmc) is not 0:
            set_pxe_boot, output_1  = self.run_command("ipmitool.exe -I lanplus -H %s -U %s -P %s chassis bootdev pxe" % (bmcip, username_bmc, password_bmc))
            if set_pxe_boot != 0:
                self.message_error('PXE启动设置失败！请检查输入！'.decode('gbk'))
            else:
                check_power_status, output_power_status = self.run_command("ipmitool.exe -I lanplus -H %s -U %s -P %s chassis power status" % (bmcip, username_bmc, password_bmc))
                if check_power_status != 0:
                    self.message_error('服务器开关机状态获取失败！请检查BMC设置！'.decode('gbk'))
                else:
                    power_status = output_power_status.split(" ")[3].strip()
                    if power_status == 'off':
                        set_server_on, output_3 = self.run_command("ipmitool.exe -I lanplus -H %s -U %s -P %s chassis power on" % (bmcip, username_bmc, password_bmc))
                        if set_server_on != 0:
                            self.message_error('服务器开机失败！请检查BMC连接状态！'.decode('gbk'))
                        else:
                            self.message_ok('服务器开机成功！'.decode('gbk'))
                    elif power_status == 'on':
                        set_server_reset, output_2 = self.run_command("ipmitool.exe -I lanplus -H %s -U %s -P %s chassis power reset" % (bmcip, username_bmc, password_bmc))
                        if set_server_reset != 0:
                            self.message_error('服务器重启失败！请检查BMC连接状态！'.decode('gbk'))
                        else:
                            self.message_ok('服务器重启成功！'.decode('gbk'))
                    else:
                        self.message_error('获取服务器当前状态异常！请检查BMC连接状态！'.decode('gbk'))
        else:
            self.message_error('输入缺失！请检查输入！'.decode('gbk'))

    def searchip(self, event):
        self.textctrl_show_ipmac.Clear()
        key_ip_mac = self.textctrl_ip_search.GetValue().strip()
        if len(key_ip_mac) == 0:
            self.message_error("输入空白！请重新输入".decode('gbk'))
        else:
            ipdict_ip_mac, ipdict_mac_ip = self.mac2ip()
            if ipdict_ip_mac.has_key(key_ip_mac):
                content = key_ip_mac + "  :  " + ipdict_ip_mac[key_ip_mac]
                self.textctrl_show_ipmac.SetValue(content)
            else:
                if ipdict_mac_ip.has_key(key_ip_mac):
                    content = ipdict_mac_ip[key_ip_mac] + ":    " + key_ip_mac
                    self.textctrl_show_ipmac.SetValue(content)
                else:
                    self.textctrl_show_ipmac.SetValue('No result match! Please check the input!')

    def viewip(self, event):
        self.button_viewall.Disable()
        self.textctrl_show_ipmac.Clear()
        ipdict, output_nothing = self.mac2ip()
        keys_ipmac = ipdict.keys()
        keys_ipmac.sort()
        ipstring = ''
        for item_key in keys_ipmac:
            ipstring = ipstring + item_key.ljust(30) + ipdict[item_key].ljust(30) + os.linesep
        self.textctrl_show_ipmac.SetValue(ipstring)
        self.button_viewall.Enable()

    @staticmethod
    def message_ok(message):
        dlg = wx.MessageDialog(None, message, "INFO BOX",  wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()

    @staticmethod
    def message_error(message):
        dlg = wx.MessageDialog(None, message, "ERROR BOX", wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()


if __name__ == '__main__':
    ipaddress_dhcp = "100.2.36.153"
    username_dhcp = "root"
    password_dhcp = "111111"
    app = wx.App()
    frame = PXEframe(None)
    frame.Show()
    app.MainLoop()
