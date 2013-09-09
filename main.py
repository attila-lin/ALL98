# -*- coding: utf-8 -*-
import wx
import sys
import cc98lib
import os

reload(sys)
sys.setdefaultencoding('utf-8')

#--------- 全局变量
getface = "face1.gif"           # 发帖小表情
getcontent = "test"                 # 发帖内容
#--------- 全局变量



class AboutFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "About", wx.DefaultPosition, wx.Size(325, 320))

        panel = wx.Panel(self, -1)

        text1 = "Now listen to me mama\nMama mama\nYou're taking away my last chance\nDon't take it away"

        text2 = '''You won't cry for my absence, I know -
You forgot me long ago.
Am I that unimportant...?
Am I so insignificant...?
Isn't something missing?
Isn't someone missing me?'''

        text3 = '''But if I had one wish fulfilled tonight
I'd ask for the sun to never rise
If God passed a mic to me to speak
I'd say stay in bed, world
Sleep in peace'''

        font1 = wx.Font(10, wx.NORMAL, wx.ITALIC, wx.NORMAL)
        font2 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        font3 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD)
        lyrics1 = wx.StaticText(panel, -1, text1,(30,15), style=wx.ALIGN_CENTRE)
        lyrics1.SetFont(font1)
        lyrics2 = wx.StaticText(panel, -1, text2,(30,100), style=wx.ALIGN_CENTRE)
        lyrics2.SetFont(font2)
        lyrics3 = wx.StaticText(panel, -1, text3,(5,220), style=wx.ALIGN_CENTRE)
        lyrics3.SetFont(font3)
        self.Center()


class AddUserFrame(wx.Frame):
    '''
    添加用户窗口
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Add User', size=(300, 150))

        self.panel = wx.Panel(self)

        self.namelabel = wx.StaticText(self.panel, -1, "name:", (70, 20))
        self.nametext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 20))  
        self.passlabel = wx.StaticText(self.panel, -1, "password:",(70, 50))
        self.passtext = wx.TextCtrl(self.panel, 1, style=wx.TE_PASSWORD, pos=(140, 50))  

        self.addbutton = wx.Button(self.panel, label = "add", pos = (80, 100), size = (50, 30))
        self.canbutton = wx.Button(self.panel, label = "cancel", pos = (170, 100), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.Confirm, self.addbutton)
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.canbutton)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def Confirm(self, event):
        '''
        确认添加
        '''
        name = self.nametext.GetValue()
        password = self.passtext.GetValue()
        
        if name == "":
            noname = wx.MessageDialog(None, "No name", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = noname.ShowModal()
            noname.Destroy()
        elif password == "":
            nopassword = wx.MessageDialog(None, "No password", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nopassword.ShowModal()
            nopassword.Destroy()
        else:
            #更新帐号和密码
            frame.sampleList.append(name.decode('utf-8'))
            frame.accout[name] = password

            file = open("./accout","a")
            file.write(name + " " + password + "\n")
            file.close()

            frame.listBox.Append(name)
            self.Close(True)

    def Cancel(self, event):
        self.Close(True)
    def OnCloseWindow(self, event):
        self.Destroy()

class EditUserFrame(wx.Frame):
    '''
    编辑用户窗口，默认填写用户名
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Edit User', size=(300, 150))

        self.panel = wx.Panel(self)

        self.namelabel = wx.StaticText(self.panel, -1, "name:", (70, 20))
        self.nametext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 20)) 

        self.checked =  frame.listBox.GetCheckedStrings()
        self.nametext.SetValue(self.checked[0])

        self.passlabel = wx.StaticText(self.panel, -1, "password:",(70, 50))
        self.passtext = wx.TextCtrl(self.panel, 1, style=wx.TE_PASSWORD, pos=(140, 50))  

        self.okbutton = wx.Button(self.panel, label = "confirm", pos = (60, 100), size = (50, 30))
        self.delbutton = wx.Button(self.panel, label = "delete", pos = (115, 100), size = (50, 30))
        self.canbutton = wx.Button(self.panel, label = "cancel", pos = (170, 100), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.Confirm, self.okbutton)
        self.Bind(wx.EVT_BUTTON, self.Delete, self.delbutton)
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.canbutton)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def Confirm(self, event):
        '''
        确认修改
        '''
        # 原来的用户名
        oldname = self.checked[0]
        newname = self.nametext.GetValue()
        password = self.passtext.GetValue()
        

        if password == "":
            nopassword = wx.MessageDialog(None, "No password", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nopassword.ShowModal()
            nopassword.Destroy()
        else:
            #删除原来的帐号 添加新的帐号
            del frame.accout[oldname.encode('utf-8')]
            frame.accout[newname.encode('utf-8')] = password

            # print frame.accout
            
            #删除用户列表的名字 然后在原来位置放置新帐号
            frame.sampleList.remove(oldname.decode('utf-8'))
            frame.sampleList.append(newname.decode('utf-8'))
            
            #选择项的位置
            pos = frame.listBox.GetSelection()
            frame.listBox.Delete(pos)
            frame.listBox.Insert(newname, pos)

            self.Close(True)

    def Delete(self, event):
        '''
        删除该用户
        '''
        #选择的帐号
        oldname = self.checked[0]

        #删除该帐号
        del frame.accout[oldname.encode('utf-8')]
        # print frame.accout

        #删除用户列表的名字
        frame.sampleList.remove(oldname.decode('utf-8'))
        
        #选择项的位置
        pos = frame.listBox.GetSelection()
        frame.listBox.Delete(pos)

        self.Close(True)

    def Cancel(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


class VisitorFrame(wx.Frame):
    '''
    访客功能界面：主要用于设置 开始页 终止页 版块号 帖子id
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '统计访客', size=(300, 220))

        self.panel = wx.Panel(self)

        self.beginlabel = wx.StaticText(self.panel, -1, "Begin:", (70, 20))
        self.begintext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 20))  
        self.endlabel = wx.StaticText(self.panel, -1, "End:",(70, 50))
        self.endtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 50))  

        self.boardidlabel = wx.StaticText(self.panel, -1, "boardid:", (70, 80))
        self.boardidtext = wx.TextCtrl(self.panel, 1, style=wx.TE_LEFT,pos=(140,80))
        self.idlabel = wx.StaticText(self.panel, -1, "id:",(70, 110))
        self.idtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140,110))

        self.gauge = wx.Gauge(self.panel, -1, 50, size=(150, 25), pos = (70,140) )

        self.begbutton = wx.Button(self.panel, label = "开始", pos = (80, 170), size = (50, 30))
        self.canbutton = wx.Button(self.panel, label = "取消", pos = (170, 170), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.Confirm, self.begbutton)
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.canbutton)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def Confirm(self, event):
        '''
        确认开始
        '''
        checkedlists =  frame.listBox.GetCheckedStrings()
        checked = checkedlists[0].encode("utf-8")
        password = frame.accout[checked]

        BoardID = int(self.boardidtext.GetValue())
        ID = int(self.idtext.GetValue())
        begin = int(self.begintext.GetValue())
        end = int(self.endtext.GetValue())

        url = cc98lib.geturl(BoardID,ID)
        headers = cc98lib.login(checked, password)

        self.visitors = cc98lib.fangke(headers, url, begin, end, self.gauge)
        # print visitors

        # 显示结果
        visres = VisitorResultFrame(parent = None, id = -1)
        visres.Show()
        self.Close()

    def Cancel(self, event):
        self.Close(True)
    def OnCloseWindow(self, event):
        self.Destroy()


class VisitorResultFrame(wx.Frame):
    """
    访客结果界面：用于显示统计访客的结果
    """
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '统计访客结果', size=(300, 700))

        self.panel = wx.Panel(self)
        #-- sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_MULTILINE)

        # print frame.visitor.visitors
        for item in frame.visitor.visitors:
            self.text.AppendText(item[0] + " : " + item[1] + '\n')

        self.sizer.Add(self.text, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)

        #-- 设置sizer
        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


class TongJiFrame(wx.Frame):
    '''
    统计水楼帖数界面：相同与访客界面，主要用于设置 开始页 终止页 版块号 帖子id
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '水楼统计', size=(300, 220))

        self.panel = wx.Panel(self)

        self.beginlabel = wx.StaticText(self.panel, -1, "Begin:", (70, 20))
        self.begintext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 20))  
        self.endlabel = wx.StaticText(self.panel, -1, "End:",(70, 50))
        self.endtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 50))  

        self.boardidlabel = wx.StaticText(self.panel, -1, "boardid:", (70, 80))
        self.boardidtext = wx.TextCtrl(self.panel, 1, style=wx.TE_LEFT,pos=(140,80))
        self.idlabel = wx.StaticText(self.panel, -1, "id:",(70, 110))
        self.idtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140,110))

        self.gauge = wx.Gauge(self.panel, -1, 50, size=(150, 25), pos=(70,140))

        self.begbutton = wx.Button(self.panel, label = "开始", pos = (80, 170), size = (50, 30))
        self.canbutton = wx.Button(self.panel, label = "取消", pos = (170, 170), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.Confirm, self.begbutton)
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.canbutton)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def Confirm(self, event):
        '''
        确认开始
        '''
        checkedlists =  frame.listBox.GetCheckedStrings()
        checked = checkedlists[0].encode("utf-8")
        password = frame.accout[checked]

        BoardID = int(self.boardidtext.GetValue())
        ID = int(self.idtext.GetValue())
        begin = int(self.begintext.GetValue())
        end = int(self.endtext.GetValue())

        url = cc98lib.geturl(BoardID,ID)
        headers = cc98lib.login(checked, password)

        self.tongji = cc98lib.tongji(headers, url, begin, end)

        # 显示结果
        tojires = TongJiResultFrame(parent = None, id = -1)
        tojires.Show()
        self.Close()

    def Cancel(self, event):
        self.Close(True)
    def OnCloseWindow(self, event):
        self.Destroy()  

class TongJiResultFrame(wx.Frame):
    """
    统计水楼帖数界面：用于显示统计水楼帖数的结果
    """
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '水楼帖数统计结果', size=(300, 700))

        self.panel = wx.Panel(self)
        #-- sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_MULTILINE)

        rank = 1
        for item in frame.tongji.tongji:
            self.text.AppendText(str(rank) + " : " + item[0] + " : " + str(item[1]) + '\n')
            rank += 1

        self.sizer.Add(self.text, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)

        #-- 设置sizer
        self.panel.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()
        
class QiangLouFrame(wx.Frame):
    '''
    抢楼界面：设置 目标楼层 版块号 帖子id
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '抢楼', size=(300, 200))

        self.panel = wx.Panel(self)

        self.targetlabel = wx.StaticText(self.panel, -1, "Target:", (70, 20))
        self.targettext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140, 20))  

        self.boardidlabel = wx.StaticText(self.panel, -1, "boardid:", (70, 80))
        self.boardidtext = wx.TextCtrl(self.panel, 1, style=wx.TE_LEFT,pos=(140,80))
        self.idlabel = wx.StaticText(self.panel, -1, "id:",(70, 110))
        self.idtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT, pos=(140,110))

        self.begbutton = wx.Button(self.panel, label = "开始", pos = (80, 140), size = (50, 30))
        self.canbutton = wx.Button(self.panel, label = "取消", pos = (170, 140), size = (50, 30))
        self.Bind(wx.EVT_BUTTON, self.Confirm, self.begbutton)
        self.Bind(wx.EVT_BUTTON, self.Cancel, self.canbutton)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def Confirm(self, event):
        '''
        确认开始
        '''
        checkedlists =  frame.listBox.GetCheckedStrings()
        checked = checkedlists[0].encode("utf-8")
        password = frame.accout[checked]

        BoardID = int(self.boardidtext.GetValue())
        ID = int(self.idtext.GetValue())
        target = int(self.targettext.GetValue())
        # getcontent = frame.context.GetValue()
        headers = cc98lib.login(checked, password)

        self.qianglou = cc98lib.qianglou(getcontent, headers, target, BoardID, ID, getface)

        self.Close()

    def Cancel(self, event):
        self.Close(True)
    def OnCloseWindow(self, event):
        self.Destroy()  


class InsertFrame(wx.Frame):
    '''
    主窗口
        组成有：
            ——添加按钮 button           ——发帖表情
            ——全选按钮 choall           ——发帖内容  context
            ——用户列表 listBox         
            ——编辑按钮 editbutton       ——各种功能按钮
    '''
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'CC98 客户端',size=(850, 420))
        self.panel = wx.Panel(self)

        #-- 总的sizer
        self.allsizer = wx.FlexGridSizer(rows = 1, cols=2, vgap=300, hgap=20)

        #-- 右边区域的sizer
        self.rightsizer = wx.GridBagSizer(10,10)

        # 添加按钮
        self.button = wx.Button(self.panel, label="添加用户", pos=(20, 10), size=(70, 30))
        self.button.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.button.SetBackgroundColour("Navy")
        self.button.SetForegroundColour("white")
        self.button.SetToolTipString("This is a BIG button...")
        self.Bind(wx.EVT_BUTTON, self.AddUser, self.button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


        # 全选按钮
        self.choall = wx.CheckBox(self.panel, -1, "全选", pos=(22, 50), size=(60, 20))

        self.Bind(wx.EVT_CHECKBOX, self.OnRadio, self.choall)

        # 用户列表
        self.sampleList = []
        self.accout = {}
        
        file = open("./accout")
        # self.sampleList = ['昊墨之魂', '墨明棋妙', '墨诗莫忘'] 

        while 1:
            line = file.readline()
            # print line
            if not line:
                break
            line = line.split()
            self.sampleList.append(line[0])
            self.accout[line[0]] = line[1]
        file.close()

        self.listBox = wx.CheckListBox(self.panel, -1, (20, 70), (100, 300), self.sampleList,   
                wx.LB_SINGLE) 
        # listBox.SetSelection(3)


        # 编辑按钮
        self.editbutton = wx.Button(self.panel, label="编辑", pos=(20, 10), size=(70, 30))
        self.editbutton.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        # button.SetBezelWidth(5)
        self.editbutton.SetBackgroundColour("Navy")
        self.editbutton.SetForegroundColour("white")
        self.editbutton.SetToolTipString("This is a BIG button...")
        self.Bind(wx.EVT_BUTTON, self.EditUser, self.editbutton)
        
        #-- 以上控件添加到sizer
        self.rightsizer.Add(self.button, pos=(0, 0), flag=wx.ALIGN_CENTER, border=7)
        self.rightsizer.Add(self.choall, pos=(1, 0), flag=wx.LEFT, border=7)
        self.rightsizer.Add(self.listBox, pos=(2, 0), flag=wx.LEFT, border=7)
        self.rightsizer.Add(self.editbutton, pos=(3, 0), flag=wx.ALIGN_CENTER, border=7)



        #-- 左边区域的sizer
        self.leftsizer = wx.BoxSizer(wx.VERTICAL)
        
        # 发帖表情对应文件
        filenames = ["face1.gif", "face2.gif", "face3.gif", "face4.gif", "face5.gif", "face6.gif", "face7.gif", "face8.gif","face9.gif","face19.gif","face20.gif",
                     "face10.gif", "face11.gif", "face12.gif", "face13.gif", "face14.gif", "face15.gif", "face16.gif", "face17.gif","face18.gif","face21.gif","face22.gif"]

        #-- 发帖表情的sizer
        self.fgs = wx.FlexGridSizer(rows = 2, cols=11, vgap=20, hgap=20)

        # 发帖表情
        self.radios = []
        for name in filenames:
            name = "./resource/" + name
            self.face = wx.Image(name,wx.BITMAP_TYPE_GIF)
            self.facesizer = wx.GridBagSizer(1,0)

            self.radio = wx.RadioButton(self.panel, -1)
            self.face = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.face))

            self.radios.append(self.radio)

            self.facesizer.Add(self.radio, pos=(0, 0), flag=wx.ALIGN_CENTER, border=2)
            self.facesizer.Add(self.face, pos=(0, 1), flag=wx.ALIGN_CENTER, border=2)

            self.fgs.Add(self.facesizer)

        # 得到选择radiobutton
        for eachRadio in self.radios:
            self.Bind(wx.EVT_RADIOBUTTON, self.GetFace, eachRadio)

        # 发帖内容框
        self.context = wx.TextCtrl(self.panel, 1, style=wx.TE_MULTILINE)

        #-- BoardID和id的sizer
        self.urlsizer = wx.GridBagSizer(10,10)

        self.boardidlabel = wx.StaticText(self.panel, -1, "boardid:")
        self.idlabel = wx.StaticText(self.panel, -1, "id:")
        self.boardidtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT,size=(100,30))
        self.idtext = wx.TextCtrl(self.panel, -1, style=wx.TE_LEFT,size=(100,30))

        #-- 将以上控件放在urlsizer内
        self.urlsizer.Add(self.boardidlabel, pos=(0, 0), flag=wx.ALIGN_CENTER, border=7)
        self.urlsizer.Add(self.boardidtext, pos=(0, 1), flag=wx.ALIGN_CENTER, border=7)
        self.urlsizer.Add(self.idlabel, pos=(0, 2), flag=wx.ALIGN_CENTER, border=7)
        self.urlsizer.Add(self.idtext, pos=(0, 3), flag=wx.ALIGN_CENTER, border=7)

        #-- 一堆button的sizer
        self.buttonssizer = wx.GridBagSizer(10,10)

        #第一行
        self.replybutton = wx.Button(self.panel, label = "回复", size = (50, 30))
        self.visitorbutton = wx.Button(self.panel, label = "访客", size = (50, 30))
        self.tongjubutton = wx.Button(self.panel, label = "统计", size = (50, 30))        
        self.famibutton = wx.Button(self.panel, label = "发米", size = (50, 30))

        #第二行
        self.qiangloubutton = wx.Button(self.panel, label = "抢楼", size = (50, 30))
        self.dakabutton = wx.Button(self.panel, label = "打卡", size = (50,30))
        self.piliangbutton = wx.Button(self.panel, label = "批量传图", size = (100,30))
        
        #第三行
        self.aboutbutton = wx.Button(self.panel, label = "About", size = (50, 30))

        self.Bind(wx.EVT_BUTTON, self.Reply, self.replybutton)
        self.Bind(wx.EVT_BUTTON, self.Visitor, self.visitorbutton)
        self.Bind(wx.EVT_BUTTON, self.TongJi, self.tongjubutton)
        self.Bind(wx.EVT_BUTTON, self.FaMi, self.famibutton)
        self.Bind(wx.EVT_BUTTON, self.QiangLou, self.qiangloubutton)
        self.Bind(wx.EVT_BUTTON, self.DaKa, self.dakabutton)
        self.Bind(wx.EVT_BUTTON, self.PiLiang, self.piliangbutton)
        self.Bind(wx.EVT_BUTTON, self.About, self.aboutbutton)

        self.buttonssizer.Add(self.replybutton, pos=(0, 0), flag=wx.ALIGN_CENTER, border=7)
        self.buttonssizer.Add(self.visitorbutton, pos=(0, 1), flag=wx.ALIGN_CENTER, border=7)
        self.buttonssizer.Add(self.tongjubutton, pos=(0, 2), flag=wx.ALIGN_CENTER, border=7)
        self.buttonssizer.Add(self.famibutton, pos=(0, 3), flag=wx.ALIGN_CENTER, border=7)
        
        self.buttonssizer.Add(self.qiangloubutton, pos=(1, 0), flag=wx.ALIGN_CENTER, border=7)
        self.buttonssizer.Add(self.dakabutton, pos=(1, 1), flag=wx.ALIGN_CENTER, border=7)
        self.buttonssizer.Add(self.piliangbutton, pos=(1, 2), span=(1, 2), flag=wx.ALIGN_CENTER, border=7)

        self.buttonssizer.Add(self.aboutbutton, pos=(2, 1), flag=wx.ALIGN_CENTER, border=7)

        #-- 以上控件添加到sizer
        self.leftsizer.Add(self.fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)
        self.leftsizer.Add(self.context, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)
        self.leftsizer.Add(self.urlsizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)
        self.leftsizer.Add(self.buttonssizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)
        
        #-- 将左右sizer加入allsizer
        self.allsizer.Add(self.rightsizer)
        self.allsizer.Add(self.leftsizer)
        
        # 设置sizer
        self.panel.SetSizer(self.allsizer)

    def AddUser(self, event):
        adduser = AddUserFrame( parent = None, id = -1)
        adduser.Show()

    def EditUser(self,event):
        checklists =  frame.listBox.GetChecked()
        if len(checklists) > 1:
            toomany = wx.MessageDialog(None, "To many to edit", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = toomany.ShowModal()
            toomany.Destroy()
        elif len(checklists) < 1:
            nochose = wx.MessageDialog(None, "No chose to edit", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nochose.ShowModal()
            nochose.Destroy()
        else:
            edituser = EditUserFrame( parent = None, id = -1)
            edituser.Show()


    def OnRadio(self, event):
        '''
        全选按钮：如果选中则下面列表全部选中，如果再点击则全部不选中
        '''
        # 如果选中
        if self.choall.GetValue() == True:
            self.listBox.SetCheckedStrings(self.sampleList)
        # 如果再点击
        else:
            for i in self.listBox.GetChecked():
                self.listBox.Check(i,check = False)


    def GetFace(self, event):
        '''
        得到小表情 赋值给全局变量getface
        '''
        radioSelected = event.GetEventObject()
        
        # radiobox和小表情的对应关系
        facedict = {
            0 : "face1.gif", 
            1 : "face2.gif", 
            2 : "face3.gif", 
            3 : "face4.gif", 
            4 : "face5.gif", 
            5 : "face6.gif", 
            6 : "face7.gif", 
            7 : "face8.gif",
            8 : "face9.gif",
            9 : "face19.gif",
            10: "face20.gif",
            11: "face10.gif", 
            12: "face11.gif", 
            13: "face12.gif", 
            14: "face13.gif", 
            15: "face14.gif", 
            16: "face15.gif", 
            17: "face16.gif", 
            18: "face17.gif",
            19: "face18.gif",
            19: "face21.gif",
            20: "face22.gif"
        }

        getface = facedict[frame.radios.index(radioSelected)]


    def Reply(self, event):
        '''
        正常回复，刷一遍mj
        '''
        # 得到选中项
        checkedlists =  frame.listBox.GetCheckedStrings()

        # QAQ有时候可以
        for checked in checkedlists:
            checked = checked.encode("utf-8")
            password = frame.accout[checked]
            BoardID = frame.boardidtext.GetValue()
            ID = frame.idtext.GetValue()
            getcontent = frame.context.GetValue()
            headers = cc98lib.login(checked, password)

            # print checked
            # print password
            # print headers

            result = cc98lib.fatie(getcontent,headers,BoardID,ID,getface)


    def Visitor(self, event):
        '''
        用于统计一路访客
        '''
        checkedlists =  frame.listBox.GetCheckedStrings()
        if len(checkedlists) >= 1:
            self.visitor = VisitorFrame(parent = None, id = -1)
            self.visitor.Show()
        else:
            nochecked = wx.MessageDialog(None, "No ID chosed", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nochecked.ShowModal()
            nochecked.Destroy()

    def TongJi(self, event):
        '''
        用于统计水楼帖数
        '''
        checkedlists =  frame.listBox.GetCheckedStrings()
        if len(checkedlists) >= 1:
            self.tongji = TongJiFrame(parent = None, id = -1)
            self.tongji.Show()
        else:
            nochecked = wx.MessageDialog(None, "No ID chosed", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nochecked.ShowModal()
            nochecked.Destroy()

    def FaMi(self, event):
        '''
        暂时弃坑
        '''
        pass

    def QiangLou(self, event):
        checkedlists =  frame.listBox.GetCheckedStrings()
        if len(checkedlists) >= 1:
            self.qianglou = QiangLouFrame(parent = None, id = -1)
            self.qianglou.Show()
        else:
            nochecked = wx.MessageDialog(None, "No ID chosed", "Warning", wx.YES_NO | wx.ICON_QUESTION)
            retCode = nochecked.ShowModal()
            nochecked.Destroy()
        pass

    def DaKa(self, event):
        pass

    def PiLiang(self, event):
        '''
        批量上传：将该文件夹内所有文件上传，包括文件夹内文件夹内文件
        '''
        file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*" 
        # 选择文件夹
        dlg = wx.FileDialog(self, "Open paint file...",
                            os.getcwd(), 
                            style = wx.FD_CHANGE_DIR,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + '--' + self.filename)
        dlg.Destroy()
    
    def About(self, event):
        self.about = AboutFrame(parent = None, id = -1)
        self.about.Show()


    def OnCloseWindow(self, event):
        '''
        关闭程序时的操作，主要是保存帐号等信息 
        '''
        self.Destroy()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = InsertFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
