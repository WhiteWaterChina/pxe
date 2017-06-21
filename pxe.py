#!/usr/bin/env python2.7
# -*- coding:cp936 -*-
"""
author:yanshuo@inspur.com
1. ����dhcp��������windowsϵͳ��ftp��������
2. template_pxe��MAC��default)�ļ��Ĵ�ŵ�ַ��Ҫ���ո���pxe�������������ȷ����Ȼ���޸ģ�
"""
import wx
import re
import os
import subprocess
import paramiko


class PXEframe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"PXE BOOT", pos=wx.DefaultPosition, size=wx.Size(507, 397),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(0, 255, 0))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook1 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.panel_ks = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, -1), wx.TAB_TRAVERSAL)
        bSizer171 = wx.BoxSizer(wx.VERTICAL)

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"��������ѡ����Ҫ��װ��ϵͳ�İ汾��Ȼ�����Ҳ�\"ѡ��ϵͳ�汾\"��ť",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        self.m_staticText6.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText6.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer12.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer171.Add(bSizer12, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"ѡ��OS�İ汾", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer14.Add(self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        combo_os_versionChoices = [u"Redhat", u"CentOS", u"SUSE", u"Ubuntu"]
        self.combo_os_version = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"Redhat", wx.DefaultPosition, wx.DefaultSize,
                                            combo_os_versionChoices, wx.CB_DROPDOWN)
        self.combo_os_version.SetSelection(0)
        bSizer14.Add(self.combo_os_version, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_chose_os = wx.Button(self.panel_ks, wx.ID_ANY, u"ѡ��ϵͳ�汾", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.button_chose_os, 0, wx.ALL, 5)

        bSizer171.Add(bSizer14, 0, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"ѡ��OS��С�汾", wx.DefaultPosition, wx.DefaultSize, 0)
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

        self.m_staticText141 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"��ѡ��BIOS��ģʽ", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText141.Wrap(-1)
        bSizer27.Add(self.m_staticText141, 0, wx.ALL, 5)

        combox_bios_modeChoices = [u"UEFI", u"LEGACY"]
        self.combox_bios_mode = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"UEFI", wx.DefaultPosition, wx.Size(150, -1),
                                            combox_bios_modeChoices, 0)
        bSizer27.Add(self.combox_bios_mode, 0, wx.ALL, 5)

        bSizer171.Add(bSizer27, 0, wx.EXPAND, 5)

        bSizer28 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText131 = wx.StaticText(self.panel_ks, wx.ID_ANY, u"��ѡ��OS��λ��", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        self.m_staticText131.Wrap(-1)
        bSizer28.Add(self.m_staticText131, 0, wx.ALL, 5)

        combox_os_bitChoices = [u"64"]
        self.combox_os_bit = wx.ComboBox(self.panel_ks, wx.ID_ANY, u"64", wx.DefaultPosition, wx.Size(160, -1),
                                         combox_os_bitChoices, 0)
        bSizer28.Add(self.combox_os_bit, 0, wx.ALL, 5)

        bSizer171.Add(bSizer28, 0, wx.EXPAND, 5)

        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        bSizer241 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText14 = wx.StaticText(self.panel_ks, wx.ID_ANY,
                                            u"��������������ҪPXE��װ����ϵͳ�����ڵ�MAC��ַ����ʽΪ6c-92-bf-4c-77-90", wx.DefaultPosition,
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
                                             u"�����ҪPXE��������ѡ�񡰲���KS�ļ�����ť��PXE��������ָ��OS������Ч��\n�����Ҫȡ��������Ч�����ڿ�ʼ��װϵͳ��ѡ��ɾ��KS�ļ�����ť",
                                             wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_staticText121.Wrap(-1)
        self.m_staticText121.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText121.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer25.Add(self.m_staticText121, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer26 = wx.BoxSizer(wx.HORIZONTAL)

        self.button_generate_ks = wx.Button(self.panel_ks, wx.ID_ANY, u"����KS�ļ�", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer26.Add(self.button_generate_ks, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.butto_del_ks = wx.Button(self.panel_ks, wx.ID_ANY, u"ɾ��KS�ļ�", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer26.Add(self.butto_del_ks, 0, wx.ALL, 5)

        bSizer25.Add(bSizer26, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer241.Add(bSizer25, 1, wx.EXPAND, 5)

        bSizer24.Add(bSizer241, 0, wx.EXPAND, 5)

        bSizer171.Add(bSizer24, 0, wx.EXPAND, 5)

        self.panel_ks.SetSizer(bSizer171)
        self.panel_ks.Layout()
        self.m_notebook1.AddPage(self.panel_ks, u"����KS�ļ�", True)
        self.panel_pxe = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(self.panel_pxe, wx.ID_ANY,
                                           u"��������������ҪPXE�����Ļ�����BMC��IP��ַ���û��������룡\r\nȻ�����Ҳ��\"����PXE����\"��ť",
                                           wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText5.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer8.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer2.Add(bSizer8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC��IP��", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer10.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.textctrl_write_ip = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(200, -1), 0)
        bSizer10.Add(self.textctrl_write_ip, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer2.Add(bSizer10, 0, wx.EXPAND, 5)

        bSizer191 = wx.BoxSizer(wx.VERTICAL)

        bSizer21 = wx.BoxSizer(wx.VERTICAL)

        bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC���û�����", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText12.Wrap(-1)
        bSizer22.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.textctrl_bmc_username = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                 wx.Size(176, -1), 0)
        bSizer22.Add(self.textctrl_bmc_username, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer21.Add(bSizer22, 1, wx.EXPAND, 5)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText13 = wx.StaticText(self.panel_pxe, wx.ID_ANY, u"BMC�����룺", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText13.Wrap(-1)
        bSizer23.Add(self.m_staticText13, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.textctrl_bmc_password = wx.TextCtrl(self.panel_pxe, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1),
                                                 wx.Size(189, -1), wx.TE_PASSWORD)
        bSizer23.Add(self.textctrl_bmc_password, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_pxeBoot = wx.Button(self.panel_pxe, wx.ID_ANY, u"����PXE����", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.button_pxeBoot, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer21.Add(bSizer23, 1, wx.EXPAND, 5)

        bSizer191.Add(bSizer21, 1, wx.EXPAND, 5)

        bSizer2.Add(bSizer191, 0, wx.EXPAND, 5)

        self.panel_pxe.SetSizer(bSizer2)
        self.panel_pxe.Layout()
        bSizer2.Fit(self.panel_pxe)
        self.m_notebook1.AddPage(self.panel_pxe, u"����PXE����", False)
        self.panel_info = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText8 = wx.StaticText(self.panel_info, wx.ID_ANY, u"��������������MAC��ַ������Ӧ��IP��ַ", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
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

        self.m_staticText10 = wx.StaticText(self.panel_info, wx.ID_ANY, u"����Ҳఴť���鿴���е�IP��MAC��ַ�Ķ�Ӧ��ϵ",
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
        self.m_notebook1.AddPage(self.panel_info, u"��Ϣ��ѯ", False)

        bSizer3.Add(self.m_notebook1, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_chose_os.Bind(wx.EVT_BUTTON, self.chose_os)
        self.button_generate_ks.Bind(wx.EVT_BUTTON, self.download_ks)
        self.butto_del_ks.Bind(wx.EVT_BUTTON, self.delete_ks)
        self.button_pxeBoot.Bind(wx.EVT_BUTTON, self.setpxe)
        self.button_search.Bind(wx.EVT_BUTTON, self.searchip)
        self.button_viewall.Bind(wx.EVT_BUTTON, self.viewip)

#        pub.subscribe(self.update_ip, "update")
#        self._thread = Thread(target=self.get_all_ip, args=())
#        self._thread.daemon = True

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class

    def mac2ip(self):
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
        except paramiko.ssh_exception.SSHException:
            self.message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
        clientDic = {}
        try:
            with open(local_path, 'r') as file_dhcp:
                contents = file_dhcp.read()
                group = re.findall(r'lease [\w\W\s\S]+?}', contents)
                for each in group:
                    ipaddr = re.findall('lease (.*?) ', each)[0]
                    macaddr = re.findall('ethernet (.*?);', each)[0]
                    macaddr = re.sub(r':', '-', macaddr)
                    clientDic[ipaddr] = macaddr
        except IOError:
            self.message_error("DHCP��������Ϣ����ʧ�ܣ������������ӣ�".decode('gbk'))
        try:
            os.remove(local_path)
        except Exception:
            pass
        return clientDic

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

    def change_ks(self, filename):
        pass

    def download_ks(self, event):
        # download_ks_template
        os_version_temp = self.combo_os_version.GetValue().strip()
        os_version = os_version_temp.lower()
        os_sub_version = self.combox_os_sub_version.GetValue().strip()
        filename_to_gen_temp = self.textctrl_write_mac.GetValue().strip()
        bios_mode = self.combox_bios_mode.GetValue().strip()
        os_bit = self.combox_os_bit.GetValue().strip()
        filename_to_gen = "01-" + filename_to_gen_temp
        flag_ks_status = 1
        if len(os_version) == 0:
            self.message_error("����ϵͳ�汾δѡ��".decode('gbk'))
            flag_ks_status = 0
        else:
            if len(os_sub_version) == 0:
                self.message_error("����ϵͳС�汾δѡ��".decode('gbk'))
                flag_ks_status = 0
            else:
                if len(filename_to_gen_temp) == 0:
                    self.message_error("MAC��ַδ���룡������ˢ�룡".decode('gbk'))
                    flag_ks_status = 0
                else:
                    if len(bios_mode) == 0:
                        self.message_error("BIOSģʽδѡ����ѡ��".decode('gbk'))
                        flag_ks_status = 0
                    else:
                        if len(os_bit) == 0:
                            self.message_error("OS��λ��δѡ����ѡ��".decode('gbk'))
                            flag_ks_status = 0
                        else:
                            os_sub_version_max = os_sub_version.split(".")[0]
                            os_sub_version_min = os_sub_version.split(".")[1]
                            filename_ks_template = os_version + os_sub_version_max + "-" + os_sub_version_min + "_" + os_bit + ".cfg"
                            local_path_ks = os.path.join(os.getcwd(), filename_to_gen)
                            remote_path_dir = r'/tftpboot/ks_template/'
                            remote_path = os.path.join(remote_path_dir, filename_ks_template)
                            # try:
                            #     down_ks_template = paramiko.Transport('%s:22' % ipaddress_dhcp)
                            #     down_ks_template.connect(username=username_dhcp, password=password_dhcp)
                            #     sftp_down_ks = paramiko.SFTPClient.from_transport(down_ks_template)
                            #     try:
                            #         sftp_down_ks.get(localpath=local_path_ks, remotepath=remote_path)
                            #         sftp_down_ks.close()
                            #     except IOError:
                            #         self.message_error("δ��TFTP�������ҵ���Ӧ��OS��KSģ�壡�������������ϵ����Ա��飡".decode('gbk'))
                            #         flag_ks_status = 0
                            #     down_ks_template.close()
                            # except paramiko.ssh_exception.SSHException:
                            #     self.message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))
                            #     flag_ks_status = 0
                            #change ks
                            file_ks = open(local_path_ks, mode='w')
                            file_ks.write("timeout 1" + os.linesep)
                            file_ks.write("default %s%s-%s_%s" % (os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                            file_ks.write("label %s%s-%s_%s" % (os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                            file_ks.write("kernel images/%s/%s%s-%s_%s/vmlinuz" % (os_version, os_version,os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                            if os_version == "redhat" or os_version == "centos":
                                if os_sub_version_max == "7":
                                    file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img inst.ks=http://%s/ks/ks_template/%s/%s%s-%s_%s.cfg" % (os_version, os_version,os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, os_version, os_version,os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                                else:
                                    file_ks.write("append initrd=images/%s/%s%s-%s_%s/initrd.img ks=http://%s/ks/ks_template/%s/%s%s-%s_%s.cfg ksdevice=eth0" % (os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit, ipaddress_dhcp, os_version, os_version, os_sub_version_max, os_sub_version_min, os_bit) + os.linesep)
                            file_ks.close()
                            #upload ks file
                            if flag_ks_status == 1:
                                try:
                                    remote_path_ks = ''
                                    if bios_mode == "LEGACY":
                                        remote_path_ks = os.path.join(r'/tftpboot/pxelinux.cfg/', filename_to_gen)
                                    elif bios_mode == "UEFI":
                                        remote_path_ks = os.path.join(r'/tftpboot/efilinux/pxelinux.cfg/', filename_to_gen)
                                    upload_ks = paramiko.Transport('%s:22' % ipaddress_dhcp)
                                    upload_ks.connect(username=username_dhcp, password=password_dhcp)
                                    sftp_upload_ks = paramiko.SFTPClient.from_transport(upload_ks)
                                    sftp_upload_ks.put(localpath=local_path_ks, remotepath=remote_path_ks)
                                    sftp_upload_ks.close()
                                    upload_ks.close()
                                    os.remove(local_path_ks)
                                    self.message_ok("KS�ļ������ɹ���".decode('gbk'))
                                except paramiko.SSHException:
                                    self.message_error("�޷�������DHCP�������������������ӣ�".decode('gbk'))

    def delete_ks(self, event):
        filename_to_del_temp = self.textctrl_write_mac.GetValue().strip()
        bios_mode = self.combox_bios_mode.GetValue().strip()
        os_bit = self.combox_os_bit.GetValue().strip()
        os_sub_version = self.combox_os_sub_version.GetValue().strip()
        os_version_temp = self.combo_os_version.GetValue().strip()
        os_version = os_version_temp.lower()
        filename_to_del = "01-" + filename_to_del_temp
        if len(os_version) == 0:
            self.message_error("OS�İ汾δѡ����ѡ��".decode('gbk'))
        else:
            if len(os_sub_version) == 0:
                self.message_error("OSС�汾δѡ����ѡ��".decode('gbk'))
            else:
                if len(bios_mode) == 0:
                    self.message_error("BIOSģʽδѡ����ѡ��".decode('gbk'))
                else:
                    if len(os_bit) == 0:
                        self.message_error("OS��λ��δѡ����ѡ��".decode('gbk'))
                    else:
                        if len(filename_to_del_temp) == 0:
                            self.message_error("MAC��ַδ���룬�����룡".decode('gbk'))
                        else:
                            try:
                                ssh_del_ks = paramiko.SSHClient()
                                ssh_del_ks.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh_del_ks.connect(ipaddress_dhcp, 22, username=username_dhcp, password=password_dhcp)
                                if bios_mode == "UEFI":
                                    ssh_del_ks.exec_command(command='rm -rf /tftpboot/efilinux/pxelinux.cfg/%s' % filename_to_del)
                                elif bios_mode == "LEGACY":
                                    ssh_del_ks.exec_command(command='rm -rf /tftpboot/pxelinux.cfg/%s' % filename_to_del)
                                ssh_del_ks.close()
                                self.message_ok("KS�ļ��ӷ�����ɾ���ɹ���".decode('gbk'))
                            except paramiko.SSHException:
                                self.message_error("TFTP����������ʧ�ܣ������������ӣ�".decode('gbk'))

    def setpxe(self, event):
        bmcip = self.textctrl_write_ip.GetValue().strip()
        username_bmc = self.textctrl_bmc_username.GetValue().strip()
        password_bmc = self.textctrl_bmc_password.GetValue().strip()
        if len(bmcip) is not 0 and len(username_bmc) is not 0 and len(password_bmc) is not 0:
            set_pxe_boot = subprocess.Popen(["ipmitool.exe", "-I", "lanplus", "-H", "%s" % bmcip, "-U", "%s" % username_bmc, "-P", "%s" % password_bmc, "chassis", "bootdev", "pxe"], stdout=subprocess.PIPE)
            set_pxe_boot.communicate()
            if set_pxe_boot.returncode != 0:
                self.message_error('PXE��������ʧ�ܣ��������룡'.decode('gbk'))
            else:
                check_power_status = subprocess.Popen(["ipmitool.exe", "-I", "lanplus", "-H", "%s" % bmcip, "-U", "%s" % username_bmc, "-P", "%s" % password_bmc, "chassis", "power", "status"], stdout=subprocess.PIPE)
                check_power_status.communicate()
                power_status = check_power_status.stdout.read().split(" ")[3].strip()
                if check_power_status.returncode != 0:
                    self.message_error('���������ػ�״̬��ȡʧ�ܣ�����BMC���ã�'.decode('gbk'))
                else:
                    if power_status == 'off':
                        set_server_on = subprocess.Popen(["ipmitool.exe", "-I", "lanplus", "-H", "%s" % bmcip, "-U", "%s" % username_bmc, "-P", "%s" % password_bmc, "chassis", "power", "on"], stdout=subprocess.PIPE)
                        set_server_on.communicate()
                        if set_server_on.returncode != 0:
                            self.message_error('����������ʧ�ܣ�����BMC����״̬��'.decode('gbk'))
                        else:
                            self.message_ok('�����������ɹ���'.decode('gbk'))
                    elif power_status == 'on':
                        set_server_reset = subprocess.Popen(["ipmitool.exe", "-I", "lanplus", "-H", "%s" % bmcip, "-U", "%s" % username_bmc, "-P", "%s" % password_bmc, "chassis", "power", "reset"], stdout=subprocess.PIPE)
                        set_server_reset.communicate()
                        if set_server_reset.returncode != 0:
                            self.message_error('����������ʧ�ܣ�����BMC����״̬��'.decode('gbk'))
                        else:
                            self.message_ok('�����������ɹ���'.decode('gbk'))
                    else:
                        self.message_error('��ȡ��������ǰ״̬�쳣������BMC����״̬��'.decode('gbk'))
        else:
            self.message_error('PXE����ʧ�ܣ��������룡'.decode('gbk'))

    def searchip(self, event):
        self.textctrl_show_ipmac.Clear()
        key_ip = self.textctrl_ip_search.GetValue().strip()
        if len(key_ip) == 0:
            self.message_error("����հף�����������".decode('gbk'))
        else:
            ipdict = self.mac2ip()
            if ipdict.has_key(key_ip):
                content = key_ip + ":    " + ipdict[key_ip]
                self.textctrl_show_ipmac.SetValue(content)
            else:
                self.textctrl_show_ipmac.SetValue('No result match! Please check the input!')

    def viewip(self, event):
        self.button_viewall.Disable()
        self.textctrl_show_ipmac.Clear()
        ipdict = self.mac2ip()
        keys_ipmac = ipdict.keys()
        keys_ipmac.sort()
        ipstring = ''
        for item_key in keys_ipmac:
            ipstring = ipstring + item_key.ljust(30) + ipdict[item_key].ljust(30) + os.linesep
        self.textctrl_show_ipmac.SetValue(ipstring)
        self.button_viewall.Enable()

    def update_ip(self, msg):
        ipstring = msg.data
        self.textctrl_show_ipmac.AppendText(ipstring)

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
    ipaddress_dhcp = "100.2.36.2"
    username_dhcp = "root"
    password_dhcp = "lijianbo"
    app = wx.App()
    frame = PXEframe(None)
    frame.Show()
    app.MainLoop()