# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
#从DCT.py调用模块
from DCT import dct_extract, dct_embed


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 800)
        self.getmsg = QtWidgets.QLineEdit(Form)
        self.getmsg.setGeometry(QtCore.QRect(160, 30, 221, 21))
        self.getmsg.setObjectName("getmsg")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(11, 30, 131, 20))
        self.label.setObjectName("label")
        self.bt1 = QtWidgets.QPushButton(Form)
        self.bt1.setGeometry(QtCore.QRect(400, 30, 181, 28))
        self.bt1.setObjectName("bt1")
        self.imgbefore = QtWidgets.QLabel(Form)
        self.imgbefore.setGeometry(QtCore.QRect(120, 80, 72, 15))
        self.imgbefore.setObjectName("imgbefore")
        self.imgafter = QtWidgets.QLabel(Form)
        self.imgafter.setGeometry(QtCore.QRect(500, 80, 72, 15))
        self.imgafter.setObjectName("imgafter")
        self.img1 = QtWidgets.QLabel(Form)
        self.img1.setGeometry(QtCore.QRect(40, 110, 300, 300))
        self.img1.setText("")
        self.img1.setObjectName("img1")
        self.img2 = QtWidgets.QLabel(Form)
        self.img2.setGeometry(QtCore.QRect(430, 100, 300, 300))
        self.img2.setText("")
        self.img2.setObjectName("img2")
        self.bt2 = QtWidgets.QPushButton(Form)
        self.bt2.setGeometry(QtCore.QRect(340, 420, 271, 28))
        self.bt2.setObjectName("bt2")
        self.img3 = QtWidgets.QLabel(Form)
        self.img3.setGeometry(QtCore.QRect(50, 470, 300, 300))
        self.img3.setText("")
        self.img3.setObjectName("img3")
        self.getlen = QtWidgets.QLineEdit(Form)
        self.getlen.setGeometry(QtCore.QRect(160, 420, 113, 21))
        self.getlen.setObjectName("getlen")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 420, 121, 16))
        self.label_2.setObjectName("label_2")
        self.outmsg = QtWidgets.QTextBrowser(Form)
        self.outmsg.setGeometry(QtCore.QRect(450, 480, 300, 300))
        self.outmsg.setObjectName("outmsg")

        self.retranslateUi(Form)
        self.bt1.clicked.connect(Form.bt1def)
        self.bt2.clicked.connect(Form.bt2def)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "输入要嵌入的信息："))
        self.bt1.setText(_translate("Form", "选择图片并嵌入信息"))
        self.imgbefore.setText(_translate("Form", "嵌入前："))
        self.imgafter.setText(_translate("Form", "嵌入后："))
        self.bt2.setText(_translate("Form", "选择图片并提取信息"))
        self.label_2.setText(_translate("Form", "提取的字节长度："))

    # 嵌入信息按钮的类
    def bt1def(self):
        #选择文件打开图片，格式默认png
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", " *.png;;")
        print(imgName)
        # 利用qlabel显示图片
        png = QtGui.QPixmap(imgName).scaled(self.img1.width(), self.img1.height())
        self.img1.setPixmap(png)
        #从getmsg控件获得要嵌入的信息
        msg = self.getmsg.text()
        #图像处理
        img_gray = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
        img_marked, len_msg = dct_embed(img_gray, msg, 20200417)
        #保存图像到项目根目录
        cv2.imwrite('marked.jpg', img_marked, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        imgout = './marked.jpg'
        #显示处理好的图像到label
        jpg = QtGui.QPixmap(imgout).scaled(self.img2.width(), self.img2.height())
        self.img2.setPixmap(jpg)

    def bt2def(self):
        # 选择文件打开图片，格式默认jpg
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", " *.jpg;;")
        print(imgName)
        # 利用qlabel显示图片
        png = QtGui.QPixmap(imgName).scaled(self.img3.width(), self.img3.height())
        self.img3.setPixmap(png)
        #从getlen获取字节长度
        len_msg = self.getlen.text()
        #将获取到的字节长度从str转换为int
        len_b=int(len_msg)
        #字节长度*8得到bit长度
        len_b*=8
        #根据bit长度从图片提取信息
        img_stego = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
        msg_out = dct_extract(img_stego, len_b, 20200417)
        #显示提取到的信息
        self.outmsg.append(msg_out)