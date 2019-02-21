'''
Created on 2019/1/29

@author: SR.WU
'''

import sys
import traceback
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic

#####exp code area########################################

# def exp_to_dict():
#     print('dict exp')
#     di = dict()
#     di['a'] = 'bc'
#     di['b'] = 'cd'
#     print(di['a'])
#          
#     if 'a' in di:
#         print('a is in di')
#     else:
#         print('a is not in di')
#          
#     if 'c' in di:
#         print('c is in di')
#     else:
#         print('c is not in di')   

# def exp_to_str_split():
#     print(sys._getframe().f_code.co_name)
#     s = '"Google#Runoob#Taobao#Facebook'
#     s_p = s.split('#')
#     
#     print(s_p)
#     print(len(s_p))

# def exp_use_tuple_as_dict_key():
#     arr = {(1,2,3):(555,444), (2,2,3):(666,555)}
#     
#     #exp 1
#     ret = arr[2,2,3]
#     print(type(ret))
#     print(ret)
# 
#     #exp 2
#     for (a,b,c),(d,e) in arr.items():
#         print(a,b,c,d,e)

def exp_to_str():
    s = 'abc*de'
    if '*' in s:
        print('hit')
        s = s.replace('*', '')
        print(f'new s = {s}')
    else:
        print('boo')

#############################################


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()        
        uic.loadUi('MainDialog.ui', self)
        self.setWindowTitle('Delta BOM ECN Description Producer')
        
        self.pushButton_openOld.clicked.connect(self.on_push_open_old)
        self.pushButton_openNew.clicked.connect(self.on_push_open_new)
        self.pushButton_outputResult.clicked.connect(self.on_push_output)
        self.old_file_path = ''
        self.new_file_path = ''        
        
        # some qt widget manipulation here.
#         self.btn_open_old = QPushButton()
#         self.btn_open_new = QPushButton()
#         self.btn_open_old.setText('open old')
#         self.btn_open_new.setText('open new')
#         
#         self.ledit_old = QLineEdit()
#         self.ledit_new = QLineEdit()
#         self.ledit_old.setText("press 'open old' to select your old BOM ")        
#         self.ledit_new.setText("press 'open old' to select your new BOM ")
# 
#         print(f'line edit size = {self.ledit_new.size().width()}, height = {self.ledit_new.size().height()}')           

    def on_push_open_old(self):        
        self.old_file_path, _fileter = QFileDialog.getOpenFileName(filter='*.txt')
        if self.old_file_path: # while not empty path
            print(self.old_file_path)
            self.lineEdit_oldFilePath.setText(self.old_file_path)                    
    
    def on_push_open_new(self):            
        self.new_file_path, _fileter = QFileDialog.getOpenFileName(filter='*.txt')    
        if self.new_file_path: # while not empty path
            print(self.new_file_path)
            self.lineEdit_newFilePath.setText(self.new_file_path)         
        
    def on_push_output(self):
        print('output') 
        try: 
            # the format of bom = {symbol_id : part_number]
            self.textBrowser_processStatus.setText('processing...')            
            old_bom, parse_log = BomTxtWorker.parse_file(self.old_file_path)
            self.textBrowser_processStatus.append(parse_log)
            new_bom, parse_log = BomTxtWorker.parse_file(self.new_file_path)
            self.textBrowser_processStatus.append(parse_log)
            savefile_path, _filter = QFileDialog.getSaveFileName(filter='*.txt')
            BomTxtWorker.save_ecn_description(old_bom, new_bom, savefile_path)
            self.textBrowser_processStatus.append('DONE! ECN content file has outputted, Sir.')
        except Exception as e: #TACTIC: To catches any exception (include inherited exception class)
            print(f'{type(e)}:{e}')
            #traceback.print_exc()
            #print(traceback.format_exc())
            #QMessageBox.critical(self, f'{type(e)}', f'{e},\n {traceback.format_exc()}') #TACTIC: perfect way to dump brief exception message.
            QMessageBox.critical(self, f'{type(e)}', f'{traceback.format_exc()}') #TACTIC: perfect way to dump exception traceback
            self.textBrowser_processStatus.setText('Waiting for you command, Sir.')                   

class BomTxtWorker():
    @staticmethod
    def parse_file(filepath):
        print(sys._getframe().f_code.co_name) # TACTIC: print the current function name
        
        if type(filepath)!= str:
            raise TypeError('Given arg filepath is not type str')

        if not filepath:
            raise ValueError('Given arg filepath is empty.')
        
        bom = dict()
        parse_log = ''   
            
        with open(filepath) as f:
            for line in f:  #TACTIC: readline from text file.                        
                parsed_line = line.split()
                if len(parsed_line) < 2:
                    print(f'illegal line: {line}')
                    parse_log += f'illegal line: {line}\n'
                else:
                    bom[parsed_line[0]] = parsed_line[1]
                    parse_log += f'got pair ({parsed_line[0]}, {parsed_line[1]})\n'                                        
        
        print(f'file ({filepath}), parsed line num = {len(bom)}')   
        parse_log += f'parse file ({filepath}), got num of symbols = {len(bom)}'
        return bom, parse_log

    @staticmethod
    def save_ecn_description(bom_old, bom_new, filepath):
        #argument check        
        if type(filepath)!= str:
            raise TypeError('Given arg filepath is not type str')
        if not filepath:
            raise ValueError('Given arg filepath is empty.')
        if type(bom_old)!=dict:
            raise TypeError('Given arg bom_old is not type dict')
        if type(bom_new)!=dict:
            raise TypeError('Given arg bom_new is not type dict')
                
        #sort out ADD, CHG, DEL dictionaries        
        dict_del = dict()
        dict_chg = dict()
        for symbol_id, part_num in bom_old.items():
            if symbol_id in bom_new:
                if part_num != bom_new[symbol_id]: #CHG case
                    part_transit = (part_num, bom_new[symbol_id])
                    if part_transit in dict_chg:
                        dict_chg[part_transit].append(symbol_id)
                    else:    
                        dict_chg[part_transit] = [symbol_id]
                
                #remove it from bom_new anyway. The rest items of bom_new would all be ADD case.
                bom_new.pop(symbol_id)
                        
            else: #DEL case                   
                if part_num in dict_del:                    
                    dict_del[part_num].append(symbol_id)
                else:
                    dict_del[part_num] = [symbol_id]   
        
        #sort out ADD dictionary step2, create inverse array.
        dict_add = dict()
        for symbol_id, part_num in bom_new.items():
            if part_num in dict_add:                    
                dict_add[part_num].append(symbol_id)
            else:
                dict_add[part_num] = [symbol_id]  
                                    
        #write result from three dictionaries        
        with open(filepath, 'w') as fp:
            for part_num, symbol_list in dict_add.items():
                text = 'ADD '
                for symbol in symbol_list:
                    text += f'{symbol},'
                text = f'{text[0:len(text)-1]} '  #replace ',' with space
                text += f'{part_num}\n'
                fp.write(text)

            for part_num, symbol_list in dict_del.items():
                text = 'DEL '
                for symbol in symbol_list:
                    text += f'{symbol},'
                text = f'{text[0:len(text)-1]} '  #replace ',' with space
                text += f'{part_num}\n'
                fp.write(text)
            
            for (part_old,part_new),symbol_list in dict_chg.items():
                text = 'CHG '
                for symbol in symbol_list:
                    text += f'{symbol},'
                text = f'{text[0:len(text)-1]} '  #replace ',' with space
                text += f'FM {part_old} TO {part_new}\n'
                fp.write(text)
            
def main():       
    try:     
        app = QtWidgets.QApplication(sys.argv)
        dlg = MainDialog()
        dlg.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f'{type(e)}:{e}')
    

if __name__ == '__main__':
    main()
    
    
    
