from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from pathlib import Path

import json
import os
from collections import OrderedDict
from UI import Ui_MainWindow
from video_controller import video_controller


class MainWindow_controller(QMainWindow):
    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.root = f""
        self.video_root = f""
        self.behavio_root = f""

        self.data_types = ["interactive",
                           "non-interactive", "obstacle", "collision"][:]

        self.init_video = True
        self.senario_clear = False
        self.basic_clear = False
        self.variant_clear = False

        self.ui.comboBox_scenario.clear()
        for _type in self.data_types:
            self.ui.comboBox_scenario.addItem(_type)
        self.update_scenario()

        self.init_video = False

        self.ui.pushButton_next.clicked.connect(self.frame_next)
        self.ui.pushButton_back.clicked.connect(self.frame_back)
        self.ui.pushButton_next_2.clicked.connect(self.variant_next)
        self.ui.pushButton_back_2.clicked.connect(self.variant_back)
        self.ui.pushButton_next_3.clicked.connect(self.basic_next)
        self.ui.pushButton_back_3.clicked.connect(self.basic_back)

        self.ui.start_frame_bottom.clicked.connect(self.set_start_frame)
        self.ui.end_frame_bottom.clicked.connect(self.set_end_frame)

        self.ui.delete_bottom.clicked.connect(self.delete_scenario)
        self.ui.undelete_bottom.clicked.connect(self.undelete_scenario)
        self.ui.copy_bottom.clicked.connect(self.copy_behavior)

        self.ui.comboBox_scenario.currentIndexChanged.connect(
            self.update_scenario)
        self.ui.comboBox_basic_scenario.currentIndexChanged.connect(
            self.update_basic)
        self.ui.comboBox_variant_scenario.currentIndexChanged.connect(
            self.update_variant)

        self.ui.button_openfile.clicked.connect(self.openfile)

    def openfile(self):
        path = str(Path('.').parent.absolute())
        path = os.path.join(path, self.var_path)
        path = path.replace("/", "//")
        os.system("gnome-open '%s'" % path)

    def load_json(self):

        if self.current_basic+"_"+self.current_variant in self.delete_list:
            self.ui.label_11.setText(f"Scenario deleted!")
        else:
            self.ui.label_11.setText(f"Behavior Stop")

        if os.path.exists(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+self.current_variant}.json"):
            with open(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+self.current_variant}.json", 'r') as openfile:
                data = json.load(openfile)
        else:
            data = {
                "start_frame": -1,
                "end_frame": -1
            }

        self.ui.start_frame_bottom.setText(
            f"Start: {(data['start_frame']):3d}")
        self.ui.end_frame_bottom.setText(f"End: {(data['end_frame']):3d}")

        return data

    def write_json(self):

        start_frame = int(self.ui.start_frame_bottom.text().split()[1])
        end_frame = int(self.ui.end_frame_bottom.text().split()[1])
        data = {
            "start_frame": start_frame,
            "end_frame": end_frame
        }
        with open(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+self.current_variant}.json", "w") as f:
            json.dump(data, f, indent=4)

    def update_video(self):

        self.video_path = f"{self.video_root}/{self.data_type}/{self.current_basic}_{self.current_variant}.mp4"
        assert os.path.exists(self.video_path), f"{self.video_path} not found"

        if self.init_video:
            self.video_controller = video_controller(
                video_path=self.video_path, ui=self.ui)

            self.ui.button_play.clicked.connect(self.video_controller.play)
            self.ui.button_stop.clicked.connect(self.video_controller.stop)
            self.ui.button_pause.clicked.connect(self.video_controller.pause)

        self.video_controller.update_video_path(self.video_path)

    def update_variant(self):

        if not self.variant_clear:
            self.current_variant = self.ui.comboBox_variant_scenario.currentText()

            self.update_video()
            self.load_json()

    def update_basic(self):

        if not self.basic_clear:
            self.current_basic = self.ui.comboBox_basic_scenario.currentText()

            self.variant_clear = True
            self.ui.comboBox_variant_scenario.clear()
            self.variant_clear = False

            for var in self.video_dict[self.current_basic]:
                self.ui.comboBox_variant_scenario.addItem(var)

            self.update_variant()

    def update_scenario(self):

        if not self.senario_clear:
            self.data_type = self.ui.comboBox_scenario.currentText()

            self.video_dict = OrderedDict()
            for video in sorted(os.listdir(self.video_root+f"/{self.data_type}")):
                basic_variant = video.split('.')[0]
                basic = "_".join(basic_variant.split('_')[:-3])
                variant = "_".join(basic_variant.split('_')[-3:])

                if basic in self.video_dict:
                    self.video_dict[basic].append(variant)
                else:
                    self.video_dict[basic] = [variant]

            self.deleted_json_name = f"remove/delete_scenario_{self.data_type}.json"
            if not os.path.exists(self.deleted_json_name):
                self.delete_list = {}
            else:
                self.delete_list = json.load(open(self.deleted_json_name))

            self.basic_clear = True
            self.ui.comboBox_basic_scenario.clear()
            self.basic_clear = False

            for basic in self.video_dict:
                self.ui.comboBox_basic_scenario.addItem(basic)

            self.update_basic()

    def frame_next(self):
        # frame no. start with 1
        current_frame_no = self.video_controller.current_frame_no
        current_frame_no = current_frame_no % self.video_controller.video_total_frame_count + 1
        self.video_controller.setslidervalue(current_frame_no)

    def frame_back(self):
        # frame no. start with 1
        current_frame_no = self.video_controller.current_frame_no
        current_frame_no = (
            current_frame_no-2) % self.video_controller.video_total_frame_count + 1
        self.video_controller.setslidervalue(current_frame_no)

    def variant_next(self):

        index = self.ui.comboBox_variant_scenario.currentIndex()
        index = (index+1) % self.ui.comboBox_variant_scenario.count()

        self.ui.comboBox_variant_scenario.setCurrentIndex(index)
        self.update_variant()

    def variant_back(self):

        index = self.ui.comboBox_variant_scenario.currentIndex()
        index = (index-1) % self.ui.comboBox_variant_scenario.count()

        self.ui.comboBox_variant_scenario.setCurrentIndex(index)
        self.update_variant()

    def basic_next(self):

        index = self.ui.comboBox_basic_scenario.currentIndex()
        index = (index+1) % self.ui.comboBox_basic_scenario.count()

        self.ui.comboBox_basic_scenario.setCurrentIndex(index)
        self.update_basic()

    def basic_back(self):

        index = self.ui.comboBox_basic_scenario.currentIndex()
        index = (index-1) % self.ui.comboBox_basic_scenario.count()

        self.ui.comboBox_basic_scenario.setCurrentIndex(index)
        self.update_basic()

    def set_start_frame(self):
        current_frame_no = self.video_controller.current_frame_no
        self.ui.start_frame_bottom.setText(f"Start: {current_frame_no:3d}")
        self.write_json()

    def set_end_frame(self):
        current_frame_no = self.video_controller.current_frame_no
        self.ui.end_frame_bottom.setText(f"End: {current_frame_no:3d}")
        self.write_json()

    def delete_scenario(self):

        self.delete_list[self.current_basic+"_"+self.current_variant] = ""

        tmp = json.load(open(self.deleted_json_name))
        self.delete_list.update(tmp)

        with open(self.deleted_json_name, "w") as f:
            json.dump(self.delete_list, f, indent=4)

        print([self.current_basic, self.current_variant], "\twill delete!!!")

        self.load_json()

    def undelete_scenario(self):

        if self.current_basic+"_"+self.current_variant in self.delete_list:

            del self.delete_list[self.current_basic+"_"+self.current_variant]

            tmp = json.load(open(self.deleted_json_name))
            if self.current_basic+"_"+self.current_variant in tmp:
                del tmp[self.current_basic+"_"+self.current_variant]
            self.delete_list.update(tmp)

            with open(self.deleted_json_name, "w") as f:
                json.dump(self.delete_list, f, indent=4)

            print([self.current_basic, self.current_variant], "\trecovered!!!")

            self.load_json()

    def copy_behavior(self):


        if os.path.exists(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+self.current_variant}.json"):
            with open(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+self.current_variant}.json", 'r') as openfile:
                data = json.load(openfile)

            N = self.ui.comboBox_variant_scenario.count()
            for i in range(N):
                variant = self.ui.comboBox_variant_scenario.itemText(i)

                with open(f"{self.behavio_root}/{self.data_type}/{self.current_basic+'_'+variant}.json", "w") as f:
                    json.dump(data, f, indent=4)

            self.load_json()
            print(f"Copy {N} variant in {self.current_basic}")

        else:
            print("Current variant no behavior!!!")
            return
