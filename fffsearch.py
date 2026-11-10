#!/usr/bin/python3
#-------------------------------------------------------------------------------
# Name:        fffsearch
# Purpose:
#
# Author:      Amir Geva
#
# Created:     07/04/2014
# Copyright:   (c) Amir Geva 2014
# Licence:     GPL V2
#-------------------------------------------------------------------------------
import sqlite3 as sq
import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import datetime, timedelta, date
import uis

def dateFormat(t):
    return str(date.fromtimestamp(t))

def launchFile(path):
    if sys.platform == 'win32':
        os.system("start "+path)
    if sys.platform.startswith('linux'):
        os.system('xdg-open '+path)
    

class SearchResults(QtCore.QAbstractTableModel):
    def __init__(self, contents, headers):
        super(SearchResults, self).__init__()
        self.contents = contents
        self.headers = headers

    def rowCount(self, parent):
        return len(self.contents)

    def columnCount(self,parent):
        if len(self.contents)==0:
            return 0
        return len(self.contents[0])

    def headerData(self,section,orientation,role):
        if role==QtCore.Qt.ItemDataRole.DisplayRole and orientation==QtCore.Qt.Orientation.Horizontal:
            return str(self.headers[section])

    def getCell(self,row,col):
        row=self.contents[row]
        return str(row[col])
            
    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            row=self.contents[index.row()]
            col=index.column()
            if col==3:
                return dateFormat(row[col])
            return str(row[col])

    def sort(self,column,order):
        rev=True
        if order==QtCore.Qt.SortOrder.AscendingOrder:
            rev=False
        s=sorted(self.contents,key=lambda row : row[column],reverse=rev)
        self.contents=s
        tl=self.createIndex(0,0,None)
        br=self.createIndex(self.rowCount(None),self.columnCount(None),None)
        self.dataChanged.emit(tl,br)

class SearchDialog(QtWidgets.QDialog):
    def __init__(self,dbcur,parent=None):
        super(SearchDialog,self).__init__(parent)
        uis.loadDialog('search',self)
        self.setWindowTitle('Fast File Find')
        self.cursor=dbcur
        self.dsize=None
        self.loadedLastSize=False

        self.searchTerm.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)
        self.searchButton.clicked.connect(self.searchPressed)
        self.resetButton.clicked.connect(self.resetPressed)

        headers=['Name','Path','Size','Date','Archive']
        c=[]
        self.results=SearchResults(c,headers)
        self.resultsList.setModel(self.results)
        self.resultsList.setSortingEnabled(True)
        self.resultsList.doubleClicked.connect(self.itemDoubleClick)
        self.resultsList.clicked.connect(self.itemClick)
        sm=self.resultsList.selectionModel()
        if sm is not None:
            sm.selectionChanged.connect(self.selChanged)
        else:
            print("No selection model")

        self.smallButton.clicked.connect(self.smallButtonPressed)
        self.largeButton.clicked.connect(self.largeButtonPressed)
        self.recentButton.clicked.connect(self.recentButtonPressed)
        self.dateType.currentIndexChanged.connect(self.dateTypeChanged)
        self.sizeType.currentIndexChanged.connect(self.sizeTypeChanged)
        
        #self.raiseTimer=QtCore.QTimer(self)
        #self.raiseTimer.timeout.connect(self.raiseWindow)
        #self.raiseTimer.start(200)
        
    def raiseWindow(self):
        self.raise_()
        self.activateWindow()
        self.raiseTimer.stop()
        self.raiseTimer=None

    def itemClick(self,index):
        pass
        
    def itemDoubleClick(self,index):
        row=index.row()
        archive=self.results.getCell(row,4)
        if len(archive)>0:
            launchFile(archive)
        else:
            filename=self.results.getCell(row,0)
            dir=self.results.getCell(row,1)
            path=os.path.join(dir,filename)
            launchFile(path)
        
        
    def manageLastSize(self):
        s=QtCore.QSettings("MLGSoft")
        if not self.loadedLastSize:
            self.loadedLastSize=True
            try:
                w=int(s.value('winWidth',defaultValue=640))
                h=int(s.value('winHeight',defaultValue=480))
                self.resize(QtCore.QSize(w,h))
                self.resizeEvent(None)
            except IOError:
                pass
        else:
            w=self.size().width()
            h=self.size().height()
            s.setValue('winWidth',w)
            s.setValue('winHeight',h)
            s.sync()


    def selChanged(self):
        pass

    def resizeEvent(self,event):
        if self.dsize is None:
            self.dsize=self.size()-self.resultsList.size()
        else:
            self.resultsList.resize(self.size()-self.dsize)
        self.manageLastSize()
                
    def resetPressed(self):
        self.exactCB.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.sizeType.setCurrentIndex(0)
        self.sizeEdit.setText('')
        self.sizeEdit.setDisabled(True)
        self.dateEdit.setText('')
        self.dateEdit.setDisabled(True)
        self.dateType.setCurrentIndex(0)
        self.searchTerm.setText('')
        self.extensionName.setText('')
        self.baseEdit.setText('')
        self.resultsEdit.setText('')
        self.setResults([], [])
        self.searchTerm.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)

    def sizeTypeChanged(self,index):
        self.sizeEdit.setEnabled(index>0)
        if (index>0):
            self.sizeEdit.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)

    def smallButtonPressed(self):
        self.sizeType.setCurrentIndex(1)
        self.sizeEdit.setEnabled(True)
        self.sizeEdit.setText('5000')

    def largeButtonPressed(self):
        self.sizeType.setCurrentIndex(2)
        self.sizeEdit.setEnabled(True)
        self.sizeEdit.setText('1000000')

    def recentButtonPressed(self):
        t=datetime.now()
        dt=timedelta(days=-91)
        t=t+dt
        self.dateEdit.setEnabled(True)
        d=(t.isoformat(' ').split())[0]
        self.dateType.setCurrentIndex(2)
        self.dateEdit.setText(d)

    def dateTypeChanged(self,index):
        self.dateEdit.setEnabled(index>0)

    def sizeCondition(self):
        size=0
        sizecond=""
        sizeind=self.sizeType.currentIndex()
        if sizeind>0:
            try:
                size=int(self.sizeEdit.text())
                if sizeind==1:
                    sizecond='<'
                else:
                    sizecond='>'
            except ValueError:
                sizecond=""
        if len(sizecond)>0:
            return "(size {} {})".format(sizecond,size)
        return ""

    def appendCondition(self,ql,cond):
        ql.append(" AND (")
        ql.append(cond)
        ql.append(")")

    def buildConditions(self, ql):
        ext=self.extensionName.text()
        term=self.searchTerm.text()
        if self.exactCB.checkState()==QtCore.Qt.CheckState.Checked:
            self.appendCondition(ql,"name = '{}'".format(term))
        else:
            terms=term.split(' ')
            for term in terms:
                if len(term)>0:
                    self.appendCondition(ql,"name LIKE '%{}%'".format(term))
        if len(ext)>0:
            self.appendCondition(ql,"ext=='.{}'".format(ext))
        sc=self.sizeCondition()
        if len(sc)>0:
            self.appendCondition(ql,sc)
        if self.dateType.currentIndex()>0:
            cond='>'
            if self.dateType.currentIndex()==1:
                cond='<'
            d=datetime.strptime(str(self.dateEdit.text()),"%Y-%m-%d")
            epoch = datetime.utcfromtimestamp(0)
            delta = d - epoch
            s=delta.total_seconds()
            self.appendCondition(ql,"time {} {}".format(cond,s))

    def searchFiles(self):
        base=self.baseEdit.text()
        ql=["SELECT name, dir, ext, size, time, path FROM t_files INNER JOIN t_dirs ON t_files.dir==t_dirs.id WHERE (1=1"]
        if len(base)>0:
            ql.append(" AND (path LIKE '{}%')".format(base))
        self.buildConditions(ql)
        ql.append(');')
        q=''.join(ql)
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def searchArchiveFiles(self):
        base=self.baseEdit.text()
        ql=["SELECT af.name, af.dir, af.ext, af.size, af.time, ad.path, a.path"
            " FROM t_archive_files af"
            " INNER JOIN t_archive_dirs ad ON af.dir==ad.id"
            " INNER JOIN t_archives a ON ad.archive==a.id"
            " WHERE (1=1"]
        if len(base)>0:
            ql.append(" AND (a.path LIKE '{}%')".format(base))
        self.buildConditions(ql)
        ql.append(');')
        q=''.join(ql)
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def searchPressed(self):
        file_rows = self.searchFiles()
        archive_rows = self.searchArchiveFiles()
        self.setResults(file_rows, archive_rows)
        self.resultsList.resizeColumnsToContents()

    def setResults(self, file_rows, archive_rows):
        headers=['Name','Path','Size','Date','Archive']
        c=[]
        for r in file_rows:
            (name, dir, ext, size, time, path)=r
            c.append([name,path,size,time,''])
        for r in archive_rows:
            (name, dir, ext, size, time, arc_dir, arc_path)=r
            c.append([name,arc_dir,size,time,arc_path])
        self.results=SearchResults(c,headers)
        self.resultsList.setModel(self.results)
        self.resultsEdit.setText('{}'.format(len(c)))




def main():
    root=os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    con=sq.connect('sindex.db')
    con.text_factory = str
    cur=con.cursor()
    app=QtWidgets.QApplication(sys.argv)
    d=SearchDialog(cur)
    d.show()
    d.showNormal()
    d.raise_()
    d.activateWindow()
    app.exec()

if __name__ == '__main__':
    main()

