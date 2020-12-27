import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control.visualization import  FuzzyVariableVisualizer

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import sys

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class Fuzzy(QMainWindow):
    def __init__(self):
        super(Fuzzy, self).__init__()
        
        # load ui file
        self.ui = uic.loadUi('gui.ui', self)

        # click listener function of button
        self.ui.deploy_btn.clicked.connect(self.deploy)
        self.ui.calc_btn.clicked.connect(self.calculate)

        # initial function
        self.setup()

    def setup(self):
        # initial data
        self.velocity_membership = {
            "very_low" : [0, 0, 10, 15],
            "low" : [10, 22.5, 35],
            "medium" : [30, 47.5, 65],
            "high" : [55, 67.5, 80],
            "very_high" : [70, 75, 85, 85]
        }
        self.distance_membership = {
            "very_low" :[0, 0, 15, 30],
            "low" : [15, 30, 45],
            "medium" : [35, 55, 75],
            "high" : [60, 75, 90],
            "very_high" : [80, 85, 90, 90]
        }
        self.brake_membership = {
            "very_low" :[0, 0, 40, 50],
            "low" : [40, 100, 160],
            "medium" : [120, 190, 280],
            "high" : [240, 300, 360],
            "very_high" : [320, 330, 360, 360]
        }

        # list all ui combonen (object name) - input
        self.velocity_input = {
            "very_low" : [self.ui.line_vel_verlow_min, self.ui.line_vel_verlow_max],
            "low" : [self.ui.line_vel_low_min, self.ui.line_vel_low_max],
            "medium" : [self.ui.line_vel_med_min, self.ui.line_vel_med_max],
            "high" : [self.ui.line_vel_high_min, self.ui.line_vel_high_max],
            "very_high" : [self.ui.line_vel_verhigh_min, self.ui.line_vel_verhigh_max],
        }
        self.distance_input = {
            "very_low" : [self.ui.line_dis_verlow_min, self.ui.line_dis_verlow_max],
            "low" : [self.ui.line_dis_low_min, self.ui.line_dis_low_max],
            "medium" : [self.ui.line_dis_med_min, self.ui.line_dis_med_max],
            "high" : [self.ui.line_dis_high_min, self.ui.line_dis_high_max],
            "very_high" : [self.ui.line_dis_verhigh_min, self.ui.line_dis_verhigh_max],
        }
        self.brake_input = {
            "very_low" : [self.ui.line_brake_verlow_min, self.ui.line_brake_verlow_max],
            "low" : [self.ui.line_brake_low_min, self.ui.line_brake_low_max],
            "medium" : [self.ui.line_brake_med_min, self.ui.line_brake_med_max],
            "high" : [self.ui.line_brake_high_min, self.ui.line_brake_high_max],
            "very_high" : [self.ui.line_brake_verhigh_min, self.ui.line_brake_verhigh_max],
        }

        # list all ui combonen (object name) - label
        self.velocity_label = {
            "very_low" : [self.ui.label_vel_1, self.ui.label_vel_2, self.ui.label_vel_3],
            "low"  :[self.ui.label_vel_4, self.ui.label_vel_5, self.ui.label_vel_6],
            "medium" : [self.ui.label_vel_7, self.ui.label_vel_8, self.ui.label_vel_9],
            "high" :[self.ui.label_vel_10, self.ui.label_vel_11, self.ui.label_vel_12],
            "very_high" :[self.ui.label_vel_13, self.ui.label_vel_14, self.ui.label_vel_15],
        }
        self.distance_label = {
            "very_low" : [self.ui.label_dis_1, self.ui.label_dis_2, self.ui.label_dis_3],
            "low"  :[self.ui.label_dis_4, self.ui.label_dis_5, self.ui.label_dis_6],
            "medium" : [self.ui.label_dis_7, self.ui.label_dis_8, self.ui.label_dis_9],
            "high" :[self.ui.label_dis_10, self.ui.label_dis_11, self.ui.label_dis_12],
            "very_high" :[self.ui.label_dis_13, self.ui.label_dis_14, self.ui.label_dis_15],
        }
        self.brake_label = {
            "very_low" : [self.ui.label_brake_1, self.ui.label_brake_2, self.ui.label_brake_3],
            "low"  :[self.ui.label_brake_4, self.ui.label_brake_5, self.ui.label_brake_6],
            "medium" : [self.ui.label_brake_7, self.ui.label_brake_8, self.ui.label_brake_9],
            "high" :[self.ui.label_brake_10, self.ui.label_brake_11, self.ui.label_brake_12],
            "very_high" :[self.ui.label_brake_13, self.ui.label_brake_14, self.ui.label_brake_15],
        }

        # list all ui combonen (object name) - input max & min
        self.input_min_lis = [self.ui.line_vel_min, self.ui.line_dis_min, self.ui.line_brake_min]
        self.input_max_lis = [self.ui.line_vel_max, self.ui.line_dis_max, self.ui.line_brake_max]

        # input initial data to inputtext & label
        self.fill_input()
        self.fill_label()

    def fill_label(self):
        membership_range = [self.velocity_membership, self.distance_membership, self.brake_membership]
        label_list = [self.velocity_label, self.distance_label, self.brake_label]

        for index in range(3):
            self.input_min_lis[index].setText(str(membership_range[index]["very_low"][0]))
            self.input_max_lis[index].setText(str(membership_range[index]["very_high"][3]))
            for level in membership_range[index]:
                if level == "very_low":
                    label_list[index][level][0].setText(str(membership_range[index][level][1]))
                    label_list[index][level][1].setText(str(membership_range[index][level][2]))
                    label_list[index][level][2].setText(str(membership_range[index][level][3]))
                elif level == "very_high":
                    label_list[index][level][0].setText(str(membership_range[index][level][0]))
                    label_list[index][level][1].setText(str(membership_range[index][level][1]))
                    label_list[index][level][2].setText(str(membership_range[index][level][2]))
                else:
                    label_list[index][level][0].setText(str(membership_range[index][level][0]))
                    label_list[index][level][1].setText(str(membership_range[index][level][1]))
                    label_list[index][level][2].setText(str(membership_range[index][level][2]))

    def fill_input(self):

        membership_range = [self.velocity_membership, self.distance_membership, self.brake_membership]
        input_list = [self.velocity_input, self.distance_input, self.brake_input]
        
        for index in range(3):
            self.input_min_lis[index].setText(str(membership_range[index]["very_low"][0]))
            self.input_max_lis[index].setText(str(membership_range[index]["very_high"][3]))
            for level in membership_range[index]:
                if level == "very_low":
                    input_list[index][level][0].setText(str(membership_range[index][level][2]))
                    input_list[index][level][1].setText(str(membership_range[index][level][3]))
                elif level == "very_high":
                    input_list[index][level][0].setText(str(membership_range[index][level][0]))
                    input_list[index][level][1].setText(str(membership_range[index][level][1]))
                else:
                    input_list[index][level][0].setText(str(membership_range[index][level][0]))
                    input_list[index][level][1].setText(str(membership_range[index][level][2]))
        
    def get_value_input(self):
        membership_range = [self.velocity_membership, self.distance_membership, self.brake_membership]
        input_list = [self.velocity_input, self.distance_input, self.brake_input]

        for index in range(3):
            try:
                membership_range[index]["very_low"][0] = float(self.input_min_lis[index].text())
                membership_range[index]["very_low"][1] = float(self.input_min_lis[index].text())
            except:
                membership_range[index]["very_low"][0] = 0
                membership_range[index]["very_low"][1] = 0


            try:
                membership_range[index]["very_high"][2] = float(self.input_max_lis[index].text())
                membership_range[index]["very_high"][3] = float(self.input_max_lis[index].text())
            except:
                membership_range[index]["very_high"][2] = 100
                membership_range[index]["very_high"][3] = 100

            for level in membership_range[index]:
                if level == "very_low":
                    try:
                        membership_range[index][level][2] = float(input_list[index][level][0].text())
                        membership_range[index][level][3] = float(input_list[index][level][1].text())
                    except:
                        membership_range[index][level][2] = 0
                        membership_range[index][level][3] = 0
                elif level == "very_high":
                    try:
                        membership_range[index][level][0] = float(input_list[index][level][0].text())
                        membership_range[index][level][1] = float(input_list[index][level][1].text())
                    except:
                        membership_range[index][level][0] = 100
                        membership_range[index][level][1] = 100
                else:
                    try:
                        membership_range[index][level][0] = float(input_list[index][level][0].text())
                        membership_range[index][level][1] = (float(input_list[index][level][0].text()) + float(input_list[index][level][1].text())) /2
                        membership_range[index][level][2] = float(input_list[index][level][1].text())
                    except:
                        membership_range[index][level][0] = 0
                        membership_range[index][level][1] = 0
                        membership_range[index][level][2] = 0

    def deploy(self):
        self.get_value_input()
        self.fill_label()
        

    def calculate(self):
        # # New Antecedent/Consequent objects hold universe variables and membership
        # # functions
        membership_range = [self.velocity_membership, self.distance_membership, self.brake_membership]

        velocity = ctrl.Antecedent(np.arange(membership_range[0]["very_low"][0], membership_range[0]["very_high"][3], 0.5), 'velocity')
        distance = ctrl.Antecedent(np.arange(membership_range[1]["very_low"][0], membership_range[1]["very_high"][3], 0.5), 'distance')
        brake = ctrl.Consequent(np.arange(membership_range[2]["very_low"][0], membership_range[2]["very_high"][3], 0.5), 'brake')

        # # Custom membership functions can be built interactively with a familiar,

        velocity['very_low'] = fuzz.trapmf(velocity.universe, membership_range[0]["very_low"])
        velocity['low'] = fuzz.trimf(velocity.universe,membership_range[0]["low"])
        velocity['medium'] = fuzz.trimf(velocity.universe, membership_range[0]["medium"])
        velocity['high'] = fuzz.trimf(velocity.universe, membership_range[0]["high"])
        velocity['very_high'] = fuzz.trapmf(velocity.universe, membership_range[0]["very_high"])

        distance['very_low'] = fuzz.trapmf(distance.universe, membership_range[1]["very_low"])
        distance['low'] = fuzz.trimf(distance.universe, membership_range[1]["low"])
        distance['medium'] = fuzz.trimf(distance.universe, membership_range[1]["medium"])
        distance['high'] = fuzz.trimf(distance.universe, membership_range[1]["high"])
        distance['very_high'] = fuzz.trapmf(distance.universe, membership_range[1]["very_high"])

        brake['very_low'] = fuzz.trapmf(brake.universe, membership_range[2]["very_low"])
        brake['low'] = fuzz.trimf(brake.universe, membership_range[2]["low"])
        brake['medium'] = fuzz.trimf(brake.universe, membership_range[2]["medium"])
        brake['high'] = fuzz.trimf(brake.universe, membership_range[2]["high"])
        brake['very_high'] = fuzz.trapmf(brake.universe, membership_range[2]["very_high"])

        """
        =============================
        DECLARE THE RULES
        =============================
        """
        rule1 = ctrl.Rule(velocity['very_low'] & distance['very_low'], brake['medium'])
        rule2 = ctrl.Rule(velocity['very_low'] & distance['low'], brake['low'])
        rule3 = ctrl.Rule(velocity['very_low'] & distance['medium'], brake['low'])
        rule4 = ctrl.Rule(velocity['very_low'] & distance['high'], brake['very_low'])
        rule5 = ctrl.Rule(velocity['very_low'] & distance['very_high'], brake['very_low'])

        rule6 = ctrl.Rule(velocity['low'] & distance['very_low'], brake['high'])
        rule7 = ctrl.Rule(velocity['low'] & distance['low'], brake['medium'])
        rule8 = ctrl.Rule(velocity['low'] & distance['medium'], brake['low'])
        rule9 = ctrl.Rule(velocity['low'] & distance['high'], brake['very_low'])
        rule10 = ctrl.Rule(velocity['low'] & distance['very_high'], brake['very_low'])

        rule11 = ctrl.Rule(velocity['medium'] & distance['very_low'], brake['very_high'])
        rule12 = ctrl.Rule(velocity['medium'] & distance['low'], brake['high'])
        rule13 = ctrl.Rule(velocity['medium'] & distance['medium'], brake['medium'])
        rule14 = ctrl.Rule(velocity['medium'] & distance['high'], brake['low'])
        rule15 = ctrl.Rule(velocity['medium'] & distance['very_high'], brake['very_low'])

        rule16 = ctrl.Rule(velocity['high'] & distance['very_low'], brake['very_high'])
        rule17 = ctrl.Rule(velocity['high'] & distance['low'], brake['high'])
        rule18 = ctrl.Rule(velocity['high'] & distance['medium'], brake['high'])
        rule19 = ctrl.Rule(velocity['high'] & distance['high'], brake['medium'])
        rule20 = ctrl.Rule(velocity['high'] & distance['very_high'], brake['low'])

        rule21 = ctrl.Rule(velocity['very_high'] & distance['very_low'], brake['very_high'])
        rule22 = ctrl.Rule(velocity['very_high'] & distance['low'], brake['very_high'])
        rule23 = ctrl.Rule(velocity['very_high'] & distance['medium'], brake['high'])
        rule24 = ctrl.Rule(velocity['very_high'] & distance['high'], brake['medium'])
        rule25 = ctrl.Rule(velocity['very_high'] & distance['very_high'], brake['low'])

        brake_ctrl = ctrl.ControlSystem(
            [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, 
            rule19, rule20, rule21, rule22, rule23, rule24, rule25])

        """
        =============================
        SIMULATION
        =============================
        Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        """
        braking = ctrl.ControlSystemSimulation(brake_ctrl)
        
        try:
            x_vel = float(self.ui.input_vel.text())
            x_dis = float(self.ui.input_dis.text())
            braking.input['velocity'] = x_vel
            braking.input['distance'] = x_dis
        except:
            braking.input['velocity'] = 0
            braking.input['distance'] = 0
            x_vel = 0
            x_dis = 0
        
        # Crunch the numbers
        braking.compute()
        self.ui.label_output.setText("{0:.2f} m/s^2".format(braking.output['brake']))
        
        for i in reversed(range(self.ui.ver_lay1.count())): 
            self.ui.ver_lay1.itemAt(i).widget().setParent(None)
            
        for i in reversed(range(self.ui.ver_lay1_2.count())): 
            self.ui.ver_lay1_2.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ui.verticalLayout_8.count())): 
            self.ui.verticalLayout_8.itemAt(i).widget().setParent(None)

        plt.rcParams['figure.constrained_layout.use'] = True
        a1,b1 = FuzzyVariableVisualizer(velocity).view()
        a2,b2 = FuzzyVariableVisualizer(distance).view()
        a3,b3 = FuzzyVariableVisualizer(brake).view()

        b1.axvline(x=x_vel ,linewidth=3, color='k')
        b2.axvline(x=x_dis, linewidth=3, color='k')

        self.ui.canvas1 = FigureCanvas(a1)
        self.toolbar1 = NavigationToolbar(self.ui.canvas1, self)
   
        self.ui.canvas2 = FigureCanvas(a2)
        self.toolbar2 = NavigationToolbar(self.ui.canvas2, self)

        self.ui.canvas3 = FigureCanvas(a3)
        self.toolbar3 = NavigationToolbar(self.ui.canvas3, self)

        self.ui.ver_lay1.addWidget(self.ui.canvas1)
##        self.ui.ver_lay1.addWidget(self.toolbar1)
        self.ui.ver_lay1.addWidget(self.ui.canvas2)
##        self.ui.ver_lay1.addWidget(self.toolbar2)
##        self.ui.ver_lay1.addWidget(self.ui.canvas3)
##        self.ui.ver_lay1.addWidget(self.toolbar3)
        
        a4,b = FuzzyVariableVisualizer(brake).view(sim=braking)
        self.ui.canvas4 = FigureCanvas(a4)
        self.toolbar4 = NavigationToolbar(self.ui.canvas4, self)
        
        self.ui.ver_lay1_2.addWidget(self.ui.canvas4)
        self.ui.verticalLayout_8.addWidget(self.toolbar4)
        
        brake = None
        braking = None



if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    Dialog = Fuzzy()
    Dialog.setWindowTitle("Braking Simulator 1.0")
    Dialog.showMaximized()
    sys.exit(app.exec_())
