# -*- coding: utf-8 -*-





import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#import matplotlib
import numpy as np

class Okno(wx.Frame):
  
    def __init__(self, parent, title):
        super(Okno, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()
        self.Show()
    def InitUI(self):    
        #####<menu>
        menubar = wx.MenuBar()      
        fileMenu = wx.Menu()
        rysujMenu = wx.Menu()        
        #menu Plik        
        fitem = fileMenu.Append(wx.ID_EXIT, u'Zamknij', u'Zamknij program')        
        #menu Rysuj        
        fitem2 = rysujMenu.Append(12, u'Rysuj', u'Rysuj wykres')
        fitem3 = rysujMenu.Append(13, u'Rysuj', u'Rysuj wykres')
        #dolacz menu        
        menubar.Append(fileMenu, u'&Plik')
        menubar.Append(rysujMenu, u'&Rysuj')
        self.SetMenuBar(menubar)
        #podepnij zdarzenia pod menu
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_MENU, lambda event: self.RysujWykres(self,txt=u"haha"), fitem2)
        self.Bind(wx.EVT_MENU, lambda event: self.RysujWykres(self,txt=u"halo"), fitem3)
        #########</menu>

        #####<statusbar>        
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(u'Wykresy 1.0 - Ekran glowny')           
        ####</statusbar>
        
        self.SetSize((1024, 768))
        self.SetTitle(u'Wykresy 1.0')
        self.Centre()
        self.Show(True)        

    def OnQuit(self, e):
        self.Close()
        
    def RysujWykres(self,e,txt):
        self.panelWykres =MatplotPanel(self)
        self.panelWykres.rysuj(self,txt)
        print txt


class MatplotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,-1,size=(750,750))
    
    def rysuj(self,e,txt):    

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        t = np.arange(0.0,10,1.0)
        
        s = [0,1,0,1,0,2,1,2,1,0]
        if txt==u"halo":
            s = [2,1,1,1,3,2,1,2,1,0]              
        self.y_max = 1.0
        self.axes.plot(t,s)
        
        self.canvas = FigureCanvas(self,-1,self.figure)

    


class MenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,-1,size=(50,50))



class Zapytania():
    def kwoty_decyzji(self, rok):
        zapytanie_kwoty_decyzji_2015 ='''select month("12".data_wyk(d.data_wyk_pr,d.data_wyk_in)) as miesiac,
            sum("12".kwota_zar("12".dec_real(d.data_wyk_pr,d.data_wyk_in,d.inf_real_pr,d.inf_real_in),d.kwota_zar_pr,d.kwota_zar_in)) as kwota_zar_suma
            from DBA.d_list_decyzja as d where year("12".data_wyk(d.data_wyk_pr,d.data_wyk_in)) in('''+str(rok)+''') and d.status <> 'P'
            group by month("12".data_wyk(d.data_wyk_pr,d.data_wyk_in))
            order by month("12".data_wyk(d.data_wyk_pr,d.data_wyk_in)) asc'''
        
        return zapytanie_kwoty_decyzji_2015
        

if __name__ == '__main__':
    zapytania=Zapytania()
    kwoty_decyzji_2015=zapytania.kwoty_decyzji(2015)        
    app = wx.App(redirect=False)
    Okno(None, title=u'Wykresy 1.0')
    app.MainLoop()