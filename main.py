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
        self.ui = uic.loadUi('gui.ui', self)

        self.vel_max = 85.5
        self.dis_max = 90.5
        self.brake_max = 360.5

        self.vel_very_low = [0, 0, 10, 15]
        self.vel_low = [10, 22.5, 35]
        self.vel_med = [30, 47.5, 65]
        self.vel_high = [55, 67.5, 80]
        self.vel_very_high = [70, 75, 85, 85]

        self.dis_very_low = [0, 0, 15, 30]
        self.dis_low = [15, 30, 45]
        self.dis_med = [35, 55, 75]
        self.dis_high = [60, 75, 90]
        self.dis_very_high = [80, 85, 90, 90]

        self.brake_very_low = [0, 0, 40, 50]
        self.brake_low = [40, 100, 160]
        self.brake_med = [120, 190, 280]
        self.brake_high = [240, 300, 360]
        self.brake_very_high = [320, 330, 360, 360]

        self.ui.deploy_btn.toggled.connect(self.deploy)
        self.ui.deploy_btn.setCheckable(True)

        self.ui.calc_btn.toggled.connect(self.calculate)
        self.ui.calc_btn.setCheckable(True)
    
    def deploy(self):
        try:
            v_11 = float(self.ui.line_vel_verlow_min.text())
        except:
            v_11 = 10.0
        
        try:
            v_12 = float(self.ui.line_vel_verlow_max.text())
        except:
            v_12 = 15.0
        
        try:
            v_21 = float(self.ui.line_vel_low_min.text())
        except:
            v_21 = 10.0
        
        try:
            v_22 = float(self.ui.line_vel_low_max.text())
        except:
            v_22 = 35.0
        
        try:
            v_31 = float(self.ui.line_vel_med_min.text())
        except:
            v_31 = 30.0
        try:
            v_32 = float(self.ui.line_vel_med_max.text())
        except:
            v_32 = 65.0
        try:
            v_41 = float(self.ui.line_vel_high_min.text())
        except:
            v_41 = 55.0
        try:
            v_42 = float(self.ui.line_vel_high_max.text())
        except:
            v_42 = 80.0

        try:
            v_51 = float(self.ui.line_vel_verhigh_min.text())
        except:
            v_51 = 70.0
        try:
            v_52 = float(self.ui.line_vel_verhigh_max.text())
        except:
            v_52 = 75.0
        try:
            v_max = float(self.ui.line_vel_max.text())
        except:
            v_max = 85.0
        #=====================================================
        
        try:
            d_11 = float(self.ui.line_dis_verlow_min.text())
        except:
            d_11 = 15.0

        try:
            d_12 = float(self.ui.line_dis_verlow_max.text())
        except:
            d_12 = 30.0

        try:
            d_21 = float(self.ui.line_dis_low_min.text())
        except:
            d_21 = 15.0

        try:
            d_22 = float(self.ui.line_dis_low_max.text())
        except:
            d_22 = 45.0

        try:
            d_31 = float(self.ui.line_dis_med_min.text())
        except:
            d_31 = 35.0
        try:
            d_32 = float(self.ui.line_dis_med_max.text())
        except:
            d_32 = 75.0
        try:
            d_41 = float(self.ui.line_dis_high_min.text())
        except:
            d_41 = 60.0
        try:
            d_42 = float(self.ui.line_dis_high_max.text())
        except:
            d_42 = 90.0

        try:
            d_51 = float(self.ui.line_dis_verhigh_min.text())
        except:
            d_51 = 80.0
        try:
            d_52 = float(self.ui.line_dis_verhigh_max.text())
        except:
            d_52 = 85.0
        
        try:
            d_max = float(self.ui.line_dis_max.text())
        except:
            d_max = 90.0
#=====================================================
        

        
        try:
            b_11 = float(self.ui.line_brake_verlow_min.text())
        except:
            b_11 = 40.0

        try:
            b_12 = float(self.ui.line_brake_verlow_max.text())
        except:
            b_12 = 50.0

        try:
            b_21 = float(self.ui.line_brake_low_min.text())
        except:
            b_21 = 40.0

        try:
            b_22 = float(self.ui.line_brake_low_max.text())
        except:
            b_22 = 160.0

        try:
            b_31 = float(self.ui.line_brake_med_min.text())
        except:
            b_31 = 120.0
        try:
            b_32 = float(self.ui.line_brake_med_max.text())
        except:
            b_32 = 280.0
        try:
            b_41 = float(self.ui.line_brake_high_min.text())
        except:
            b_41 = 240.0
        try:
            b_42 = float(self.ui.line_brake_high_max.text())
        except:
            b_42 = 360.0

        try:
            b_51 = float(self.ui.line_brake_verhigh_min.text())
        except:
            b_51 = 320.0
        try:
            b_52 = float(self.ui.line_brake_verhigh_max.text())
        except:
            b_52 = 330.0
            
        try:
            b_max = float(self.ui.line_brake_max.text())
        except:
            b_max = 360.0

        
        self.vel_very_low = [0, 0, v_11, v_12]
        self.vel_low = [v_21, (v_21+v_22)/2 , v_22]
        self.vel_med = [v_31, (v_31+v_32)/2, v_32]
        self.vel_high = [v_41, (v_41+v_42)/2, v_42]
        self.vel_very_high = [v_51, v_52, v_max, v_max]

        self.dis_very_low = [0, 0, d_11, d_12]
        self.dis_low = [d_21, (d_21+d_22)/2, d_22]
        self.dis_med = [d_31, (d_31+d_32)/2, d_32]
        self.dis_high = [d_41, (d_41+d_42)/2, d_42]
        self.dis_very_high = [d_51, d_52, d_max, d_max]

        self.brake_very_low = [0, 0, b_11, b_12]
        self.brake_low = [b_21, (b_21+b_22)/2, b_22]
        self.brake_med = [b_31, (b_31+b_32)/2, b_32]
        self.brake_high = [b_41, (b_41+b_42)/2, b_42]
        self.brake_very_high = [b_51, b_52, b_max, b_max]

        self.vel_max = max(v_max, v_42)
        self.dis_max = max(d_max ,d_42)
        self.brake_max = max(b_max, b_42)
        
        
        self.ui.lbl_v_verlow.setText('[0:{}:{}]'.format(v_11,v_12))
        self.ui.lbl_v_low.setText('[{}:{}:{}]'.format(v_21,(v_21+v_22)/2,v_22))
        self.ui.lbl_v_med.setText('[{}:{}:{}]'.format(v_31,(v_31+v_32)/2,v_32))
        self.ui.lbl_v_high.setText('[{}:{}:{}]'.format(v_41,(v_41+v_42)/2,v_42))
        self.ui.lbl_v_verhigh.setText('[{}:{}:{}]'.format(v_51,v_52,v_max))
        
                
        self.ui.lbl_d_verlow.setText('[0:{}:{}]'.format(d_11,d_12))
        self.ui.lbl_d_low.setText('[{}:{}:{}]'.format(d_21,(d_21+d_22)/2,d_22))
        self.ui.lbl_d_med.setText('[{}:{}:{}]'.format(d_31,(d_31+d_32)/2,d_32))
        self.ui.lbl_d_high.setText('[{}:{}:{}]'.format(d_41,(d_41+d_42)/2,d_42))
        self.ui.lbl_d_verhigh.setText('[{}:{}:{}]'.format(d_51,d_52,d_max))
        
        self.ui.lbl_b_verlow.setText('[0:{}:{}]'.format(b_11,b_12))
        self.ui.lbl_b_low.setText('[{}:{}:{}]'.format(b_21,(b_21+b_22)/2,b_22))
        self.ui.lbl_b_med.setText('[{}:{}:{}]'.format(b_31,(b_31+b_32)/2,b_32))
        self.ui.lbl_b_high.setText('[{}:{}:{}]'.format(b_41,(b_41+b_42)/2,b_42))
        self.ui.lbl_b_verhigh.setText('[{}:{}:{}]'.format(b_51,b_52,b_max))
        

    def calculate(self):
        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        velocity = ctrl.Antecedent(np.arange(0, self.vel_max, 0.5), 'velocity')
        distance = ctrl.Antecedent(np.arange(0, self.dis_max, 0.5), 'distance')
        brake = ctrl.Consequent(np.arange(0, self.brake_max, 0.5), 'brake')

        # Custom membership functions can be built interactively with a familiar,

        velocity['very_low'] = fuzz.trapmf(velocity.universe, self.vel_very_low)
        velocity['low'] = fuzz.trimf(velocity.universe, self.vel_low)
        velocity['medium'] = fuzz.trimf(velocity.universe, self.vel_med)
        velocity['high'] = fuzz.trimf(velocity.universe, self.vel_high)
        velocity['very_high'] = fuzz.trapmf(velocity.universe, self.vel_very_high)

        distance['very_low'] = fuzz.trapmf(distance.universe, self.dis_very_low)
        distance['low'] = fuzz.trimf(distance.universe, self.dis_low)
        distance['medium'] = fuzz.trimf(distance.universe, self.dis_med)
        distance['high'] = fuzz.trimf(distance.universe, self.dis_high)
        distance['very_high'] = fuzz.trapmf(distance.universe, self.dis_very_high)

        brake['very_low'] = fuzz.trapmf(brake.universe, self.brake_very_low)
        brake['low'] = fuzz.trimf(brake.universe, self.brake_low)
        brake['medium'] = fuzz.trimf(brake.universe, self.brake_med)
        brake['high'] = fuzz.trimf(brake.universe, self.brake_high)
        brake['very_high'] = fuzz.trapmf(brake.universe, self.brake_very_high)





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
        self.ui.ver_lay1_2.addWidget(self.toolbar4)
        
        
        brake = None
        braking = None



if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    Dialog = Fuzzy()
    Dialog.setWindowTitle("Braking Simulator 1.0")
    Dialog.showMaximized()
    sys.exit(app.exec_())
