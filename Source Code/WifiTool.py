#-------------------------------------------------------------------------------
# Name:  WifiTool
# Purpose: Create a GUI to create or stop wifi in laptop
#
# Author:      Wayne Wu
#
# Created:     08/03/2018
# Latest Modified: 24/03/2018
#-------------------------------------------------------------------------------
import os
import subprocess
import re
from urllib import request
import wx
import wx.adv
import time
import webbrowser

class WifiWin(wx.Frame):
    """
    WifiWin是定制的用来描述控制wifi窗口
    """
    def __init__(self, parent, id, title, size):
        """
        Args:
            parent: 该Frame的父控件
            id:Frame的id
            title:Frame的显示名称
            size:Frame的尺寸
        Returns:
            None
        Raises:
            None
        """
        super(WifiWin, self).__init__(parent, id, title, size=size)
        icon=wx.Icon('wifi.png', type=wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)
        self.SetMaxSize(size)
        self.SetMinSize(size)
        self.panel = wx.Panel(self, -1)
        self.panel.SetSizer(self.initPanel())
        self.CreateStatusBar()
        self.SetStatusText("网络状态: 未连接")


    def initPanel(self):
        """
        该函数用于部署Panel上的控件
        Args:
            None
        Returns:
            Sizer: 返回包含Panel上所有控件的Sizer对象
        Raises：
            None
        """
        labelName = wx.StaticText(self.panel, -1, label="  Wifi名称:  ")
        labelName.SetForegroundColour("SKY BLUE")
        self.textName  = wx.TextCtrl(self.panel, -1)
        self.textName.SetForegroundColour("CORAL")
        self.textName.Bind(wx.EVT_TEXT, self.onNameTextChange)
        boxSizer1 = wx.BoxSizer()
        boxSizer1.Add(labelName)
        boxSizer1.Add(self.textName, proportion=1, flag=wx.EXPAND)

        labelPasswd = wx.StaticText(self.panel, -1, label="  Wifi密码:  ")
        labelPasswd.SetForegroundColour("SKY BLUE")
        self.textPasswd  = wx.TextCtrl(self.panel, -1)
        self.textPasswd.SetForegroundColour("CORAL")
        self.textPasswd.Bind(wx.EVT_TEXT, self.onPasswordTextChange)
        boxSizer2 = wx.BoxSizer()
        boxSizer2.Add(labelPasswd)
        boxSizer2.Add(self.textPasswd, proportion=1, flag=wx.EXPAND)


        self.infoBox  = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)

        bmp = wx.Image("start.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        buttonStartWifi = wx.BitmapButton(self.panel, -1, bmp)
        buttonStartWifi.Bind(wx.EVT_BUTTON, self.onStartWifi)
        bmp = wx.Image("pause.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        buttonStopWifi = wx.BitmapButton(self.panel, -1, bmp)
        buttonStopWifi.Bind(wx.EVT_BUTTON, self.onStopWifi)
        boxSizer3 = wx.BoxSizer()
        boxSizer3.Add(buttonStartWifi)
        boxSizer3.Add(buttonStopWifi)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(boxSizer1, flag=wx.EXPAND)
        Sizer.Add(boxSizer2, flag=wx.EXPAND)
        Sizer.Add(self.infoBox, proportion=1, flag=wx.EXPAND)
        Sizer.Add(boxSizer3, flag=wx.ALIGN_RIGHT)

        return Sizer

    def __printCommandInfo(self):
        """
        该函数用于在TextCtrl控件中显示操作（启动或关闭Wifi）执行后返回的提示信息
        Args:
            None
        Returns:
            None
        Raises：
            None
        """
        with open("tmp.txt") as file:
            self.infoBox.AppendText(file.read().strip()+"\n")

    def __printWarningInfo(self, content):
        """
        该函数用于在TextCtrl控件中显示告警信息（显示红色）
        Args:
            None
        Returns:
            None
        Raises：
            None
        """
        self.infoBox.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.infoBox.AppendText(content)
        self.infoBox.SetDefaultStyle(wx.TextAttr(wx.BLACK))

    def __printSuccessInfo(self, content):
        """
        该函数用于在TextCtrl控件中显示成功信息（显示绿色）
        Args:
            None
        Returns:
            None
        Raises：
            None
        """
        self.infoBox.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.infoBox.AppendText(content)
        self.infoBox.SetDefaultStyle(wx.TextAttr(wx.BLACK))

    def onStartWifi(self, event):
        """
        该函数为StartWifi Button的Callback事件函数，用于启用Wifi热点
        Args:
            event:控件触发的事件类型
        Returns:
            None
        Raises：
            None
        """
        name=self.textName.GetValue()
        password = self.textPasswd.GetValue()
        content = ""
        self.infoBox.AppendText(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n")
        #检测Wifi名称或密码合法性
        if not name or not password:
            if not name:
                content = "Wifi名称为空！\n请输入Wifi名称！\n"
                self.textName.SetBackgroundColour("Yellow")
            if not password:
                content = content + "Wifi密码为空！\n 请输入Wifi密码！\n"
                self.textPasswd.SetBackgroundColour("Yellow")

            self.__printWarningInfo("Wifi 启动失败！\n\n")
            return wx.MessageBox(content, "错误", style=wx.OK|wx.ICON_ERROR)

        if(len(password) < 8):
            self.textPasswd.SetBackgroundColour("Yellow")
            self.__printWarningInfo("Wifi 启动失败！\n\n")
            self.SetStatusText("网络状态: 未连接")
            return wx.MessageBox("密码长度必须大于8位！", "错误", style=wx.OK|wx.ICON_ERROR)

        #执行Windows下批处理命令来允许开启无线网卡热点
        commad = "netsh wlan set hostednetwork mode=allow > tmp.txt"
        if(0 == os.system(commad)):
            self.__printCommandInfo()
        else:
            self.__printWarningInfo("Wifi 启动失败！\n\n")
            self.SetStatusText("网络状态: 未连接")
            return wx.MessageBox("承载网络模式设置失败！", "错误", style=wx.OK|wx.ICON_ERROR)

        #执行Windows下批处理命令来设置无线网卡热点的名称及密码
        commad = "netsh wlan set hostednetwork ssid=%s key=%s > tmp.txt" % (name, password)
        if(0 == os.system(commad)):
            self.__printCommandInfo()
        else:
            self.__printWarningInfo("Wifi 启动失败！\n\n")
            self.SetStatusText("网络状态: 未连接")
            return wx.MessageBox("设置承载网络SSID及用户密码秘钥失败！", "错误", style=wx.OK|wx.ICON_ERROR)

        #执行Windows下启用设置好的无线网卡热点
        commad = "netsh wlan start hostednetwork > tmp.txt"
        if(0 == os.system(commad)):
            self.__printCommandInfo()
            self.__printSuccessInfo("Wifi 启动成功！\n\n")
            self.SetStatusText("网络状态: 已连接")
            choice = wx.MessageBox("打开网络和共享中心，将本地网络共享给设置的无线Wifi。\n详细请参考网址:http://www.jb51.net/diannaojichu/78584.html，是否需要跳转到参考页面?", "注意",
                          style=wx.YES_NO|wx.ICON_INFORMATION)
            if(choice == wx.YES):
                webbrowser.open("http://www.jb51.net/diannaojichu/78584.html",new=1)
        else:
            self.__printWarningInfo("Wifi 启动失败！\n\n")
            self.SetStatusText("网络状态: 未连接")
            return wx.MessageBox("启动承载网络失败！\n\n", "错误", style=wx.OK|wx.ICON_ERROR)

    def onStopWifi(self, event):
        """
        该函数为StopWifi Button的Callback事件函数，用于停止Wifi热点
        Args:
            event:控件触发的事件类型
        Returns:
            None
        Raises：
            None
        """
        #执行Windows下停止设置好的无线网卡热点
        self.infoBox.AppendText(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n")
        commad = "netsh wlan stop hostednetwork > tmp.txt"
        if(0 == os.system(commad)):
            self.__printCommandInfo()
            self.__printWarningInfo("Wifi 已断开\n\n")
            self.SetStatusText("网络状态: 未连接")
        else:
            return wx.MessageBox("无法停止该Wifi热点！", "错误", style=wx.OK)

    def onNameTextChange(self, event):
        """
        该函数为Name TextCtrl的Callback事件函数，当内容不符合要求时TextCtrl背景将显示为黄色
        Args:
            event:控件触发的事件类型
        Returns:
            None
        Raises：
            None
        """
        if(self.textName.GetValue()):
            self.textName.SetBackgroundColour("White")
        else:
            self.textName.SetBackgroundColour("Yellow")

    def onPasswordTextChange(self, event):
        """
        该函数为Password TextCtrl的Callback事件函数，当内容不符合要求时TextCtrl背景将显示为黄色
        Args:
            event:控件触发的事件类型
        Returns:
            None
        Raises：
            None
        """
        if(len(self.textPasswd.GetValue()) >= 8):
            self.textPasswd.SetBackgroundColour("White")
        else:
            self.textPasswd.SetBackgroundColour("Yellow")
class WifiApp(wx.App):
    """
    WifiApp是定制的用来描述控制wifi App
    """
    def __init__(self):
        """
        该函数用于初始化App,在App上部署Frame
        Args:
            None
        Returns:
            None
        Raises：
            None
        """
        super(WifiApp, self).__init__()
        frame=WifiWin(None, -1, "热点工具", (400,500))
        frame.Show()
    def OnExit(self):
        """
        该函数在应用退出时将会关闭Wifi热点(当热点仍开启时)
        Args:
            None
        Returns:
            the status code of execute command "netsh wlan stop hostednetwork"
        Raises：
            None
        """
        return os.system("netsh wlan stop hostednetwork")


def main():
    app = WifiApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
