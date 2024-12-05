# -*- coding: utf-8 -*-

#导入程序运行必须模块
import os
import sys
import subprocess
import threading
import time
import psutil
#导入PyQt5模块
from PyQt5.QtCore import QObject, pyqtSignal
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
import serial.serialutil # type: ignore
#导入designer工具生成的login模块
from com import Ui_Serial # type: ignore
#import win32com.shell.shell as shell
#import struct
#print('当前Python解释器位数: ',struct.calcsize("P") * 8 )

import serial
import serial.tools.list_ports
global runing
runing=True
global S_exit
S_exit=False
global serial_port_num
serial_port_num=0

class MyMainForm(QMainWindow, Ui_Serial):
    #取串口列表
    available_ports = []
    #更新信号
    update_signal = pyqtSignal(int,bytes)

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #自动运行
        self.update_signal.connect(self.update_label)

        self.btn()
        #按键
        #self.pushButton.clicked.connect(self.btn)

    def update_label(self,i,received_data):
        print("更新标签\n"+str(i))
        print(len(self.available_ports))
        if len(self.available_ports)<i+1:
            print("串口数量不足")
            return
        
        label = getattr(self, "label_" + str(i+1))
        print("received_data=",received_data)
        label.setText(self.available_ports[i].name + "->" + str(received_data))
        #label.setText(label.text()+received_data.decode('utf-8')+'\n')
        if received_data == b'Hello,Serial!':
            label.setStyleSheet("background-color: rgb(14, 143, 22);color: rgb(255, 255, 255);")
        else:
            label.setStyleSheet("background-color: rgb(89, 146, 216);color: rgb(174, 209, 255)")

        if self.progressBar.value() < 100:
            self.progressBar.setProperty("value", self.progressBar.value() + 5)
        else:
            self.progressBar.setProperty("value", 5)

    def closeEvent(self, event):
        # 在窗口关闭时执行一些操作
        print("window is closing , do something")
        global runing
        runing=False
        global S_exit
        S_exit=True
        # 执行默认的窗口关闭事件
        super().closeEvent(event)

    def btn(self):
        thread1=threading.Thread(target=self.start_up)
        thread1.start()

    def start_up(self):

        global runing
        while runing:
            #print(runing)
            # 获取可用的串口列表
            self.available_ports = serial.tools.list_ports.comports()
            print("enable serial ports:",len(self.available_ports),"\n")
            self.label_10.setText("可用串口："+str(len(self.available_ports)))
            global serial_port_num
            if len(self.available_ports)==serial_port_num:
                print("no new serial")
            else:
                #重置标签样式
                for j in range(1,9):
                    label=getattr(self,"label_"+str(j))
                    label.setStyleSheet("background-color: rgb(152, 182, 223);color: rgb(174, 209, 255);")    
                    label.setText(" "+str(j)+"->")
                    #print(j)
                serial_port_num=len(self.available_ports)
                print("new serial port number：",serial_port_num)
                self.label_10.setText("新的串口数量："+str(serial_port_num))
                if S_exit==False:
                    runing=False
                    time.sleep(3)
                    runing=True
                # 显示每个可用串口的名字
                for i in range(len(self.available_ports)):
                    if i<8:
                        print(self.available_ports[i].name)
                        th=threading.Thread(target=self.mythread, args=(i,))
                        th.start()
            
            time.sleep(2)   # 休眠2秒

    def mythread(self,i):
        print("线程启动"+str(i))
        # 线程要执行的代码
        #self.label.setText("线程启动\n")
        time.sleep(i*0.5)   # 休眠i秒
        label=getattr(self,"label_"+str(i+1))
        print(label)
        label.setText(self.available_ports[i].name+"->")
        label.setStyleSheet("background-color: rgb(89, 146, 216);color: rgb(174, 209, 255);")
       
        # 打开串口
        print(self.available_ports[i].device)
        try:
            ser = serial.Serial(self.available_ports[i].device, 9600, timeout=1)  # 串口名为'COM1'，波特率为9600，超时时间为1秒
            if ser.is_open:
                print('serial port is open')
            else:
                print('serial port is not open')
                time.sleep(1)   # 休眠1秒
                print(self.available_ports[i].device)
            # 配置串口参数（例如：数据位、停止位、奇偶校验位）
            ser.bytesize = serial.EIGHTBITS  # 8位数据位
            ser.stopbits = serial.STOPBITS_ONE  # 1位停止位
            ser.parity = serial.PARITY_NONE  # 无校验
            data_to_send = b'Hello,Serial!'

            # 循环接收数据
            while runing:
                try:
                    # 发送数据
                    ser.write(data_to_send)
                    # 接收数据
                    received_data = ser.read(50)  # 读取最多50个字节的数据
                    print('received_data:', received_data)
                    self.update_signal.emit(i,received_data)
                except serial.serialutil.SerialException:
                    print("serial port is not open")
                    #ser.close()
                    break

        except:
            print("serial open failed")
            label.setText("串口打开失败")
            label.setStyleSheet("background-color: rgb(255, 255, 255);color: rgb(255, 0, 0);")
        finally:
            if "ser" in locals():
                ser.close()
        print("thread end"+str(i))

if __name__ == "__main__":
    print("start")
    print(psutil.Process().parent().name())
    # 判断是否有另一个实例在运行
    pro_i=0
    for process in psutil.process_iter(['pid', 'name']):
        #print(process.info,os.getpid())
        if process.info['name'] == psutil.Process().parent().name()  :
            print(process.info['pid'], process.info['name'],os.getpid())
            pro_i+=1
            if pro_i>3:  # 说明有多个实例在运行
                print("Another instance is running, quit now.")
                sys.exit()
    
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())