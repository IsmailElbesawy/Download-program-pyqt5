############# import main module ######
# PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import urllib.request
import pafy
import humanize

#--------------------- import Ui File ---------------------------#
# FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))
ui, _ = loadUiType('main.ui')


####### Intiate Ui File ######


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.InitUI()

        self.Handel_Buttons()

    def InitUI(self):
        # contain all ui changes in hoading
        # self.light_style()
        self.setWindowTitle('Python Downloader')
        self.tabWidget.tabBar().setVisible(False)
        self.setFixedSize(780, 444)

        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()

    #------------ start Connect Button with Method ---------------------#

    def Handel_Buttons(self):
        # connect download files button with method
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)

        # connect download video youtube button with method
        self.pushButton_4.clicked.connect(self.Download_youtube_video)
        self.pushButton_5.clicked.connect(self.Get_Video_data)
        self.pushButton_3.clicked.connect(self.Save_Browse)

        self.pushButton_6.clicked.connect(self.Handel_playlist_Browse)
        self.pushButton_7.clicked.connect(self.playlist_Download)

        self.pushButton_8.clicked.connect(self.Open_home)
        self.pushButton_9.clicked.connect(self.Open_downolad)
        self.pushButton_10.clicked.connect(self.Open_youtube)
        self.pushButton_11.clicked.connect(self.Open_sitting)

        self.pushButton_13.clicked.connect(self.light_style)
        self.pushButton_14.clicked.connect(self.dark_blue_style)
        self.pushButton_15.clicked.connect(self.dark_orange_style)
        self.pushButton_16.clicked.connect(self.amoled_style)
        self.pushButton_17.clicked.connect(self.light_style)
        self.pushButton_18.clicked.connect(self.style_style)
        self.pushButton_17.clicked.connect(self.dark_style)

    #------------ End Connect Button with Method ---------------------#

    #------------ Start  Download files method ---------------------#

    def Handel_Progress(self, blocknum, blocksize, totalsize):
        # calculate the progress
        readed_data = blocknum * blocksize
        if totalsize > 0:
            donwload_percentage = readed_data * 100 / totalsize
            print(donwload_percentage)
            self.progressBar.setValue(donwload_percentage)
        QApplication.processEvents()

    def Handel_Browse(self):
        # enable browseing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory="../../../Downloads", filter="All files(*.*);;Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)")
        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        # downloading any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error",
                                "Provied a valid url or save location")
        else:
            try:
                urllib.request.urlretrieve(
                    download_url, save_location, self.Handel_Progress)
                # show messges to complete download
                QMessageBox.information(
                    self, 'Download Complete', "The file download is completed")
                self.lineEdit.setText("")          # rest lineEdit to empty
                self.lineEdit_2.setText("")
                self.progressBar.setValue(0)        # rest progress bar to 0
            except Exception:
                QMessageBox.warning(
                    self, "Data Error", "Provied a valid url or url link is not working. The Download Faild")

    #------------ end Download files method ---------------------#

    #------------ Start Download youtube video method ---------------------#
    def Get_Video_data(self):
        video_url = self.lineEdit_3.text()
        if video_url == "":
            QMessageBox.warning(
                self, "Data Error", "Provied a valid video url")
        else:
            video = pafy.new(video_url)
            video_streams = video.videostreams
            for stream in video_streams:
                q = stream.quality.split('x')[1]+"p"
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(
                    stream.mediatype, stream.extension, q, size)
                self.comboBox.addItem(data)

    def Save_Browse(self):
        # enable browseing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(
            self, caption="Save as", directory="../../../Downloads/", filter="(*.mp4 *.mov *.3gp *.3gpp *.ogg *.oga *.wmv *.wma *.asf *.webm *.flv *.avi)"
        )
        self.lineEdit_4.setText(str(save_location[0]))

    def Download_youtube_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error",
                                "Provied a valid url video or save location")

        else:
            try:
                video = pafy.new(video_url)
                video_stream = video.videostreams
                video_quality = self.comboBox.currentIndex()
                download = video_stream[video_quality].download(
                    filepath=save_location, callback=self.Video_progress)
                # show messges to complete download
                QMessageBox.information(
                    self, 'Download Complete', "The Video download is completed")
                self.lineEdit_3.setText("")          # rest lineEdit to empty
                self.lineEdit_4.setText("")
                self.progressBar_2.setValue(0)       # rest progress bar to 0
                self.label_5.setText("")
                self.comboBox.clear()
            except Exception:
                QMessageBox.warning(
                    self, "Data Error", "Provied a valid url or url link is not working. The Download Faild")

    def Video_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            downoald_percentage = read_data*100 / total
            self.progressBar_2.setValue(downoald_percentage)
            remaining_time = round(time/60, 2)

            self.label_5.setText(
                str('{} minutes remaining'.format(remaining_time)))
        QApplication.processEvents()

    # ----------------- End Download youtube video method ------------------------- #

    #------------ Start Download youtube playlist video method ---------------------#

    def playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error",
                                "Provied a valid url playlist or save location")
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']
            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(
                callback=self.playlist_progress)
            QApplication.processEvents()

            current_video_in_download += 1

    def playlist_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            downoald_percentage = read_data*100 / total
            self.progressBar_3.setValue(downoald_percentage)
            remaining_time = round(time/60, 2)

            self.label_6.setText(
                str('{} minutes remaining'.format(remaining_time)))
        QApplication.processEvents()

    def Handel_playlist_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(
            self, "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)

    # ----------------- End Download youtube playlist video method ------------------------- #

    #------------ Start UI method ---------------------#
    def Open_home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_downolad(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_sitting(self):
        self.tabWidget.setCurrentIndex(3)

    def classic_style(self):
        style = open('theme/classic.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_blue_style(self):
        style = open('theme/dark_blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_style(self):
        style = open('theme/dark_orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def light_style(self):
        style = open('theme/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def style_style(self):
        style = open('theme/style.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def amoled_style(self):
        style = open('theme/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_style(self):
        style = open('theme/dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    #------------ End UI method ---------------------#

    #------------ start Animation ---------------------#

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation1.setDuration(1000)
        box_animation1.setStartValue(QRect(0, 0, 0, 0))
        box_animation1.setEndValue(QRect(140, 90, 301, 171))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(1000)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(470, 90, 301, 171))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(1000)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(140, 280, 301, 171))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(1000)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(470, 280,  301, 171))
        box_animation4.start()
        self.box_animation4 = box_animation4
    #------------ End Animation ---------------------#


def main():
    app = QApplication(sys.argv)
    windo = MainApp()
    windo.show()
    app.exec_()  # infinte loop


if __name__ == '__main__':
    main()
