from PyQt5 import QtCore 
# from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
# from PyQt5.QtCore import QThread, pyqtSignal

import time
import os
import json

from UI import Ui_MainWindow
from img_controller import img_controller

import ujson
from six.moves import cPickle as pickle

class MainWindow_controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        
        scenario_list = sorted(os.listdir("./label"))
        
        for scenario in scenario_list:
            self.ui.town_comboBox.addItem(scenario)
            
        self.file_path = f'./label/{self.ui.town_comboBox.currentText()}'
        
        self.img_controller = img_controller(img_path=self.file_path,
                                             ui=self.ui, Town= self.get_town(self.ui.town_comboBox.currentText()))

        self.ui.btn_zoom_in.clicked.connect(self.img_controller.set_zoom_in)
        self.ui.btn_zoom_out.clicked.connect(self.img_controller.set_zoom_out)
        self.ui.slider_zoom.valueChanged.connect(self.getslidervalue)   
        self.ui.slider_zoom.setProperty("value", 20)
        self.getslidervalue()     
        
           
        self.ui.town_comboBox.currentIndexChanged.connect(self.init_new_picture)
        
        self.ui.pushButton_clear.clicked.connect(self.img_controller.clear)
        
        self.ui.pushButton_save_region.clicked.connect(self.img_controller.save_flag)


        self.ui.pushButton_show_results.clicked.connect(self.img_controller.show_results)
        
        self.ui.pushButton_show_point.clicked.connect(self.img_controller.show_point)
     
     
        self.ui.pushButton_goal.clicked.connect(self.edit_goal_mode)
        
        self.ui.pushButton_color_area.clicked.connect(self.img_controller.show_selected_color_area)
        
        
        self.ui.pushButton_save_goals.clicked.connect(self.img_controller.save_goal)
        
        
        self.ui.pushButton_show_goals.clicked.connect(self.img_controller.show_goals)
        
        
        self.ui.pushButton_show_not_labeled_color.clicked.connect(self.img_controller.show_no_labeled_color )
        
        
        self.ui.btn_next.clicked.connect(self.variant_next )
        self.ui.btn_back.clicked.connect(self.variant_back )
        
        self.ui.pushButton_save_world_point.clicked.connect(self.save_target_point )
        
        #show_no_labeled_color
        
    def variant_back(self):
        index = self.ui.town_comboBox.currentIndex()
        index -=1
        if index < 0: 
            index = self.ui.town_comboBox.count() - 1
        self.ui.town_comboBox.setCurrentIndex(index)
        self.init_new_picture()
        
    def variant_next(self):
        index = self.ui.town_comboBox.currentIndex()
        index +=1
        if index >= self.ui.town_comboBox.count():
            index = 0
        self.ui.town_comboBox.setCurrentIndex(index)
        self.init_new_picture()
        
    def edit_goal_mode(self, ):
        self.img_controller.reverse_goals_flag()
        if self.img_controller.edit_goals_mode:
            self.ui.pushButton_goal.setStyleSheet("color: rgb(255, 255, 0)")
        else:
            self.ui.pushButton_goal.setStyleSheet("color: rgb(255, 255, 255)")
        

    def init_new_picture(self):

        self.img_controller.world_coordinate_list = []
        self.ui.slider_zoom.setProperty("value", 20)
        # self.file_path = f'./Maps/{self.ui.town_comboBox.currentText()}.png'
        
        self.file_path = f'./label/{self.ui.town_comboBox.currentText()}'
        self.img_controller.set_path(self.file_path, self.get_town(self.ui.town_comboBox.currentText()) )  
        self.getslidervalue()     


    def getslidervalue(self):        
        self.img_controller.set_slider_value(self.ui.slider_zoom.value()+1)
        # print(self.ui.slider_zoom.value()+1)
    
    
    def save_dict(self, di_, filename_):
        with open(filename_, 'wb') as f:
            pickle.dump(di_, f)
    def load_dict(self, filename_):
        with open(filename_, 'rb') as f:
            ret_di = pickle.load(f)
        return ret_di
    
    def save_target_point(self):
        
        json_path = f"obstacle_points/{self.ui.town_comboBox.currentText().replace('.png', '')}.json"
        save_points = []

        for point in self.img_controller.world_coordinate_list:
            save_points.append(point.tolist())

        print(f"{json_path}, {save_points}")

        with open(json_path, "w") as f:
            json.dump(save_points, f, indent=4)

        if os.path.exists(f'./target_points.pkl'):
            
            tags = self.load_dict(f'./target_points.pkl')
            tags[self.ui.town_comboBox.currentText().replace(".png", "")] = point
            self.save_dict(tags, f'./target_points.pkl')

        else:
            tags = {}
            tags[self.ui.town_comboBox.currentText().replace(".png", "")] = point
            self.save_dict(tags, f'./target_points.pkl')
            
        path = self.ui.town_comboBox.currentText().replace(".png", "")
            
            
    
    def get_town(self,  current_actor_path):
        
        if "10_" in current_actor_path:
            Town = "Town10HD"
        elif "7_" in current_actor_path:
            Town = "Town07"
        elif "6_" in current_actor_path:
            Town = "Town06"
        elif "5_" in current_actor_path:
            Town = "Town05"
        elif "3_" in current_actor_path:
            Town = "Town03"
        elif "2_" in current_actor_path:
            Town = "Town02"
        elif "1_" in current_actor_path:
            Town = "Town01"     
        elif "A0" in current_actor_path:
            Town = "A0"      
        elif "A1" in current_actor_path:
            Town = "A1"   
        elif "A6" in current_actor_path:
            Town = "A6"   
        elif "B3" in current_actor_path:
            Town = "B3"     
        elif "B7" in current_actor_path:
            Town = "B7"   
        elif "B8" in current_actor_path:
            Town = "B8" 
            
        return Town



