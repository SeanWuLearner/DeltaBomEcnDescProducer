'''
Created on 2019/1/29

@author: SR.WU
'''

import sys
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.setWindowTitle('Delta BOM ECN Description Producer')
                    
        self.mainlayout = QVBoxLayout(self)  # equivalent to self.setLayout(self.mainlayout)
        self.hlayout_up = QHBoxLayout()         
        self.hlayout_down = QHBoxLayout()
        self.mainlayout.addLayout(self.hlayout_up)
        self.mainlayout.addLayout(self.hlayout_down)                
        
        self.btn_open_old = QPushButton()
        self.btn_open_new = QPushButton()
        self.btn_open_old.setText('open old')
        self.btn_open_new.setText('open new')
        
        self.ledit_old = QLineEdit()
        self.ledit_new = QLineEdit()
        self.ledit_old.setText("press 'open old' to select your old BOM ")        
        self.ledit_new.setText("press 'open old' to select your new BOM ")
        self.ledit_old.adjustSize()
        #self.ledit_new.adjustSize()
        self.ledit_new.setBaseSize(400, 800)  ## SRWU: To work from here.

        print(f'line edit size = {self.ledit_new.size().width()}, height = {self.ledit_new.size().height()}')  
        
        
        
        self.hlayout_up.addWidget(self.btn_open_old)
        self.hlayout_up.addWidget(self.ledit_old)
        self.hlayout_down.addWidget(self.btn_open_new)
        self.hlayout_down.addWidget(self.ledit_new)
                    
        
        
        
        self.adjustSize()        


class PartLine():
    def __init__(self, cate='UNK', cate_id=9999, has_asterisk=False, part_no='0123456789'):
        self.cate = cate
        self.cate_id = cate_id
        self.has_asterisk = has_asterisk
        self.part_no = part_no

class BomTxtParser():
    @staticmethod
    def parse():
        print('static func in parser') 

def main():    
    #BomTxtParser.parse()
    app = QtWidgets.QApplication(sys.argv)
    dlg = MainDialog()
    dlg.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()