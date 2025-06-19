import sys
import io
import os
import folium 
import requests
import pygame 
import pyttsx3 
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QMessageBox, QPushButton, QLineEdit, QLabel, QCheckBox, QSizePolicy)
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5 import QtCore, QtGui, QtWidgets
from gauge import AnalogGaugeWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtwidgets import *
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QDateTime 
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtWidgets import QLabel, QPushButton, QFrame


import cv2
import random
import psutil  
import math

pygame.mixer.init()

class ModernButton(QPushButton):
    """Modern styled button with hover effects"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumWidth(110)  
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(43, 87, 151, 180),
                    stop:0.5 rgba(64, 128, 255, 200),
                    stop:1 rgba(43, 87, 151, 180));
                border: 2px solid rgba(255, 255, 255, 30);
                border-radius: 15px;
                color: white;
                font: bold 11pt "Segoe UI";
                padding: 8px 20px;  /* Increased horizontal padding */
                text-align: center;
                letter-spacing: 0.5px;
            }
        
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(64, 128, 255, 220),
                    stop:0.5 rgba(85, 149, 255, 240),
                    stop:1 rgba(64, 128, 255, 220));
                border: 2px solid rgba(255, 255, 255, 80);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(33, 67, 131, 200),
                    stop:0.5 rgba(43, 87, 151, 220),
                    stop:1 rgba(33, 67, 131, 200));
                border: 2px solid rgba(255, 255, 255, 50);
            }
            
            QPushButton:focus {
                outline: none;
                border: 2px solid rgba(100, 200, 255, 150);
            }
        """)

class InteractiveToggleButton(QPushButton):
    """Interactive toggle button with modern styling"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.is_toggled = False
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(152, 57, 38, 120),
                    stop:1 rgba(180, 70, 50, 140));
                border: 2px solid rgba(255, 100, 100, 100);
                border-radius: 20px;
                color: white;
                font: bold 10pt "Segoe UI";
                padding: 8px 16px;
                min-width: 100px;
                text-align: center;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(172, 77, 58, 160),
                    stop:1 rgba(200, 90, 70, 180));
                border: 2px solid rgba(255, 120, 120, 150);
            }
            
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(50, 150, 50, 160),
                    stop:1 rgba(80, 180, 80, 180));
                border: 2px solid rgba(100, 255, 100, 150);
            }
            
            QPushButton:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(70, 170, 70, 180),
                    stop:1 rgba(100, 200, 100, 200));
                border: 2px solid rgba(120, 255, 120, 180);
            }
        """)

class ModernControlButton(QPushButton):
    """Modern control button for map and music controls"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(0, 171, 169, 200),
                    stop:0.7 rgba(0, 151, 149, 180),
                    stop:1 rgba(0, 131, 129, 160));
                border: 2px solid rgba(0, 255, 253, 100);
                border-radius: 12px;
                color: white;
                font: bold 10pt "Segoe UI";
                padding: 6px 12px;
                text-align: center;
            }
            
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(20, 191, 189, 220),
                    stop:0.7 rgba(20, 171, 169, 200),
                    stop:1 rgba(20, 151, 149, 180));
                border: 2px solid rgba(50, 255, 253, 150);
            }
            
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(0, 141, 139, 180),
                    stop:0.7 rgba(0, 121, 119, 160),
                    stop:1 rgba(0, 101, 99, 140));
                border: 2px solid rgba(0, 200, 198, 80);
            }
        """)

class GlowingMusicButton(QPushButton):
    """Glowing music control button"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 200),
                    stop:0.3 rgba(64, 128, 255, 180),
                    stop:1 rgba(43, 87, 151, 160));
                border: 2px solid rgba(100, 200, 255, 150);
                border-radius: 17px;
                padding: 5px;
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 240),
                    stop:0.3 rgba(84, 148, 255, 200),
                    stop:1 rgba(63, 107, 171, 180));
                border: 2px solid rgba(150, 250, 255, 200);
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(200, 200, 200, 180),
                    stop:0.3 rgba(44, 88, 155, 160),
                    stop:1 rgba(23, 67, 131, 140));
                border: 2px solid rgba(80, 180, 255, 120);
            }
        """)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
        self.last_warning = {}  # Store last warning for each tyre
        
        # Initialize tyre monitoring variables with different starting values
        self.tyre_data = {
            'FL': {'pressure': 32.0, 'temp': 35.0, 'last_update': 0, 'warning_active': False, 'warnings': []},
            'FR': {'pressure': 31.5, 'temp': 34.0, 'last_update': 0, 'warning_active': False, 'warnings': []},
            'RL': {'pressure': 32.5, 'temp': 33.5, 'last_update': 0, 'warning_active': False, 'warnings': []},
            'RR': {'pressure': 31.8, 'temp': 34.5, 'last_update': 0, 'warning_active': False, 'warnings': []}
        }
        
        # Add variables for warning system
        self.current_warning_tyre = None
        self.warning_duration = 15  # Duration for each warning
        self.normal_duration = 10   # Duration for normal condition display
        self.cooldown_duration = 5  # Time between warnings in seconds
        self.last_warning_time = 0
        self.warning_stage = 0  # Track current stage in warning sequence
        self.simulation_time = 0  # Initialize simulation time
        self.is_normal_phase = False  # Track if we're in normal condition phase
        
        # Create a realistic warning sequence with normal conditions between warnings
        self.warning_sequence = [
            # Original sequence
            {'type': 'normal', 'duration': 15},
            {'tyre': 'RR', 'type': 'pressure_high', 'value': 40.0},
            {'type': 'normal', 'duration': 10},
            {'tyre': 'FR', 'type': 'temp_low', 'value': 25.0},
            {'type': 'normal', 'duration': 10},
            {'tyre': 'FL', 'type': 'pressure_low', 'value': 22.0},
            {'type': 'normal', 'duration': 10},
            {'tyre': 'RL', 'type': 'both', 'pressure': 40.0, 'temp': 70.0},
            {'type': 'normal', 'duration': 10},
            {'tyre': 'FR', 'type': 'temp_high', 'value': 70.0},
            {'type': 'normal', 'duration': 10},
            
            # Additional realistic scenarios
            # Rapid pressure loss scenario
            {'tyre': 'FL', 'type': 'pressure_dropping', 'value': 28.0, 'rate': -2.0},
            {'type': 'normal', 'duration': 10},
            
            # High-speed temperature spike
            {'tyre': 'RR', 'type': 'temp_spike', 'value': 75.0},
            {'type': 'normal', 'duration': 10},
            
            # Multiple tyre pressure imbalance
            {'tyre': 'FL', 'type': 'pressure_high', 'value': 38.0},
            {'tyre': 'FR', 'type': 'pressure_low', 'value': 24.0},
            {'type': 'normal', 'duration': 10},
            
            # Emergency braking temperature warning
            {'tyre': 'FL', 'type': 'both', 'pressure': 35.0, 'temp': 72.0},
            {'tyre': 'FR', 'type': 'both', 'pressure': 35.0, 'temp': 72.0},
            {'type': 'normal', 'duration': 10},
            
            # Slow leak simulation
            {'tyre': 'RL', 'type': 'pressure_dropping', 'value': 30.0, 'rate': -0.5},
            {'type': 'normal', 'duration': 10},
            
            # Uneven wear pattern indication
            {'tyre': 'RR', 'type': 'both', 'pressure': 33.0, 'temp': 68.0},
            {'tyre': 'RL', 'type': 'both', 'pressure': 29.0, 'temp': 68.0},
            {'type': 'normal', 'duration': 10},
            
            # Critical low pressure emergency
            {'tyre': 'FR', 'type': 'pressure_low', 'value': 20.0},
            {'type': 'normal', 'duration': 15}
        ]
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(1117, 636)  # Set minimum size
        MainWindow.setStyleSheet("background-color: rgb(30, 31, 40);")
        
        # Create central widget and main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Create a single widget to hold everything
        self.main_container = QWidget(self.centralwidget)
        self.main_container.setFixedSize(1117, 636)
        
        # Center the main container in the window
        self.main_container.setStyleSheet("""
            QWidget {
                background-color: rgb(30, 31, 40);
            }
        """)
        
        # Create layout for the central widget
        layout = QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_container, 0, Qt.AlignCenter)
        
        # Set up background image with proper z-order
        self.label = QtWidgets.QLabel(self.main_container)
        self.label.setGeometry(QtCore.QRect(0, 0, 1117, 636))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/bg/Untitled (1).png"))
        self.label.setScaledContents(True)
        self.label.lower()  # Make sure background stays at the back

        self.current_music_file = None
        self.is_playing = False
        self.is_paused = False
        
        self.current_location = [15.3647, 75.1240]
        self.destination = None
        
        # Calculate centered positions relative to container
        frame_x = (1117 - 521) // 2
        content_x = (1117 - 971) // 2
        
        # Add mode toggle to main container
        self.mode_toggle = QCheckBox("Light Mode", self.main_container)
        self.mode_toggle.setGeometry(10, 10, 150, 40)
        self.mode_toggle.setStyleSheet("""
            QCheckBox {
                color: white; 
                font: bold 10pt 'Segoe UI';
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid rgba(100, 150, 255, 150);
                background: rgba(30, 31, 40, 200);
            }
            QCheckBox::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(100, 200, 255, 255),
                    stop:1 rgba(50, 150, 255, 200));
                border: 2px solid rgba(150, 200, 255, 200);
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(150, 200, 255, 200);
            }
        """)
        self.mode_toggle.stateChanged.connect(self.toggle_mode)
        
        # Add attribution label to main container
        self.attribution_label = QtWidgets.QLabel("by Noorjahan", self.main_container)
        self.attribution_label.setGeometry(0, 616, 1117, 20)  # Position at bottom of container
        self.attribution_label.setAlignment(QtCore.Qt.AlignCenter)
        self.attribution_label.setStyleSheet("color: rgba(255, 255, 255, 150); font: 8pt 'Segoe UI'; background: transparent;")
        
        # Navigation frame with proper width
        frame_x = (1117 - 700) // 2  # Increased width to 700
        self.frame = QtWidgets.QFrame(self.main_container)
        self.frame.setGeometry(QtCore.QRect(frame_x, 60, 700, 61))
        self.frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 31, 40, 200),
                    stop:1 rgba(50, 51, 60, 180));
                border: 2px solid rgba(100, 150, 255, 100);
                border-radius: 25px;
            }
        """)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(15, 8, 15, 8)
        self.horizontalLayout.setSpacing(15)  # Increased spacing between buttons

        # Create buttons with proper sizing
        self.btn_dash = ModernButton("DASHBOARD", self.frame)
        self.btn_dash.setMinimumWidth(150)  # Increased width for DASHBOARD
        self.btn_dash.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(43, 87, 151, 180),
                    stop:0.5 rgba(64, 128, 255, 200),
                    stop:1 rgba(43, 87, 151, 180));
                border: 2px solid rgba(255, 255, 255, 30);
                border-radius: 15px;
                color: white;
                font: bold 11pt "Segoe UI";
                padding: 8px 20px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(64, 128, 255, 220),
                    stop:0.5 rgba(85, 149, 255, 240),
                    stop:1 rgba(64, 128, 255, 220));
                border: 2px solid rgba(255, 255, 255, 80);
            }
        """)
        self.horizontalLayout.addWidget(self.btn_dash)

        # Other buttons with consistent width
        button_width = 100
        self.btn_tyre = ModernButton("TYRE", self.frame)
        self.btn_tyre.setMinimumWidth(button_width)
        self.horizontalLayout.addWidget(self.btn_tyre)
        
        self.btn_ac = ModernButton("AC", self.frame)
        self.btn_ac.setMinimumWidth(button_width)
        self.horizontalLayout.addWidget(self.btn_ac)
        
        self.btn_music = ModernButton("MUSIC", self.frame)
        self.btn_music.setMinimumWidth(button_width)
        self.horizontalLayout.addWidget(self.btn_music)
        
        self.btn_map = ModernButton("MAP", self.frame)
        self.btn_map.setMinimumWidth(button_width)
        self.horizontalLayout.addWidget(self.btn_map)

        # Initialize all frames with proper visibility
        self.frame_dashboard = QtWidgets.QFrame(self.main_container)
        self.frame_dashboard.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_dashboard.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(34, 46, 61, 255), 
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_dashboard.setVisible(True)  # Make dashboard visible initially
        self.frame_dashboard.raise_()  # Ensure it's above background

        # Initialize tyre frame
        self.frame_tyre = QtWidgets.QFrame(self.main_container)
        self.frame_tyre.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_tyre.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(34, 46, 61, 255),
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_tyre.setVisible(False)

        # Initialize AC frame
        self.frame_AC = QtWidgets.QFrame(self.main_container)
        self.frame_AC.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_AC.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(34, 46, 61, 255),
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_AC.setVisible(False)

        # Initialize map frame
        self.frame_map = QtWidgets.QFrame(self.main_container)
        self.frame_map.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_map.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(34, 46, 61, 255),
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_map.setVisible(False)

        # Initialize music frame
        self.frame_music = QtWidgets.QFrame(self.main_container)
        self.frame_music.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_music.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(34, 46, 61, 255),
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_music.setVisible(False)

        # Speed gauge
        self.speed = AnalogGaugeWidget(self.frame_dashboard)
        self.speed.setGeometry(QtCore.QRect(30, 30, 311, 281))  # Changed Y from 50 to 30
        self.speed.setStyleSheet("background-color: transparent;\nborder-radius:0px;") 
        self.speed.setObjectName("speed")
        
        # RPM gauge
        self.rpm = AnalogGaugeWidget(self.frame_dashboard)
        self.rpm.setGeometry(QtCore.QRect(630, 30, 311, 281))  # Changed Y from 50 to 30
        self.rpm.setStyleSheet("background-color: transparent;\nborder-radius:0px;") 
        self.rpm.setObjectName("rpm")
        
        self.frame_2 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_2.setGeometry(QtCore.QRect(350, 30, 263, 38))
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color: rgba(85, 85, 127,80);\n"
"border-radius:15px;\n"
"}\n"
"\n"
"QLabel{\n"
"background:None;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 3, 0, 3)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMaximumSize(QtCore.QSize(40, 35))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(":/icon/steering.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setMaximumSize(QtCore.QSize(40, 35))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap(":/icon/702814.png"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_2.addWidget(self.label_13)
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setMaximumSize(QtCore.QSize(40, 35))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/icon/748151.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setMaximumSize(QtCore.QSize(40, 35))
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap(":/icon/1442194.png"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        
        self.frame_3 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_3.setGeometry(QtCore.QRect(370, 340, 240, 60))  # Increased width and height
        self.frame_3.setStyleSheet("background-color: rgba(85, 85, 127,80);\n"
"border-radius:15px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.date = QtWidgets.QLabel(self.frame_3)
        self.date.setGeometry(QtCore.QRect(10, 5, 220, 50))  # Adjusted position and height
        self.date.setStyleSheet("color:#fff;\n"
"font: 13pt \"MS UI Gothic\";\n"
"background:None;\n"
"padding-top: 5px;")  # Added padding to move text down slightly
        self.date.setAlignment(QtCore.Qt.AlignCenter)
        self.date.setWordWrap(True) 
        self.date.setObjectName("date")
        
        self.datetime_timer = QTimer(MainWindow)
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000) 
        self.update_datetime() 

        self.car_state = QtWidgets.QFrame(self.frame_dashboard)
        self.car_state.setGeometry(QtCore.QRect(350, 80, 271, 251))
        self.car_state.setStyleSheet("background:None;\n"
"color:#ee1111;")
        self.car_state.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.car_state.setFrameShadow(QtWidgets.QFrame.Raised)
        self.car_state.setObjectName("car_state")
        self.label_3 = QtWidgets.QLabel(self.car_state)
        self.label_3.setGeometry(QtCore.QRect(50, 10, 181, 231))
        self.label_3.setStyleSheet("background:None")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icon/car.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_7 = QtWidgets.QLabel(self.car_state)
        self.label_7.setGeometry(QtCore.QRect(200, 150, 41, 16))
        self.label_7.setObjectName("label_7")
        self.label_5 = QtWidgets.QLabel(self.car_state)
        self.label_5.setGeometry(QtCore.QRect(200, 110, 31, 16))
        self.label_5.setStyleSheet("color:green;")
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.car_state)
        self.label_4.setGeometry(QtCore.QRect(40, 110, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.car_state)
        self.label_8.setGeometry(QtCore.QRect(120, 50, 41, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.car_state)
        self.label_9.setGeometry(QtCore.QRect(120, 190, 55, 16))
        self.label_9.setStyleSheet("")
        self.label_9.setObjectName("label_9")
        self.label_6 = QtWidgets.QLabel(self.car_state)
        self.label_6.setGeometry(QtCore.QRect(40, 150, 41, 16))
        self.label_6.setObjectName("label_6")

        # Battery indicator frame
        self.frame_4 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_4.setGeometry(QtCore.QRect(690, 350, 190, 46))  # Changed Y from 370 to 350
        self.frame_4.setStyleSheet("""
            QFrame {
                background: none;
                border: none;
            }
        """)
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        
        # Create an inner frame to hold both components
        self.battery_container = QtWidgets.QFrame(self.frame_4)
        self.battery_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(15, 15, 25, 255),
                    stop:0.5 rgba(25, 25, 35, 255),
                    stop:1 rgba(15, 15, 25, 255));
                border-radius: 12px;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(25, 35, 45, 255),
                    stop:0.5 rgba(35, 45, 55, 255),
                    stop:1 rgba(25, 35, 45, 255));
            }
        """)
        
        # Create layout for the container with proper padding
        self.container_layout = QtWidgets.QHBoxLayout(self.battery_container)
        self.container_layout.setContentsMargins(10, 6, 10, 6)  # Adjusted vertical padding
        self.container_layout.setSpacing(8)
        
        # Battery label with improved visibility
        self.label_14 = QtWidgets.QLabel(self.battery_container)
        self.label_14.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255);
                font: bold 10pt 'Segoe UI';
                background: none;
                padding: 2px;
            }
        """)
        self.label_14.setFixedWidth(89)
        self.label_14.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.container_layout.addWidget(self.label_14)
        
        # Modern battery progress bar with border and glass effect
        self.battery_level = QtWidgets.QProgressBar(self.battery_container)
        self.battery_level.setFixedHeight(24)
        self.battery_level.setStyleSheet("""
            QProgressBar {
                background: rgba(40, 40, 40, 200);
                color: white;
               
                text-align: center;
                font: bold 8.5pt 'Segoe UI';
                margin: 0px;
                padding: 0px;
                border: 2px solid rgba(7, 170, 255, 200);
            }
            QProgressBar:hover {
                border: 2px solid rgba(0, 190, 255, 255);
            }
            QProgressBar::chunk {
                
                margin: 2px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(39, 174, 96, 255),
                    stop:0.5 rgba(241, 196, 15, 255),
                    stop:1 rgba(231, 76, 60, 255));
            }
        """)
        self.container_layout.addWidget(self.battery_level)
        
        # Add the container to the main layout
        self.horizontalLayout_3.addWidget(self.battery_container)
        
        # Add variables for car simulation
        self.current_speed = 0
        self.current_rpm = 0
        self.battery_percentage = 100
        self.acceleration = 0
        self.is_accelerating = False
        self.is_braking = False
        
        # Create timer for dynamic updates
        self.car_timer = QTimer()
        self.car_timer.timeout.connect(self.update_car_status)
        self.car_timer.start(100)  # Update every 100ms
        
        self.frame_5 = QtWidgets.QFrame(self.frame_dashboard)
        self.frame_5.setGeometry(QtCore.QRect(92, 350, 160, 44))  # Changed Y from 370 to 350
        self.frame_5.setStyleSheet("background: rgba(30, 31, 40, 120); border-radius:15px;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.door_toggle_btn = InteractiveToggleButton("Unlock Door", self.frame_5)
        self.door_toggle_btn.setMinimumSize(140, 35) 
        self.door_toggle_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(152, 57, 38, 180),
                    stop:1 rgba(180, 70, 50, 200));
                border: 2px solid rgba(255, 100, 100, 150);
                border-radius: 17px;
                color: white;
                font: bold 10pt "Segoe UI"; 
                padding: 6px 8px; 
                min-width: 135px; 
                text-align: center; 
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(172, 77, 58, 220),
                    stop:1 rgba(200, 90, 70, 240));
                border: 2px solid rgba(255, 120, 120, 200);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(50, 150, 50, 220),
                    stop:1 rgba(80, 180, 80, 240));
                border: 2px solid rgba(100, 255, 100, 200);
            }
            QPushButton:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(70, 170, 70, 240),
                    stop:1 rgba(100, 200, 100, 255));
                border: 2px solid rgba(120, 255, 120, 220);
            }
        """)
        self.horizontalLayout_4.addWidget(self.door_toggle_btn) 
        self.horizontalLayout_4.setContentsMargins(5, 3, 5, 3) 
        self.door_status = "Locked"
        
        self.frame_AC = QtWidgets.QFrame(self.main_container)
        self.frame_AC.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_AC.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(34, 46, 61, 255), 
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        
        # Create outdoor temperature circle (right side)
        self.circularProgressCPU = QtWidgets.QFrame(self.frame_AC)
        self.circularProgressCPU.setGeometry(QtCore.QRect(700, 80, 220, 220))
        self.circularProgressCPU.setStyleSheet("""
            QFrame {
                border-radius: 110px;    
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, 
                    stop:0.68 rgba(85, 170, 255, 255), 
                    stop:0.612 rgba(255, 255, 255, 0));
            }
        """)
        
        self.circularOutdoor = QtWidgets.QFrame(self.circularProgressCPU)
        self.circularOutdoor.setGeometry(QtCore.QRect(15, 15, 190, 190))
        self.circularOutdoor.setStyleSheet("""
            QFrame {
                border-radius: 95px;    
                background-color: rgb(58, 58, 102);
            }
        """)

        # Create indoor temperature circle (left side)
        self.circularIndoor = QtWidgets.QFrame(self.frame_AC)
        self.circularIndoor.setGeometry(QtCore.QRect(50, 80, 220, 220))
        self.circularIndoor.setStyleSheet("""
            QFrame {
                border-radius: 110px;    
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, 
                    stop:0.88 rgba(255,196,13,255), 
                    stop:0.712 rgba(255, 255, 255, 0));
            }
        """)
        
        self.circularInner = QtWidgets.QFrame(self.circularIndoor)
        self.circularInner.setGeometry(QtCore.QRect(15, 15, 190, 190))
        self.circularInner.setStyleSheet("""
            QFrame {
                border-radius: 95px;    
                background-color: rgb(43,87,151);
            }
        """)

        # Indoor temperature display
        self.labelIndoorTemp = QtWidgets.QLabel(self.circularInner)
        self.labelIndoorTemp.setGeometry(QtCore.QRect(30, 95, 132, 60))  # Reduced height and moved down
        self.labelIndoorTemp.setStyleSheet("""
            color: rgb(115, 185, 255);
            font: bold 26pt 'Segoe UI';  /* Slightly smaller font */
            background: none;
            padding: 0px;
            margin: 0px;
        """)
        self.labelIndoorTemp.setAlignment(QtCore.Qt.AlignCenter)
        self.labelIndoorTemp.setText("20°C")
        
        # Indoor label text
        self.labelIndoorText = QtWidgets.QLabel(self.circularInner)
        self.labelIndoorText.setGeometry(QtCore.QRect(30, 20, 132, 70))  # More height, moved up more
        self.labelIndoorText.setStyleSheet("""
            QLabel {
                background: None;
                color: rgba(255, 255, 255, 180);
                font: bold 9.5pt 'Segoe UI';  /* Slightly smaller font */
                padding: 0px;
                margin: 0px;
                letter-spacing: 0.5px;
            }
        """)
        self.labelIndoorText.setAlignment(QtCore.Qt.AlignCenter)
        self.labelIndoorText.setWordWrap(True)  # Enable word wrap
        self.labelIndoorText.setText("Indoor\nTemperature")

        # Outdoor temperature display
        self.labelOutdoorTemp = QtWidgets.QLabel(self.circularOutdoor)
        self.labelOutdoorTemp.setGeometry(QtCore.QRect(30, 95, 132, 60))  # Reduced height and moved down
        self.labelOutdoorTemp.setStyleSheet("""
            color: rgb(115, 185, 255);
            font: bold 22pt 'Segoe UI';  /* Reduced from 26pt to 22pt */
            background: none;
            padding: 0px;
            margin: 0px;
        """)
        self.labelOutdoorTemp.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOutdoorTemp.setText("29°C")
        
        # Outdoor label text
        self.labelOutdoorText = QtWidgets.QLabel(self.circularOutdoor)
        self.labelOutdoorText.setGeometry(QtCore.QRect(30, 20, 132, 70))  # More height, moved up more
        self.labelOutdoorText.setStyleSheet("""
            QLabel {
                background: None;
                color: rgba(255, 255, 255, 180);
                font: bold 9.5pt 'Segoe UI';  /* Slightly smaller font */
                padding: 0px;
                margin: 0px;
                letter-spacing: 0.5px;
            }
        """)
        self.labelOutdoorText.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOutdoorText.setWordWrap(True)  # Enable word wrap
        self.labelOutdoorText.setText("Outdoor\nTemperature")
        
        self.weather = QtWidgets.QFrame(self.frame_AC)
        self.weather.setGeometry(QtCore.QRect(330, 10, 341, 351))
        self.weather.setStyleSheet("QFrame{\n"
"border-radius:5px;\n"
"background-color: rgb(14, 22, 39);\n"
"}")
        self.weather.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.weather.setFrameShadow(QtWidgets.QFrame.Raised)
        self.weather.setObjectName("weather")
        self.label_18 = QtWidgets.QLabel(self.weather)
        self.label_18.setGeometry(QtCore.QRect(50, 10, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("QLabel\n"
"{\n"
"background:None;\n"
"color:rgb(227,162,26);\n"
"}")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2 = QtWidgets.QLabel(self.weather)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 101, 81))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/p.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_17 = QtWidgets.QLabel(self.weather)
        self.label_17.setGeometry(QtCore.QRect(210, 60, 121, 81))
        self.label_17.setStyleSheet("color:#fff")
        self.label_17.setWordWrap(True) 
        self.label_17.setAlignment(Qt.AlignLeft | Qt.AlignTop) 
        self.label_17.setObjectName("label_17")
        self.frame_6 = QtWidgets.QFrame(self.weather)
        self.frame_6.setGeometry(QtCore.QRect(30, 250, 281, 81))
        self.frame_6.setStyleSheet("color:#fff;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(30)
        self.gridLayout.setVerticalSpacing(11)
        self.gridLayout.setObjectName("gridLayout")
        self.label_24 = QtWidgets.QLabel(self.frame_6)
        self.label_24.setText("")
        self.label_24.setPixmap(QtGui.QPixmap(":/bg/289759.png"))
        self.label_24.setScaledContents(True)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 0, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.frame_6)
        self.label_23.setText("")
        self.label_23.setPixmap(QtGui.QPixmap(":/icons/95252.png"))
        self.label_23.setScaledContents(True)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 0, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setStyleSheet("")
        self.label_22.setText("")
        self.label_22.setPixmap(QtGui.QPixmap(":/icons/567255.png"))
        self.label_22.setScaledContents(True)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 0, 0, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.frame_6)
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 1, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.frame_6)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 1, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.frame_6)
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 1, 2, 1, 1)
        self.labelPercentageCPU_4 = QtWidgets.QLabel(self.weather) 
        self.labelPercentageCPU_4.setGeometry(QtCore.QRect(110, 80, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto Thin")
        font.setPointSize(13)
        self.labelPercentageCPU_4.setFont(font)
        self.labelPercentageCPU_4.setStyleSheet("color: rgba(115, 185, 255, 70);\n"
"padding: 0px;\n"
" background-color: none;")
        self.labelPercentageCPU_4.setAlignment(QtCore.Qt.AlignCenter) 
        self.labelPercentageCPU_4.setIndent(-1)
        self.labelPercentageCPU_4.setObjectName("labelPercentageCPU_4")
        self.line = QtWidgets.QFrame(self.weather)
        self.line.setGeometry(QtCore.QRect(194, 81, 3, 40))
        self.line.setStyleSheet("background-color: rgba(85, 85, 255,120);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.checked =AnimatedToggle(self.frame_AC)
        self.checked.setGeometry(QtCore.QRect(140, 310, 120, 50)) 
        
        self.frame_music = QtWidgets.QFrame(self.main_container)
        self.frame_music.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_music.setStyleSheet("QFrame{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(34, 46, 61, 255), stop:1 rgba(34, 34, 47, 255));\n" # Corrected
"\n"
"border-radius:200px;\n"
"\n"
"}")
        self.frame_music.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_music.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_music.setObjectName("frame_music")
        
        self.dial = QtWidgets.QDial(self.frame_music)
        self.dial.setGeometry(QtCore.QRect(40, 100, 220, 220))
        self.dial.setProperty("value", 16)
        self.dial.setInvertedAppearance(False)
        self.dial.setInvertedControls(False)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(False)
        self.dial.setObjectName("dial")
        self.dial.valueChanged.connect(self.change_volume)
        
        self.horizontalSlider = QtWidgets.QSlider(self.frame_music)
        self.horizontalSlider.setGeometry(QtCore.QRect(150, 360, 651, 21))
        self.horizontalSlider.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"background-color: rgb(31, 119, 180);\n"
"height: 20px;\n"
"\n"
"border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    width: 20px;\n"
"    background-image: url(:/icon/pin.png);\n"
"}\n"
"\n"
"QSlider::add-page:qlineargradient {\n"
"background: lightgrey;\n"
"border-top-right-radius: 9px;\n"
"border-bottom-right-radius: 9px;\n"
"border-top-left-radius: 0px;\n"
"border-bottom-left-radius: 0px;\n"
"}\n"
"\n"
"")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 35)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        
        self.dial_2 = QtWidgets.QDial(self.frame_music)
        self.dial_2.setGeometry(QtCore.QRect(730, 100, 220, 220))
        self.dial_2.setProperty("value", 55)
        self.dial_2.setInvertedAppearance(False)
        self.dial_2.setInvertedControls(False)
        self.dial_2.setWrapping(False)
        self.dial_2.setNotchesVisible(False)
        self.dial_2.setObjectName("dial_2")
        
        self.label_20 = QtWidgets.QLabel(self.frame_music)
        self.label_20.setGeometry(QtCore.QRect(100, 80, 91, 31))
        self.label_20.setStyleSheet("color: rgb(23, 190, 207);\n"
"font: 75 12pt \"Nirmala UI\";\n"
"background:None;")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.label_28 = QtWidgets.QLabel(self.frame_music)
        self.label_28.setGeometry(QtCore.QRect(780, 80, 120, 31)) 
        self.label_28.setStyleSheet("color: rgb(23, 190, 207);\n"
"font: 75 12pt \"Nirmala UI\";\n"
"background:None;")
        self.label_28.setAlignment(QtCore.Qt.AlignCenter) 
        self.label_28.setObjectName("label_28")
        
        self.label_29 = QtWidgets.QLabel(self.frame_music)
        self.label_29.setGeometry(QtCore.QRect(400, 80, 161, 161))
        self.label_29.setStyleSheet("background:None;")
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap(":/music/music.png"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        
        # Music control buttons with proper alignment
        self.btn_prev = GlowingMusicButton(self.frame_music)
        self.btn_prev.setGeometry(QtCore.QRect(420, 310, 35, 35))
        self.btn_prev.setText("")
        self.btn_prev.setIcon(QtGui.QIcon(":/music/3.png"))
        self.btn_prev.setObjectName("btn_prev")
        self.btn_prev.clicked.connect(self.previous_track)
        
        self.btn_play_pause = GlowingMusicButton(self.frame_music)
        self.btn_play_pause.setGeometry(QtCore.QRect(465, 305, 45, 45))
        self.btn_play_pause.setText("")
        self.btn_play_pause.setIcon(QtGui.QIcon(":/music/151859.png"))
        self.btn_play_pause.setObjectName("btn_play_pause")
        self.btn_play_pause.clicked.connect(self.toggle_play_pause)
        
        self.btn_next = GlowingMusicButton(self.frame_music)
        self.btn_next.setGeometry(QtCore.QRect(520, 310, 35, 35))
        self.btn_next.setText("")
        self.btn_next.setIcon(QtGui.QIcon(":/music/2.png"))
        self.btn_next.setObjectName("btn_next")
        self.btn_next.clicked.connect(self.next_track)
        
        # Update the music controls styling to ensure consistent appearance
        music_controls_style = """
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 200),
                    stop:0.3 rgba(64, 128, 255, 180),
                    stop:1 rgba(43, 87, 151, 160));
                border: 2px solid rgba(100, 200, 255, 150);
                border-radius: 17px;
                padding: 5px;
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(255, 255, 255, 240),
                    stop:0.3 rgba(84, 148, 255, 200),
                    stop:1 rgba(63, 107, 171, 180));
                border: 2px solid rgba(150, 250, 255, 200);
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(200, 200, 200, 180),
                    stop:0.3 rgba(44, 88, 155, 160),
                    stop:1 rgba(23, 67, 131, 140));
                border: 2px solid rgba(80, 180, 255, 120);
            }
        """
        self.btn_prev.setStyleSheet(music_controls_style)
        self.btn_play_pause.setStyleSheet(music_controls_style)
        self.btn_next.setStyleSheet(music_controls_style)
        
        # Set consistent icon sizes
        icon_size = QtCore.QSize(20, 20)
        self.btn_prev.setIconSize(icon_size)
        self.btn_play_pause.setIconSize(QtCore.QSize(25, 25))
        self.btn_next.setIconSize(icon_size)
        
        self.btn_browse_music = ModernButton("Browse Music", self.frame_music)
        self.btn_browse_music.setGeometry(QtCore.QRect(40, 20, 200, 45))
        self.btn_browse_music.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(65, 105, 225, 180),
                    stop:0.5 rgba(100, 149, 237, 200),
                    stop:1 rgba(65, 105, 225, 180));
                border: 2px solid rgba(100, 200, 255, 100);
                border-radius: 22px;
                color: rgb(0, 255, 255);
                font: bold 14pt "Segoe UI";
                padding: 8px 16px;
                min-width: 180px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85, 125, 245, 220),
                    stop:0.5 rgba(120, 169, 255, 240),
                    stop:1 rgba(85, 125, 245, 220));
                border: 2px solid rgba(150, 220, 255, 150);
                color: rgb(150, 255, 255);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(55, 85, 205, 200),
                    stop:0.5 rgba(80, 129, 217, 220),
                    stop:1 rgba(55, 85, 205, 200));
                border: 2px solid rgba(100, 200, 255, 100);
                color: rgb(0, 200, 200);
            }
        """)
        
        # Add glow effect to the button
        glow = QtWidgets.QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(0, 200, 255, 160))
        glow.setOffset(0, 0)
        self.btn_browse_music.setGraphicsEffect(glow)
        self.btn_browse_music.clicked.connect(self.browse_music_files)
        
        self.label_33 = QtWidgets.QLabel(self.frame_music)
        self.label_33.setGeometry(QtCore.QRect(260, 260, 481, 31))
        self.label_33.setStyleSheet("color: rgb(23, 190, 207);\n"
"font: 75 12pt \"Nirmala UI\";\n"
"background:None;")
        self.label_33.setAlignment(QtCore.Qt.AlignCenter)
        self.label_33.setObjectName("label_33")
        
        self.frame_map = QtWidgets.QFrame(self.main_container)
        self.frame_map.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_map.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(34, 46, 61, 255), stop:1 rgba(34, 34, 47, 255)); /* Corrected */
                border-radius: 200px;
            }
        """)
        
        self.mode_toggle = QCheckBox("Light Mode", self.main_container)
        self.mode_toggle.setGeometry(10, 10, 150, 40)
        self.mode_toggle.setStyleSheet("""
            QCheckBox {
                color: white; 
                font: bold 10pt 'Segoe UI';
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid rgba(100, 150, 255, 150);
                background: rgba(30, 31, 40, 200);
            }
            QCheckBox::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(100, 200, 255, 255),
                    stop:1 rgba(50, 150, 255, 200));
                border: 2px solid rgba(150, 200, 255, 200);
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(150, 200, 255, 200);
            }
        """)
        self.mode_toggle.stateChanged.connect(self.toggle_mode)

        self.frame_map.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_map.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_map.setObjectName("frame_map")

        self.map_plot = QWebEngineView(self.frame_map)
        self.map_plot.setObjectName("map_plot")
        self.map_plot.setGeometry(QRect(30, 75, 521, 296))  # Moved down and adjusted height
        
        self.webcam = QLabel(self.frame_map)
        self.webcam.setObjectName("webcam")
        self.webcam.setGeometry(QRect(570, 75, 371, 246))  # Moved down to align with map
        self.webcam.setStyleSheet("""
            border: 3px solid rgba(0,171,169,120); 
            border-radius: 15px;
            background: rgba(20, 25, 35, 150);
            color: rgba(0,171,169,200);
            font: bold 14pt 'Segoe UI';
            text-align: center;
        """)
        self.webcam.setAlignment(Qt.AlignCenter)
        
        self.control_panel = QtWidgets.QFrame(self.frame_map)
        self.control_panel.setGeometry(QtCore.QRect(570, 335, 371, 50))  # Adjusted y position
        self.control_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85, 85, 127, 150),
                    stop:1 rgba(65, 65, 107, 130)); 
                border: 2px solid rgba(100, 200, 255, 150);
                border-radius: 20px;
            }
        """)
        
        self.control_layout = QtWidgets.QHBoxLayout(self.control_panel)
        self.control_layout.setContentsMargins(10, 5, 10, 5) 
        self.control_layout.setSpacing(15) 
        
        self.btn_get_location = ModernControlButton("Get Location", self.control_panel)
        self.btn_get_location.setMinimumWidth(120)
        self.btn_get_location.clicked.connect(self.get_current_location)
        self.control_layout.addWidget(self.btn_get_location)
        
        self.btn_camera_toggle = ModernControlButton("Start Camera", self.control_panel)
        self.btn_camera_toggle.setMinimumWidth(120)
        self.btn_camera_toggle.clicked.connect(self.controlTimer)
        self.control_layout.addWidget(self.btn_camera_toggle)
        
        # Create destination UI elements
        self.destination_frame = QtWidgets.QFrame(self.frame_map)
        self.destination_frame.setGeometry(QtCore.QRect(30, 10, 521, 50))
        self.destination_frame.setStyleSheet("""
            QFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85, 85, 127, 150),
                    stop:1 rgba(65, 65, 107, 130)); 
                border: 2px solid rgba(100, 200, 255, 150);
                border-radius: 20px;
            }
        """)
        
        self.dest_layout = QtWidgets.QHBoxLayout(self.destination_frame)
        self.dest_layout.setContentsMargins(15, 0, 15, 0)
        self.dest_layout.setSpacing(10)
        
        self.destination_input = QLineEdit(self.destination_frame)
        self.destination_input.setPlaceholderText("Enter destination (e.g., Bangalore)")
        self.destination_input.setStyleSheet("""
            QLineEdit {
                background: rgba(30, 35, 45, 200);
                border: 2px solid rgba(100, 150, 255, 120); 
                border-radius: 15px; 
                color: white;
                padding: 0px 15px; 
                font: 11pt 'Segoe UI'; 
                min-height: 35px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(150, 200, 255, 200);
                background: rgba(40, 45, 55, 220);
            }
            QLineEdit::placeholder {
                color: rgba(200, 200, 200, 150);
                font: italic 11pt 'Segoe UI';
            }
        """)
        self.destination_input.setMinimumWidth(380)
        self.dest_layout.addWidget(self.destination_input)
        
        self.btn_set_destination = ModernControlButton("Set", self.destination_frame)
        self.btn_set_destination.setFixedSize(70, 35)
        self.btn_set_destination.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(0, 171, 169, 200),
                    stop:0.7 rgba(0, 151, 149, 180),
                    stop:1 rgba(0, 131, 129, 160));
                border: 2px solid rgba(0, 255, 253, 120);
                border-radius: 15px;
                color: white;
                font: bold 10pt "Segoe UI";
                padding: 0px;
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 rgba(20, 191, 189, 220),
                    stop:0.7 rgba(20, 171, 169, 200),
                    stop:1 rgba(20, 151, 149, 180));
                border: 2px solid rgba(50, 255, 253, 150);
            }
        """)
        self.dest_layout.addWidget(self.btn_set_destination)
        
        # Connect the Set button to the destination setting function
        self.btn_set_destination.clicked.connect(self.set_destination_from_input)
        
        # Initialize destination-related variables
        self.destination = None
        self.destination_name = None
        
        # Update the map initially
        self.update_map()
        
        # Make sure the map is properly initialized with current location
        self.current_location = [15.3647, 75.1240]  # Default to KLE Tech University
        
        # Improved current location display with larger size
        self.location_display = QtWidgets.QLabel(self.frame_map)
        self.location_display.setGeometry(QtCore.QRect(570, 15, 371, 48))
        self.location_display.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255); 
                font: bold 10pt 'Segoe UI'; 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85, 85, 127, 180),
                    stop:1 rgba(65, 65, 107, 160)); 
                border: 2px solid rgba(0, 255, 255, 150);
                border-radius: 24px; 
                padding: 0 20px;
                qproperty-alignment: AlignCenter;
            }
        """)
        self.location_display.setText("Current: KLE Tech University, Hubli")
        
        # Initialize camera-related variables
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.cap = None

        # Connect resize event to reposition attribution label
        MainWindow.resizeEvent = self.resize_main_window_elements

        self.show_Dash()
        self.progress()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.label_km = QLabel(self.speed) 
        self.label_km.setText("Km/h")
        self.label_km.setGeometry(QRect(130, 150, 50, 20))
        self.label_km.setStyleSheet("""
            color: #fff;
            font: bold 10pt 'Segoe UI';
            background: None;
            padding: 1px;
        """)
        self.label_km.setAlignment(Qt.AlignCenter)
        self.label_km.raise_()  # Bring label to front

        # Modify road animation frame to be vertical and wider
        self.road_frame = QtWidgets.QFrame(self.frame_dashboard)
        self.road_frame.setGeometry(QtCore.QRect(350, 80, 271, 251))
        self.road_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 20, 20, 255),
                    stop:0.5 rgba(40, 40, 40, 255),
                    stop:1 rgba(20, 20, 20, 255));
                border-radius: 15px;
            }
        """)
        
        # Modify road markers for vertical orientation - Create BEFORE car
        self.road_markers = []
        marker_spacing = 35  # Consistent spacing between markers
        marker_height = 15   # Slightly taller markers
        num_markers = 6      # Reduced number for better spacing
        
        for i in range(num_markers):
            marker = QtWidgets.QLabel(self.road_frame)
            y_pos = 20 + i * (marker_spacing + marker_height)  # Space between markers plus marker height
            marker.setGeometry(QtCore.QRect(115, y_pos, 40, marker_height))
            marker.setStyleSheet("""
                background-color: rgba(255, 255, 255, 220);
                border-radius: 4px;
            """)
            self.road_markers.append(marker)
            marker.lower()  # Make sure markers stay behind car
        
        # Update marker positions array for vertical movement
        self.marker_positions = []
        for i in range(num_markers):
            self.marker_positions.append(20 + i * (marker_spacing + marker_height))
        
        # Add car overlay AFTER creating markers
        self.car_overlay = QtWidgets.QLabel(self.road_frame)
        self.car_overlay.setGeometry(QtCore.QRect(85, 120, 100, 120))  # Increased size and adjusted position
        self.car_overlay.setStyleSheet("""
            QLabel {
                background: none;  # Remove background color
                border: none;
            }
        """)
        
        # Using an existing car icon and applying color overlay
        original_pixmap = QtGui.QPixmap(":/icon/car.png")
        # Create a new pixmap with the desired size
        scaled_pixmap = original_pixmap.scaled(100, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Create a new pixmap with transparency
        colored_pixmap = QtGui.QPixmap(scaled_pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        
        # Create painter for the new pixmap
        painter = QtGui.QPainter(colored_pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Draw the original image
        painter.drawPixmap(0, 0, scaled_pixmap)
        
        # Apply color overlay only to non-transparent pixels
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceAtop)
        gradient = QLinearGradient(0, 0, colored_pixmap.width(), 0)
        gradient.setColorAt(0, QColor(30, 144, 255, 255))  # Royal Blue
        gradient.setColorAt(0.5, QColor(65, 105, 225, 255))  # Royal Blue, slightly darker
        gradient.setColorAt(1, QColor(30, 144, 255, 255))  # Royal Blue
        painter.fillRect(colored_pixmap.rect(), gradient)
        
        painter.end()
        
        self.car_overlay.setPixmap(colored_pixmap)
        self.car_overlay.setScaledContents(True)
        
        # Add a more pronounced glow effect to the car
        glow_effect = QtWidgets.QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(15)  # Slightly reduced blur for sharper appearance
        glow_effect.setColor(QtGui.QColor(65, 105, 225, 180))  # Matching blue color with transparency
        glow_effect.setOffset(0, 0)
        self.car_overlay.setGraphicsEffect(glow_effect)
        
        self.car_overlay.raise_()  # Ensure car stays on top
        
        # Gear indicator frame - positioned below speedometer
        self.gear_frame = QtWidgets.QFrame(self.frame_dashboard)
        self.gear_frame.setGeometry(QtCore.QRect(150, 310, 60, 35))  # Changed Y from 310 to 290
        self.gear_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 30, 200);
                border-radius: 8px;
                border: 2px solid rgba(100, 150, 255, 150);
            }
        """)
        
        # Add gear label - adjusted size
        self.gear_label = QtWidgets.QLabel(self.gear_frame)
        self.gear_label.setGeometry(QtCore.QRect(0, 0, 60, 35))
        self.gear_label.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255);
                font: bold 12pt 'Segoe UI';
                background: none;
            }
        """)
        self.gear_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gear_label.setText("P")
        
        # Add driving mode indicator - positioned below RPM gauge
        self.mode_frame = QtWidgets.QFrame(self.frame_dashboard)
        self.mode_frame.setGeometry(QtCore.QRect(730, 310, 120, 35))  # Changed Y from 310 to 290
        self.mode_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 30, 200);
                border-radius: 8px;
                border: 2px solid rgba(100, 150, 255, 150);
            }
        """)
        
        self.mode_label = QtWidgets.QLabel(self.mode_frame)
        self.mode_label.setGeometry(QtCore.QRect(0, 0, 120, 35))
        self.mode_label.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255);
                font: bold 12pt 'Segoe UI';
                background: none;
                padding: 0 5px;
            }
        """)
        self.mode_label.setAlignment(QtCore.Qt.AlignCenter)
        self.mode_label.setText("ECO")

        # Create tyre monitoring section with modern design
        self.frame_tyre = QtWidgets.QFrame(self.main_container)
        self.frame_tyre.setGeometry(QtCore.QRect((MainWindow.width() - 971) // 2, 120, 971, 411))
        self.frame_tyre.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(34, 46, 61, 255),
                    stop:1 rgba(34, 34, 47, 255));
                border-radius: 200px;
            }
        """)
        self.frame_tyre.setVisible(False)

        # Add title with modern styling
        self.tyre_title = QtWidgets.QLabel(self.frame_tyre)
        self.tyre_title.setGeometry(QtCore.QRect(0, 20, 971, 40))
        self.tyre_title.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255);
                font: bold 16pt 'Segoe UI';
                background: none;
                letter-spacing: 1px;
            }
        """)
        self.tyre_title.setAlignment(QtCore.Qt.AlignCenter)
        self.tyre_title.setText("Tyre Pressure and Temperature Monitoring")

        # Create modern background for car display
        self.car_container = QtWidgets.QFrame(self.frame_tyre)
        self.car_container.setGeometry(QtCore.QRect(335, 100, 300, 250))
        self.car_container.setStyleSheet("""
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(0, 171, 169, 30),
                    stop:0.8 rgba(0, 171, 169, 15),
                    stop:1 rgba(0, 171, 169, 0));
                border: 2px solid rgba(0, 171, 169, 50);
                border-radius: 20px;
            }
        """)

        # Add car image with proper scaling
        self.car_image = QtWidgets.QLabel(self.car_container)
        self.car_image.setGeometry(QtCore.QRect(50, 10, 200, 250))
        self.car_image.setStyleSheet("background: none;")
        self.car_image.setPixmap(QtGui.QPixmap(":/icon/car.png"))
        self.car_image.setScaledContents(True)

        # Add glow effect to car
        car_glow = QtWidgets.QGraphicsDropShadowEffect()
        car_glow.setBlurRadius(20)
        car_glow.setColor(QtGui.QColor(0, 255, 255, 160))
        car_glow.setOffset(0, 0)
        self.car_image.setGraphicsEffect(car_glow)

        # Create tyre indicators with proper positioning
        positions = {
            "FL": {"x": 185, "y": 110, "title": "Front Left"},
            "FR": {"x": 685, "y": 110, "title": "Front Right"},
            "RL": {"x": 185, "y": 240, "title": "Rear Left"},
            "RR": {"x": 685, "y": 240, "title": "Rear Right"}
        }

        for pos, data in positions.items():
            self.create_tyre_indicator(pos, data["x"], data["y"], data["title"])

        # Create connecting lines with animation
        self.create_connection_lines()

        # Initialize tyre monitoring variables with realistic starting values
        self.tyre_data = {
            'FL': {'pressure': 32.0, 'temp': 35.0, 'last_update': 0},
            'FR': {'pressure': 32.0, 'temp': 35.0, 'last_update': 0},
            'RL': {'pressure': 32.0, 'temp': 35.0, 'last_update': 0},
            'RR': {'pressure': 32.0, 'temp': 35.0, 'last_update': 0}
        }

        # Create timer for tyre data updates
        self.tyre_timer = QTimer()
        self.tyre_timer.timeout.connect(self.update_tyre_data)
        self.tyre_timer.start(1000)  # Update every second

        # Add simulation variables
        self.ambient_temp = 25.0  # Ambient temperature in Celsius
        self.driving_condition = "normal"  # Can be "normal", "aggressive", "highway"

        # Replace AC toggle with temperature controls
        self.temp_control_frame = QtWidgets.QFrame(self.frame_AC)
        self.temp_control_frame.setGeometry(QtCore.QRect(60, 310, 240, 60))
        self.temp_control_frame.setStyleSheet("""
            QFrame {
                background: rgba(0, 20, 40, 180);
                border: 2px solid rgba(0, 200, 255, 40);
                border-radius: 30px;
            }
        """)

        # Create horizontal layout for temperature controls
        self.temp_control_layout = QtWidgets.QHBoxLayout(self.temp_control_frame)
        self.temp_control_layout.setContentsMargins(10, 5, 10, 5)
        self.temp_control_layout.setSpacing(10)

        # Decrease temperature button
        self.btn_temp_down = QPushButton("-", self.temp_control_frame)
        self.btn_temp_down.setFixedSize(40, 40)
        self.btn_temp_down.setStyleSheet("""
            QPushButton {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(0, 171, 169, 200),
                    stop:0.8 rgba(0, 151, 149, 180),
                    stop:1 rgba(0, 131, 129, 160));
                border: 2px solid rgba(0, 255, 253, 100);
                border-radius: 20px;
                color: white;
                font: bold 20pt "Segoe UI";
            }
            QPushButton:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(0, 191, 189, 220),
                    stop:0.8 rgba(0, 171, 169, 200),
                    stop:1 rgba(0, 151, 149, 180));
                border: 2px solid rgba(50, 255, 253, 150);
            }
            QPushButton:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    stop:0 rgba(0, 151, 149, 180),
                    stop:0.8 rgba(0, 131, 129, 160),
                    stop:1 rgba(0, 111, 109, 140));
            }
        """)
        self.temp_control_layout.addWidget(self.btn_temp_down)

        # Temperature display
        self.temp_display = QLabel("20°C", self.temp_control_frame)
        self.temp_display.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 255);
                font: bold 14pt "Segoe UI";
                background: none;
            }
        """)
        self.temp_display.setAlignment(Qt.AlignCenter)
        self.temp_control_layout.addWidget(self.temp_display)

        # Increase temperature button
        self.btn_temp_up = QPushButton("+", self.temp_control_frame)
        self.btn_temp_up.setFixedSize(40, 40)
        self.btn_temp_up.setStyleSheet(self.btn_temp_down.styleSheet())
        self.temp_control_layout.addWidget(self.btn_temp_up)

        # Initialize temperature value
        self.current_temp = 20
        self.min_temp = 16
        self.max_temp = 30

        # Connect buttons to temperature adjustment functions
        self.btn_temp_up.clicked.connect(self.increase_temperature)
        self.btn_temp_down.clicked.connect(self.decrease_temperature)

        # Remove the old AC toggle reference
        if hasattr(self, 'checked'):
            self.checked.deleteLater()
            delattr(self, 'checked')

        # Initialize weather variables
        self.outdoor_temp = 29.0
        self.weather_conditions = ["Clear", "Cloudy", "Rainy", "Partly Cloudy"]
        self.current_weather = "Cloudy"
        self.humidity = 70
        self.wind_speed = 32
        self.precipitation = 20
        
        # Create timer for weather updates
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(30000)  # Update every 30 seconds

    def create_tyre_indicator(self, position, x, y, title):
        """Create modern tyre indicator matching the reference design"""
        # Main frame without borders
        frame = QtWidgets.QFrame(self.frame_tyre)
        frame.setGeometry(QtCore.QRect(x, y, 180, 120))  # Increased height and width for warning message
        frame.setStyleSheet("background: none;")

        # Title text with warning LED
        title_container = QtWidgets.QFrame(frame)
        title_container.setGeometry(QtCore.QRect(0, 5, 180, 25))
        title_container.setStyleSheet("background: none;")
        
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: rgb(0, 255, 255); font: bold 12pt 'Segoe UI'; background: none;")
        title_layout.addWidget(title_label)
        
        # Add warning LED
        warning_led = QtWidgets.QLabel()
        warning_led.setFixedSize(12, 12)
        warning_led.setStyleSheet("background-color: rgb(0, 255, 127); border-radius: 6px; border: 1px solid rgb(100, 255, 150);")
        title_layout.addWidget(warning_led)
        title_layout.addStretch()
        
        # Store warning LED reference
        setattr(self, f'warning_led_{position}', warning_led)

        # Warning message label
        warning_label = QtWidgets.QLabel("")
        warning_label.setGeometry(QtCore.QRect(0, 90, 180, 25))
        warning_label.setStyleSheet("color: rgb(255, 255, 0); font: bold 9pt 'Segoe UI'; background: none;")
        warning_label.setWordWrap(True)
        warning_label.setAlignment(Qt.AlignLeft)
        warning_label.setParent(frame)
        setattr(self, f'warning_label_{position}', warning_label)

        # Pressure display
        pressure_container = QtWidgets.QFrame(frame)
        pressure_container.setGeometry(QtCore.QRect(0, 32, 180, 25))
        pressure_container.setStyleSheet("background: none;")

        pressure_layout = QtWidgets.QHBoxLayout(pressure_container)
        pressure_layout.setContentsMargins(0, 0, 0, 0)
        pressure_layout.setSpacing(5)

        pressure_value = QtWidgets.QLabel("36.0")
        pressure_value.setStyleSheet("color: rgb(255, 255, 0); font: bold 14pt 'Segoe UI'; background: none;")
        pressure_value.setObjectName(f"pressure_label_{position}")  # Set object name for identification
        pressure_layout.addWidget(pressure_value)
        setattr(self, f'pressure_label_{position}', pressure_value)

        pressure_unit = QtWidgets.QLabel("PSI")
        pressure_unit.setStyleSheet("color: rgb(0, 255, 255); font: bold 11pt 'Segoe UI'; background: none;")
        pressure_layout.addWidget(pressure_unit)
        pressure_layout.addStretch()

        # Temperature display
        temp_container = QtWidgets.QFrame(frame)
        temp_container.setGeometry(QtCore.QRect(0, 60, 180, 25))
        temp_container.setStyleSheet("background: none;")

        temp_layout = QtWidgets.QHBoxLayout(temp_container)
        temp_layout.setContentsMargins(0, 0, 0, 0)
        temp_layout.setSpacing(5)

        temp_value = QtWidgets.QLabel("25.0")
        temp_value.setStyleSheet("color: rgb(255, 255, 0); font: bold 14pt 'Segoe UI'; background: none;")
        temp_value.setObjectName(f"temp_label_{position}")  # Set object name for identification
        temp_layout.addWidget(temp_value)
        setattr(self, f'temp_label_{position}', temp_value)

        temp_unit = QtWidgets.QLabel("°C")
        temp_unit.setStyleSheet("color: rgb(0, 255, 255); font: bold 11pt 'Segoe UI'; background: none;")
        temp_layout.addWidget(temp_unit)
        temp_layout.addStretch()

    def update_indicator_display(self, label, value, warning_led, is_warning_active, is_current_warning, has_warning):
        """Update indicator display with warning colors and messages"""
        try:
            label.setText(f"{value:.1f}")
            
            # Get the position (FL, FR, RL, RR) from the label name
            label_name = label.objectName()
            if '_label_' in label_name:
                position = label_name.split('_label_')[1]
                warning_label = getattr(self, f'warning_label_{position}', None)
                if warning_label is None:
                    return
                
                tyre_position = {
                    'FL': 'Front Left',
                    'FR': 'Front Right',
                    'RL': 'Rear Left',
                    'RR': 'Rear Right'
                }[position]
                
                # Check if this is a pressure or temperature label
                is_pressure = 'pressure' in label_name
                tyre = self.tyre_data[position]
                
                if is_warning_active and is_current_warning and has_warning:
                    # Determine warning type and color
                    if is_pressure:
                        if value < 25:
                            color = "#8B0000"  # Dark red
                            message = f"Low Pressure: {value:.1f} PSI"
                        else:
                            color = "#FF0000"  # Red
                            message = f"High Pressure: {value:.1f} PSI"
                    else:  # Temperature
                        if value < 30:
                            color = "#00BFFF"  # Blue
                            message = f"Low Temperature: {value:.1f}°C"
                        else:
                            color = "#FF4500"  # Orange-Red
                            message = f"High Temperature: {value:.1f}°C"
                            
                    # Update warning LED and label with pulsing effect
                    warning_led.setStyleSheet(f"""
                        QLabel {{
                            background-color: {color};
                            border-radius: 6px;
                            border: 2px solid {color};
                        }}
                    """)
                    label.setStyleSheet(f"color: {color}; font: bold 14pt 'Segoe UI'; background: none;")
                    
                    # Show warning message
                    if len(tyre.get('warnings', [])) > 1:
                        warning_label.setText(f"Multiple Warnings Active")
                    else:
                        warning_label.setText(message)
                    warning_label.setStyleSheet(f"color: {color}; font: bold 9pt 'Segoe UI'; background: none;")
                else:
                    # Normal state colors based on value ranges
                    if is_pressure:
                        if 29 <= value <= 35:
                            color = "#7FFF00"  # Green
                        else:
                            color = "#FFA500"  # Orange
                    else:  # Temperature
                        if 30 <= value <= 50:
                            color = "#7FFF00"  # Green
                        else:
                            color = "#FFA500"  # Orange
                            
                    label.setStyleSheet(f"color: {color}; font: bold 14pt 'Segoe UI'; background: none;")
                    
                    if not is_warning_active:
                        warning_led.setStyleSheet("""
                            QLabel {
                                background-color: #7FFF00;
                                border-radius: 6px;
                                border: 1px solid #98FB98;
                            }
                        """)
                        warning_label.setText("Normal Operation")
                        warning_label.setStyleSheet("color: #7FFF00; font: bold 9pt 'Segoe UI'; background: none;")
                    
        except Exception as e:
            print(f"Error updating display: {str(e)}")
            import traceback
            traceback.print_exc()

    def speak_warning(self, message):
        """Speak the warning message using text-to-speech"""
        try:
            self.engine.say(message)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {str(e)}")

    def update_tyre_data(self):
        """Update tyre data with realistic simulation and sequential warnings"""
        if not self.frame_tyre.isVisible():
            return

        try:
            self.simulation_time += 1
            current_time = self.simulation_time
            
            # Ensure all tyres have required fields
            for position in ['FL', 'FR', 'RL', 'RR']:
                if position not in self.tyre_data:
                    self.tyre_data[position] = {
                        'pressure': 32.0,
                        'temp': 35.0,
                        'last_update': 0,
                        'warning_active': False,
                        'warnings': []
                    }
                tyre = self.tyre_data[position]
                if 'warning_active' not in tyre:
                    tyre['warning_active'] = False
                if 'warnings' not in tyre:
                    tyre['warnings'] = []
            
            # Handle warning sequence
            if self.warning_stage < len(self.warning_sequence):
                warning = self.warning_sequence[self.warning_stage]
                
                if not self.current_warning_tyre and not self.is_normal_phase:
                    if warning['type'] == 'normal':
                        # Start normal phase
                        self.is_normal_phase = True
                        self.last_warning_time = current_time
                        # Reset all tyres to normal
                        for pos in ['FL', 'FR', 'RL', 'RR']:
                            tyre = self.tyre_data[pos]
                            tyre['warning_active'] = False
                            tyre['warnings'] = []
                            # Gradually return to normal values
                            tyre['pressure'] = 32.0
                            tyre['temp'] = 35.0
                        # Update all displays
                        for pos in ['FL', 'FR', 'RL', 'RR']:
                            self.update_displays(pos)
                    else:
                        # Start new warning
                        self.current_warning_tyre = warning.get('tyre')
                        self.last_warning_time = current_time
                        voice_message = ""
                        is_critical = False

                        # Handle different warning types
                        if warning['type'] == 'pressure_dropping':
                            # Rapid pressure loss simulation
                            tyre = self.tyre_data[warning['tyre']]
                            tyre['warning_active'] = True
                            tyre['warnings'] = ['pressure_dropping']
                            tyre['pressure'] = warning['value']
                            is_critical = True
                            voice_message = (f"{self.get_tyre_name(warning['tyre'])} warning! "
                                           f"Rapid pressure loss detected! Current pressure: {int(warning['value'])} ... P S I. "
                                           f"Dropping at {abs(warning['rate'])} P S I per minute.")

                        elif warning['type'] == 'temp_spike':
                            # Temperature spike warning
                            tyre = self.tyre_data[warning['tyre']]
                            tyre['warning_active'] = True
                            tyre['warnings'] = ['temp_spike']
                            tyre['temp'] = warning['value']
                            is_critical = True
                            voice_message = (f"{self.get_tyre_name(warning['tyre'])} warning! "
                                           f"Sudden temperature spike detected: {int(warning['value'])} degrees!")

                        elif 'type' in warning and warning['type'] == 'both':
                            # Multiple issues (original or new scenarios)
                            tyre = self.tyre_data[warning['tyre']]
                            tyre['warning_active'] = True
                            tyre['warnings'] = ['pressure_high', 'temp_high']
                            tyre['pressure'] = warning['pressure']
                            tyre['temp'] = warning['temp']
                            is_critical = warning['temp'] >= 70 or warning['pressure'] >= 40 or warning['pressure'] <= 22
                            if is_critical:
                                voice_message = (f"{self.get_tyre_name(warning['tyre'])} warning! "
                                               f"Pressure: {int(warning['pressure'])} P S I. "
                                               f"Temperature: {int(warning['temp'])} degrees.")

                        else:
                            # Handle original warning types
                            tyre = self.tyre_data[warning['tyre']]
                            tyre['warning_active'] = True
                            if 'pressure' in warning['type']:
                                tyre['pressure'] = warning['value']
                                tyre['warnings'] = [warning['type']]
                                is_critical = warning['value'] >= 40 or warning['value'] <= 22
                                if is_critical:
                                    message = "High" if "high" in warning['type'] else "Low"
                                    voice_message = (f"{self.get_tyre_name(warning['tyre'])} warning! "
                                                   f"Critical {message.lower()} pressure: {int(warning['value'])} ... P S I.")
                            elif 'temp' in warning['type']:
                                tyre['temp'] = warning['value']
                                tyre['warnings'] = [warning['type']]
                                is_critical = warning['value'] >= 70 or warning['value'] <= 25
                                if is_critical:
                                    message = "High" if "high" in warning['type'] else "Low"
                                    voice_message = (f"{self.get_tyre_name(warning['tyre'])} warning! "
                                                   f"Critical {message.lower()} temperature: {int(warning['value'])} degrees.")

                        # Update displays first
                        if warning.get('tyre'):
                            self.update_displays(warning['tyre'])
                        
                        # Only announce if it's a critical warning
                        if is_critical and voice_message:
                            # Set speech properties for better clarity
                            self.engine.setProperty('rate', 130)
                            QTimer.singleShot(1500, lambda msg=voice_message: self.speak_warning(msg))
                            # Reset speech rate after announcement
                            QTimer.singleShot(5000, lambda: self.engine.setProperty('rate', 150))
                else:
                    # Handle active warning or normal phase
                    warning_elapsed = current_time - self.last_warning_time
                    duration = warning['duration'] if warning['type'] == 'normal' else self.warning_duration
                    
                    if warning_elapsed >= duration:
                        if self.is_normal_phase:
                            # End normal phase
                            self.is_normal_phase = False
                        else:
                            # Reset current warning
                            if self.current_warning_tyre:
                                tyre = self.tyre_data[self.current_warning_tyre]
                                tyre['warning_active'] = False
                                tyre['warnings'] = []
                            self.current_warning_tyre = None
                        
                        # Move to next stage
                        self.warning_stage += 1
                        self.last_warning_time = current_time
            
            # Update all tyre displays
            for position in ['FL', 'FR', 'RL', 'RR']:
                self.update_displays(position)

        except Exception as e:
            print(f"Error updating tyre data: {str(e)}")
            import traceback
            traceback.print_exc()
            
    def update_displays(self, position):
        """Update visual displays for a specific tyre"""
        try:
            tyre = self.tyre_data[position]
            
            if not tyre['warning_active']:
                # Normal value updates with unique variations
                pressure_change = random.uniform(-0.1, 0.1)
                temp_change = random.uniform(-0.2, 0.2)
                
                # Position-specific biases
                if position in ['FL', 'FR']:
                    temp_change += 0.05  # Front tyres slightly warmer
                if position in ['FL', 'RL']:
                    pressure_change += 0.02  # Left side slightly higher pressure
                
                # Gradual return to normal values
                target_pressure = 32.0
                target_temp = 35.0
                tyre['pressure'] += (target_pressure - tyre['pressure']) * 0.1 + pressure_change
                tyre['temp'] += (target_temp - tyre['temp']) * 0.1 + temp_change
                
                # Ensure values stay within safe ranges
                tyre['pressure'] = max(20.0, min(45.0, tyre['pressure']))
                tyre['temp'] = max(20.0, min(80.0, tyre['temp']))
            
            # Update displays
            pressure_label = getattr(self, f'pressure_label_{position}')
            temp_label = getattr(self, f'temp_label_{position}')
            warning_led = getattr(self, f'warning_led_{position}')
            
            self.update_indicator_display(
                pressure_label,
                tyre['pressure'],
                warning_led,
                tyre['warning_active'],
                position == self.current_warning_tyre,
                'pressure' in str(tyre.get('warnings', []))
            )
            self.update_indicator_display(
                temp_label,
                tyre['temp'],
                warning_led,
                tyre['warning_active'],
                position == self.current_warning_tyre,
                'temp' in str(tyre.get('warnings', []))
            )
        except Exception as e:
            print(f"Error updating displays for {position}: {str(e)}")
            traceback.print_exc()

    def get_tyre_name(self, position):
        """Convert tyre position code to readable name"""
        names = {
            'FL': 'Front Left Tyre',
            'FR': 'Front Right Tyre',
            'RL': 'Rear Left Tyre',
            'RR': 'Rear Right Tyre'
        }
        return names.get(position, position)

    def update_status_indicators(self):
        """Update the status indicators with neon styling"""
        try:
            # Create status bar with proper spacing
            self.status_bar.setGeometry(QtCore.QRect(285, 360, 400, 40))
            self.status_bar.setStyleSheet("""
                QFrame {
                    background: rgba(15, 20, 30, 150);
                    border-radius: 20px;
                }
            """)

            # Create modern button-like indicators
            status_texts = [
                "Pressure",
                "Temperature",
                "Balance"
            ]

            # Clear existing layout
            for i in reversed(range(self.status_bar.layout().count())): 
                self.status_bar.layout().itemAt(i).widget().setParent(None)

            # Add new indicators with neon effect
            for text in status_texts:
                indicator = QtWidgets.QLabel(text)
                indicator.setStyleSheet("""
                    QLabel {
                        color: rgb(0, 255, 127);
                        font: bold 12pt 'Segoe UI';
                        padding: 5px 30px;
                        border: 1px solid rgb(0, 255, 127);
                        border-radius: 15px;
                    }
                """)
                indicator.setAlignment(Qt.AlignCenter)
                self.status_bar.layout().addWidget(indicator)

        except Exception as e:
            print(f"Error updating status indicators: {str(e)}")

    def get_status_color(self, is_ok):
        """Return color for status indicators"""
        return "rgb(0, 255, 127)" if is_ok else "rgb(255, 50, 50)"

    # Method to handle resizing and reposition elements like the attribution label
    def resize_main_window_elements(self, event):
        # No need to adjust positions since everything is in the main_container
        # and centered using layout
        QtWidgets.QMainWindow.resizeEvent(self.centralwidget.parentWidget(), event)

    def showEvent(self, event):
        # Initial resize to ensure proper layout
        self.resize_main_window_elements(None)
        super().showEvent(event)

    def update_datetime(self):
        current_dt = QDateTime.currentDateTime()
        display_text = current_dt.toString("MMM d, yyyy\nhh:mm:ss AP")
        self.date.setText(display_text)

    def browse_music_files(self):
        try:
            file_dialog = QFileDialog()
            file_dialog.setStyleSheet("""
                QFileDialog {
                    background-color: rgb(30, 31, 40);
                }
                QFileDialog QLabel {
                    color: rgb(200, 200, 200);
                }
                QFileDialog QPushButton {
                    background-color: rgb(43, 87, 151);
                    color: white;
                    border: 1px solid rgb(100, 200, 255);
                    border-radius: 4px;
                    padding: 5px 15px;
                    min-width: 80px;
                }
                QFileDialog QPushButton:hover {
                    background-color: rgb(65, 105, 225);
                }
                QFileDialog QLineEdit {
                    background-color: rgb(40, 41, 50);
                    color: white;
                    border: 1px solid rgb(100, 200, 255);
                    border-radius: 4px;
                    padding: 3px;
                }
                QFileDialog QTreeView {
                    background-color: rgb(40, 41, 50);
                    color: white;
                }
                QFileDialog QTreeView::item:selected {
                    background-color: rgb(65, 105, 225);
                }
            """)
            
            file_path, _ = file_dialog.getOpenFileName(
                self.frame_music,
                "Select Music File",
                "",
                "Audio Files (*.mp3 *.wav *.ogg *.m4a *.flac)"
            )
            
            if file_path:
                try:
                    self.current_music_file = file_path
                    pygame.mixer.music.load(file_path)
                    self.is_playing = False
                    self.is_paused = False
                    
                    # Update display with file name
                    file_name = os.path.basename(file_path)
                    if len(file_name) > 40:  # Truncate long names
                        file_name = file_name[:37] + "..."
                    self.label_33.setText(file_name)
                    self.label_33.setStyleSheet("""
                        color: rgb(0, 255, 255);
                        font: bold 12pt "Segoe UI";
                        background: none;
                    """)
                    
                except pygame.error as e:
                    QMessageBox.warning(
                        self.frame_music,
                        "Error",
                        f"Could not load music file: {str(e)}"
                    )
        except Exception as e:
            QMessageBox.warning(
                self.frame_music,
                "Error",
                f"An error occurred: {str(e)}"
            )

    def load_music(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            self.is_playing = False
            self.is_paused = False
        except pygame.error as e:
            QMessageBox.warning(None, "Error", f"Could not load music file: {str(e)}")

    def toggle_play_pause(self):
        if self.current_music_file is None:
            QMessageBox.information(None, "No Music", "Please select a music file first.")
            return
            
        if not self.is_playing and not self.is_paused:
            pygame.mixer.music.play()
            self.is_playing = True
        elif self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            
    def toggle_mode(self, state):
        if state == Qt.Checked:
            # Light mode styling
            light_frame_style = """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 250),
                        stop:0.5 rgba(248, 250, 255, 250),
                        stop:1 rgba(240, 245, 255, 250));
                    border-radius: 200px;
                }
            """
            
            self.frame_dashboard.setStyleSheet(light_frame_style)
            self.frame_tyre.setStyleSheet(light_frame_style)
            self.frame_AC.setStyleSheet(light_frame_style)
            self.frame_map.setStyleSheet(light_frame_style)
            self.frame_music.setStyleSheet(light_frame_style)
        else:
            # Dark mode styling
            dark_frame_style = """
                QFrame {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(34, 46, 61, 255),
                        stop:1 rgba(34, 34, 47, 255));
                    border-radius: 200px;
                }
            """
            
            self.frame_dashboard.setStyleSheet(dark_frame_style)
            self.frame_tyre.setStyleSheet(dark_frame_style)
            self.frame_AC.setStyleSheet(dark_frame_style)
            self.frame_map.setStyleSheet(dark_frame_style)
            self.frame_music.setStyleSheet(dark_frame_style)

    def next_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def previous_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def change_volume(self):
        volume = self.dial.value() / 100.0
        pygame.mixer.music.set_volume(volume)

    def get_city_coordinates(self, city_name):
        indian_cities = {
            'mumbai': [19.0760, 72.8777], 'delhi': [28.7041, 77.1025], 'bangalore': [12.9716, 77.5946],
            'chennai': [13.0827, 80.2707], 'kolkata': [22.5726, 88.3639], 'hyderabad': [17.3850, 78.4867],
            'pune': [18.5204, 73.8567], 'ahmedabad': [23.0225, 72.5714], 'jaipur': [26.9124, 75.7873],
            'surat': [21.1702, 72.8311], 'lucknow': [26.8467, 80.9462], 'kanpur': [26.4499, 80.3319],
            'nagpur': [21.1458, 79.0882], 'indore': [22.7196, 75.8577], 'thane': [19.2183, 72.9781],
            'bhopal': [23.2599, 77.4126], 'visakhapatnam': [17.6868, 83.2185], 'pimpri': [18.6298, 73.8075],
            'patna': [25.5941, 85.1376], 'vadodara': [22.3072, 73.1812], 'ghaziabad': [28.6692, 77.4538],
            'ludhiana': [30.9010, 75.8573], 'coimbatore': [11.0168, 76.9558], 'agra': [27.1767, 78.0081],
            'madurai': [9.9252, 78.1198], 'nashik': [19.9975, 73.7898], 'faridabad': [28.4089, 77.3178],
            'meerut': [28.9845, 77.7064], 'rajkot': [22.3039, 70.8022], 'kalyan': [19.2437, 73.1355],
            'vasai': [19.4912, 72.8056], 'hubli': [15.3647, 75.1240], 'dharwad': [15.4589, 75.0078],
            'mysore': [12.2958, 76.6394], 'aurangabad': [19.8762, 75.3433], 'jodhpur': [26.2389, 73.0243],
            'kota': [25.2138, 75.8648], 'guwahati': [26.1445, 91.7362], 'chandigarh': [30.7333, 76.7794],
            'salem': [11.6643, 78.1460], 'howrah': [22.5958, 88.2636], 'tiruchirappalli': [10.7905, 78.7047],
            'solapur': [17.6599, 75.9064], 'tiruppur': [11.1085, 77.3411], 'moradabad': [28.8386, 78.7733],
            'aligarh': [27.8974, 78.0880], 'jamshedpur': [22.8046, 86.2029], 'jabalpur': [23.1815, 79.9864],
            'gwalior': [26.2183, 78.1828]
        }
        city_lower = city_name.lower().strip()
        return indian_cities.get(city_lower, None)

    def update_map(self):
        try:
            m = folium.Map(
                tiles='OpenStreetMap',
                zoom_start=12 if not self.destination else 8,
                location=self.current_location
            )
            folium.Marker(
                self.current_location, popup="Current Location - KLE Tech University, Hubli",
                tooltip="You are here", icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            if self.destination:
                folium.Marker(
                    self.destination, popup=f"Destination - {self.destination_name}",
                    tooltip="Destination", icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)
                folium.PolyLine(
                    [self.current_location, self.destination], color="blue", weight=3, opacity=0.7
                ).add_to(m)
                m.fit_bounds([self.current_location, self.destination], padding=(50, 50))
            
            data = io.BytesIO()
            m.save(data, close_file=False)
            if hasattr(self, 'map_plot'):
                self.map_plot.setHtml(data.getvalue().decode())
        except Exception as e:
            print(f"Error updating map: {e}")

    def get_current_location(self):
        try:
            import random
            lat_offset, lon_offset = random.uniform(-0.002, 0.002), random.uniform(-0.002, 0.002)
            self.current_location = [15.3647 + lat_offset, 75.1240 + lon_offset]
            self.update_map()
            self.location_display.setText(f"Current: {self.current_location[0]:.4f}, {self.current_location[1]:.4f}")
            QMessageBox.information(None, "Location Updated", 
                                  f"Location updated near KLE Tech University, Hubli\n"
                                  f"Coordinates: {self.current_location[0]:.6f}, {self.current_location[1]:.6f}")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Could not get current location: {str(e)}")

    def set_destination_from_input(self):
        try:
            destination_text = self.destination_input.text().strip()
            if not destination_text:
                QMessageBox.warning(None, "Input Error", "Please enter a destination city name.")
                return
            
            coordinates = self.get_city_coordinates(destination_text)
            if coordinates:
                self.destination = coordinates
                self.destination_name = destination_text.title()
                self.update_map()
                distance = self.calculate_distance(self.current_location, self.destination)
                QMessageBox.information(None, "Destination Set", 
                                      f"Destination set to: {self.destination_name}\n"
                                      f"Coordinates: {coordinates[0]:.4f}, {coordinates[1]:.4f}\n"
                                      f"Approximate distance: {distance:.1f} km")
                self.destination_input.clear()
            else:
                QMessageBox.warning(None, "City Not Found", 
                                  f"Sorry, '{destination_text}' is not in our database.\n"
                                  f"Please try major Indian cities like Mumbai, Delhi, Bangalore, etc.")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Could not set destination: {str(e)}")

    def calculate_distance(self, point1, point2):
        import math
        lat1, lon1 = map(math.radians, point1)
        lat2, lon2 = map(math.radians, point2)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371 
        return c * r

    def toggle_door(self):
        if self.door_status == "Locked":
            self.door_status = "Unlocked"
            self.door_toggle_btn.setText("Lock Door")
            self.door_toggle_btn.setChecked(True)
            # Force car to stop immediately when door is unlocked
            self.current_speed = 0
            self.current_rpm = 0
            self.acceleration = 0
            self.is_accelerating = False
            self.is_braking = True
            self.speed.update_value(0)
            self.rpm.update_value(0)
            self.gear_label.setText("P")
            self.mode_label.setText("PARKED")
            QMessageBox.warning(None, "Safety Alert", "Door unlocked! Vehicle cannot move until doors are locked.")
        else:
            self.door_status = "Locked"
            self.door_toggle_btn.setText("Unlock Door")
            self.door_toggle_btn.setChecked(False)

    def viewCam(self):
        if self.cap is not None:
            ret, image = self.cap.read()
            if ret:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = image.shape
                qImg = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
                self.webcam.setPixmap(QPixmap.fromImage(qImg))
            else:
                self.webcam.setText("Camera Error")

    def quit_cam(self):
        self.timer.stop()
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
            self.cap = None
        self.webcam.clear()
        self.webcam.setText("Camera Off") 
        if hasattr(self, 'btn_camera_toggle'):
            self.btn_camera_toggle.setText("Start Camera")

    def controlTimer(self):
        if not self.timer.isActive():
            try:
                self.cap = cv2.VideoCapture(0)
                if self.cap and self.cap.isOpened(): 
                    self.timer.start(30)
                    self.btn_camera_toggle.setText("Stop Camera")
                    self.webcam.setText("") 
                else:
                    self.cap = None 
                    QMessageBox.warning(None, "Camera Error", "Could not access camera.")
                    self.webcam.setText("Camera Error")
            except Exception as e:
                QMessageBox.warning(None, "Camera Error", f"Error starting camera: {str(e)}")
                self.webcam.setText("Camera Error")
        else:
            self.quit_cam()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("CAR DASHBOARD", "Enhanced Car Dashboard - KLE Tech"))
        # Update button text order to match creation order
        self.btn_dash.setText(_translate("MainWindow", "DASHBOARD"))
        self.btn_tyre.setText(_translate("MainWindow", "TYRE"))
        self.btn_ac.setText(_translate("MainWindow", "AC"))
        self.btn_tyre.setText(_translate("MainWindow", "TYRE"))  # Add tyre button text
        self.btn_music.setText(_translate("MainWindow", "MUSIC"))
        self.btn_map.setText(_translate("MainWindow", "MAP"))
        self.label_7.setText(_translate("MainWindow", "Locked"))
        self.label_5.setText(_translate("MainWindow", "Open"))
        self.label_4.setText(_translate("MainWindow", "Locked"))
        self.label_8.setText(_translate("MainWindow", "Locked"))
        self.label_9.setText(_translate("MainWindow", "Locked"))
        self.label_6.setText(_translate("MainWindow", "Locked"))
        self.label_14.setText(_translate("MainWindow", "Battery"))  # Changed from Fuel to Battery
        self.door_toggle_btn.setText(_translate("MainWindow", "Unlock Door"))
        
        # Temperature displays
        self.labelOutdoorTemp.setText(_translate("MainWindow", "29°C"))
        self.labelOutdoorText.setText(_translate("MainWindow", "Outdoor\nTemperature"))
        self.labelIndoorTemp.setText(_translate("MainWindow", "20°C"))
        self.labelIndoorText.setText(_translate("MainWindow", "Indoor\nTemperature"))
        
        self.label_18.setText(_translate("MainWindow", "Weather Forecast - Hubli"))
        self.label_17.setText(_translate("MainWindow", "Precipitation: 20%\nHumidity: 70%\nWind: 32 km/h"))
        self.label_25.setText(_translate("MainWindow", "Mode1"))
        self.label_26.setText(_translate("MainWindow", "Mode2"))
        self.label_27.setText(_translate("MainWindow", "Mode3"))
        self.labelPercentageCPU_4.setText(_translate("MainWindow", "<html><head/><body><p>Cloudy</p></body></html>"))
        self.checked.setText(_translate("MainWindow", "AC Toggle"))
        self.label_20.setText(_translate("MainWindow", "Volume"))
        self.label_28.setText(_translate("MainWindow", "Mixer"))
        self.label_33.setText(_translate("MainWindow", "No Music Selected - Click Browse Music"))
        self.webcam.setText(_translate("MainWindow", "Camera Off")) 
        
        self.btn_dash.clicked.connect(self.show_Dash)
        self.btn_ac.clicked.connect(self.show_AC)
        self.btn_tyre.clicked.connect(self.show_Tyre)
        self.btn_music.clicked.connect(self.show_Music)
        self.btn_map.clicked.connect(self.show_Map)
        self.door_toggle_btn.clicked.connect(self.toggle_door)

    def show_Dash(self):
        """Show dashboard section and hide others"""
        try:
            self.quit_cam()
            self.frame_dashboard.setVisible(True)
            self.frame_dashboard.raise_()
            self.frame_tyre.setVisible(False)
            self.frame_AC.setVisible(False)
            self.frame_map.setVisible(False)
            self.frame_music.setVisible(False)
            # Ensure dashboard elements are visible and properly layered
            self.speed.setVisible(True)
            self.rpm.setVisible(True)
            self.frame_2.setVisible(True)
            self.frame_3.setVisible(True)
            self.frame_4.setVisible(True)
            self.frame_5.setVisible(True)
            self.car_state.setVisible(True)
        except Exception as e:
            print(f"Error in show_Dash: {str(e)}")

    def show_Tyre(self):
        """Show tyre section and hide others"""
        try:
            self.quit_cam()
            self.frame_dashboard.setVisible(False)
            self.frame_tyre.setVisible(True)
            self.frame_tyre.raise_()
            self.frame_AC.setVisible(False)
            self.frame_map.setVisible(False)
            self.frame_music.setVisible(False)
        except Exception as e:
            print(f"Error in show_Tyre: {str(e)}")

    def show_AC(self):
        """Show AC section and hide others"""
        try:
            self.quit_cam()
            self.frame_dashboard.setVisible(False)
            self.frame_tyre.setVisible(False)
            self.frame_map.setVisible(False)
            self.frame_music.setVisible(False)
            
            # Show AC frame and ensure proper z-ordering
            self.frame_AC.setVisible(True)
            self.frame_AC.raise_()
            
            # Ensure all AC components are visible and properly ordered
            self.circularProgressCPU.setVisible(True)
            self.circularOutdoor.setVisible(True)
            self.labelOutdoorTemp.setVisible(True)
            self.labelOutdoorText.setVisible(True)
            
            self.circularIndoor.setVisible(True)
            self.circularInner.setVisible(True)
            self.labelIndoorTemp.setVisible(True)
            self.labelIndoorText.setVisible(True)
            
            self.weather.setVisible(True)
            self.temp_control_frame.setVisible(True)
            
            # Update the weather display immediately
            self.update_weather()
        except Exception as e:
            print(f"Error in show_AC: {str(e)}")

    def show_Music(self):
        """Show music section and hide others"""
        try:
            self.quit_cam()
            self.frame_dashboard.setVisible(False)
            self.frame_tyre.setVisible(False)
            self.frame_AC.setVisible(False)
            self.frame_map.setVisible(False)
            self.frame_music.setVisible(True)
            self.frame_music.raise_()
        except Exception as e:
            print(f"Error in show_Music: {str(e)}")

    def show_Map(self):
        """Show map section and hide others"""
        try:
            self.frame_dashboard.setVisible(False)
            self.frame_tyre.setVisible(False)
            self.frame_AC.setVisible(False)
            self.frame_map.setVisible(True)
            self.frame_map.raise_()
            self.frame_music.setVisible(False)
        except Exception as e:
            print(f"Error in show_Map: {str(e)}")

    def progress(self):
        self.speed.set_MaxValue(200)
        self.speed.set_MinValue(0)
        self.speed.set_DisplayValueColor(200, 200, 200)
        self.speed.set_CenterPointColor(255, 255, 255)
        self.speed.set_NeedleColor(255, 255, 200)
        self.speed.set_NeedleColorDrag(255, 255, 255)
        self.speed.set_ScaleValueColor(255, 255, 255)
        self.speed.set_enable_big_scaled_grid(True)
        self.speed.set_enable_barGraph(False)
        self.speed.set_enable_filled_Polygon(False)
        self.speed.update_value(0)  # Start at 0
        self.speed.set_enable_value_text_display(True)
        self.speed.units = "Km/h"

        self.rpm.set_scala_main_count(8)
        self.rpm.set_MaxValue(8)
        self.rpm.set_MinValue(0)
        self.rpm.update_value(0)  # Start at 0
        self.rpm.set_DisplayValueColor(200, 200, 200)
        self.rpm.set_enable_big_scaled_grid(True)
        self.rpm.set_ScaleValueColor(255, 255, 255)
        self.rpm.set_NeedleColorDrag(255, 255, 255)
        self.rpm.set_CenterPointColor(255, 255, 255)
        self.rpm.units = " RPM"
        self.rpm.set_enable_value_text_display(True)

    def update_car_status(self):
        # First check door status - if unlocked, force stop all movement
        if self.door_status == "Unlocked":
            if self.current_speed > 0 or self.current_rpm > 0:
                self.current_speed = 0
                self.current_rpm = 0
                self.acceleration = 0
                self.is_accelerating = False
                self.is_braking = True
                self.speed.update_value(0)
                self.rpm.update_value(0)
                self.gear_label.setText("P")
                self.gear_label.setStyleSheet("color: rgb(255, 100, 100); font: bold 14pt 'Segoe UI'; background: none;")
                self.mode_label.setText("PARKED")
                self.mode_label.setStyleSheet("color: rgb(255, 100, 100); font: bold 12pt 'Segoe UI'; background: none;")
            return  # Exit the method early - no updates if door is unlocked

        # Get laptop battery percentage
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.battery_percentage = battery.percent
            else:
                battery_drain = (abs(self.acceleration) * 0.01 + self.current_speed * 0.0005)
                self.battery_percentage = max(0, min(100, self.battery_percentage - battery_drain))
        except Exception as e:
            print(f"Error reading battery: {e}")
            battery_drain = (abs(self.acceleration) * 0.01 + self.current_speed * 0.0005)
            self.battery_percentage = max(0, min(100, self.battery_percentage - battery_drain))

        # Enhanced movement simulation when doors are locked
        # Increased chance of acceleration changes for more dynamic movement
        if random.random() < 0.2:  # Increased from 0.1 to 0.2 for more frequent changes
            self.is_accelerating = not self.is_accelerating
        if random.random() < 0.1:  # Increased from 0.05 to 0.1 for more dynamic braking
            self.is_braking = not self.is_braking
            
        # More aggressive acceleration and deceleration
        if self.is_accelerating and not self.is_braking:
            self.acceleration = min(self.acceleration + 1.0, 8.0)  # Increased acceleration rate and max
        elif self.is_braking:
            self.acceleration = max(self.acceleration - 1.5, -5.0)  # Increased braking power
        else:
            self.acceleration = max(self.acceleration - 0.5, 0)  # Faster return to neutral
            
        # More responsive speed updates
        speed_change = self.acceleration * 1.5  # Increased speed change multiplier
        self.current_speed = max(0, min(200, self.current_speed + speed_change))
        
        # More responsive RPM calculation
        self.current_rpm = (self.current_speed / 200.0) * 8.0

        # Update gear indicator based on speed and state
        if self.current_speed == 0:
            if self.is_braking:
                self.gear_label.setText("P")
                self.gear_label.setStyleSheet("color: rgb(0, 255, 255); font: bold 14pt 'Segoe UI'; background: none;")
            else:
                self.gear_label.setText("N")
                self.gear_label.setStyleSheet("color: rgb(255, 255, 0); font: bold 14pt 'Segoe UI'; background: none;")
        else:
            if self.is_braking:
                self.gear_label.setText("B")
                self.gear_label.setStyleSheet("color: rgb(255, 100, 100); font: bold 14pt 'Segoe UI'; background: none;")
            else:
                self.gear_label.setText("D")
                self.gear_label.setStyleSheet("color: rgb(100, 255, 100); font: bold 14pt 'Segoe UI'; background: none;")

        # More dynamic driving mode transitions
        if self.current_speed > 140 or self.acceleration > 6:  # Adjusted thresholds
            self.mode_label.setText("SPORT")
            self.mode_label.setStyleSheet("color: rgb(255, 100, 100); font: bold 12pt 'Segoe UI'; background: none;")
        elif self.current_speed > 80 or self.acceleration > 3:  # Adjusted thresholds
            self.mode_label.setText("NORMAL")
            self.mode_label.setStyleSheet("color: rgb(255, 255, 100); font: bold 12pt 'Segoe UI'; background: none;")
        else:
            self.mode_label.setText("ECO")
            self.mode_label.setStyleSheet("color: rgb(100, 255, 100); font: bold 12pt 'Segoe UI'; background: none;")

        # Update UI elements
        self.speed.update_value(self.current_speed)
        self.rpm.update_value(self.current_rpm)
        self.battery_level.setValue(int(self.battery_percentage))

        # Update battery level color based on percentage
        if self.battery_percentage <= 20:
            self.battery_level.setStyleSheet("""
                QProgressBar {
                    background-color: rgba(50, 50, 50, 150);
                    color: white;
                    text-align: center;
                    font: bold 9pt 'Segoe UI';
                    margin: 0px;
                    padding: 0px;
                    border: 2px solid rgba(231, 76, 60, 200);
                }
                QProgressBar::chunk {
                    background-color: rgb(231, 76, 60);
                }
            """)
        elif self.battery_percentage <= 50:
            self.battery_level.setStyleSheet("""
                QProgressBar {
                    background-color: rgba(50, 50, 50, 150);
                    color: white;
                    text-align: center;
                    font: bold 9pt 'Segoe UI';
                    margin: 0px;
                    padding: 0px;
                    border: 2px solid rgba(241, 196, 15, 200);
                }
                QProgressBar::chunk {
                    background-color: rgb(241, 196, 15);
                }
            """)
        else:
            self.battery_level.setStyleSheet("""
                QProgressBar {
                    background-color: rgba(50, 50, 50, 150);
                    color: white;
                    text-align: center;
                    font: bold 9pt 'Segoe UI';
                    margin: 0px;
                    padding: 0px;
                    border: 2px solid rgba(39, 174, 96, 200);
                }
                QProgressBar::chunk {
                    background-color: rgb(39, 174, 96);
                }
            """)

        # Faster road animation
        self.animation_speed = self.current_speed / 6  # Increased animation speed
        marker_spacing = 35
        marker_height = 15
        
        for i, marker in enumerate(self.road_markers):
            self.marker_positions[i] += self.animation_speed
            if self.marker_positions[i] > 250:  # Reset when marker goes below
                self.marker_positions[i] = -marker_height
            marker.setGeometry(QtCore.QRect(115, int(self.marker_positions[i]), 40, marker_height))

    def simulate_driving_conditions(self):
        """Simulate different driving conditions affecting tyre pressure and temperature"""
        # Randomly change driving conditions
        if random.random() < 0.1:  # 10% chance to change driving condition
            self.driving_condition = random.choice(["normal", "aggressive", "highway"])
        
        # Update ambient temperature with small variations
        self.ambient_temp += random.uniform(-0.2, 0.2)
        self.ambient_temp = max(15.0, min(35.0, self.ambient_temp))
        
        # Return modifiers based on main.py thresholds
        if self.driving_condition == "aggressive":
            return {
                'pressure': random.uniform(-0.3, 0.5),  # More extreme pressure changes
                'temp': random.uniform(0.5, 1.0)  # Higher temperature increases
            }
        elif self.driving_condition == "highway":
            return {
                'pressure': random.uniform(-0.1, 0.3),  # Moderate pressure changes
                'temp': random.uniform(0.3, 0.7)  # Moderate temperature increases
            }
        else:  # normal driving
            return {
                'pressure': random.uniform(-0.2, 0.2),  # Small pressure fluctuations
                'temp': random.uniform(-0.3, 0.3)  # Small temperature changes
            }

    def create_connection_lines(self):
        """Create subtle connecting lines between car and indicators"""
        line_color = "rgba(0, 171, 169, 100)"
        
        # Define line positions with adjusted coordinates for smaller indicators
        line_positions = [
            # Front Left
            (335, 180, 120, 2, True),
            # Front Right
            (485, 180, 190, 2, False),
            # Rear Left
            (335, 260, 120, 2, True),
            # Rear Right
            (485, 260, 190, 2, False)
        ]

        self.lines = []
        for x, y, w, h, is_left in line_positions:
            line = QtWidgets.QFrame(self.frame_tyre)
            line.setGeometry(QtCore.QRect(x, y, w, h))
            gradient_direction = "x1:0, y1:0, x2:1, y2:0" if is_left else "x1:1, y1:0, x2:0, y2:0"
            line.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient({gradient_direction},
                        stop:0 {line_color},
                        stop:1 rgba(0, 171, 169, 0));
                    border: none;
                }}
            """)
            self.lines.append(line)

    def increase_temperature(self):
        if self.current_temp < self.max_temp:
            self.current_temp += 1
            self.update_temperature_display()

    def decrease_temperature(self):
        if self.current_temp > self.min_temp:
            self.current_temp -= 1
            self.update_temperature_display()

    def update_temperature_display(self):
        # Update temperature display
        self.temp_display.setText(f"{self.current_temp}°C")
        self.labelIndoorTemp.setText(f"{self.current_temp}°C")

        # Calculate color based on temperature
        if self.current_temp <= 20:
            # Cool colors (blue to cyan)
            ratio = (self.current_temp - self.min_temp) / (20 - self.min_temp)
            color = QColor(0, int(171 + (84 * ratio)), int(255 - (86 * ratio)))
        else:
            # Warm colors (cyan to red)
            ratio = (self.current_temp - 20) / (self.max_temp - 20)
            color = QColor(int(255 * ratio), int(171 * (1 - ratio)), int(169 * (1 - ratio)))

        # Update circular frame gradient
        self.circularInner.setStyleSheet(f"""
            QFrame {{
                border-radius: 95px;
                background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                    stop:0 {color.name()},
                    stop:0.7 rgba({color.red()}, {color.green()}, {color.blue()}, 180),
                    stop:1 rgba({color.red()}, {color.green()}, {color.blue()}, 100));
            }}
        """)

    def update_weather(self):
        try:
            current_hour = QDateTime.currentDateTime().time().hour()
            
            # Base temperature curve throughout the day
            # Coolest at 4AM, warmest at 2PM
            base_temp = 25.0  # Base temperature
            
            # Temperature variation based on time of day
            if 0 <= current_hour < 4:
                # Late night to early morning (coolest)
                temp_offset = -5.0
            elif 4 <= current_hour < 10:
                # Morning temperature rise
                progress = (current_hour - 4) / 6
                temp_offset = -5.0 + (progress * 12.0)
            elif 10 <= current_hour < 14:
                # Midday peak
                temp_offset = 7.0
            elif 14 <= current_hour < 20:
                # Afternoon decline
                progress = (current_hour - 14) / 6
                temp_offset = 7.0 - (progress * 8.0)
            else:
                # Evening and night
                progress = (current_hour - 20) / 4
                temp_offset = -1.0 - (progress * 4.0)

            # Add random fluctuation
            random_fluctuation = random.uniform(-0.5, 0.5)
            
            # Calculate new temperature
            new_temp = base_temp + temp_offset + random_fluctuation
            
            # Smooth transition to new temperature
            self.outdoor_temp += (new_temp - self.outdoor_temp) * 0.3
            
            # Update weather conditions periodically
            if random.random() < 0.2:  # 20% chance to change weather
                self.current_weather = random.choice(self.weather_conditions)
                
               
                if self.current_weather == "Rainy":
                    self.outdoor_temp -= random.uniform(2.0, 4.0)
                elif self.current_weather == "Cloudy":
                    self.outdoor_temp -= random.uniform(1.0, 2.0)
                
                
                if self.current_weather == "Rainy":
                    self.humidity = random.randint(80, 95)
                    self.wind_speed = random.randint(25, 45)
                    self.precipitation = random.randint(60, 90)
                elif self.current_weather == "Cloudy":
                    self.humidity = random.randint(65, 80)
                    self.wind_speed = random.randint(20, 35)
                    self.precipitation = random.randint(20, 40)
                else:
                    self.humidity = random.randint(50, 70)
                    self.wind_speed = random.randint(10, 25)
                    self.precipitation = random.randint(0, 20)

            # Update displays
            self.labelOutdoorTemp.setText(f"{self.outdoor_temp:.1f}°C")
            self.labelPercentageCPU_4.setText(f"<html><head/><body><p>{self.current_weather}</p></body></html>")
            self.label_17.setText(f"Precipitation: {self.precipitation}%\nHumidity: {self.humidity}%\nWind: {self.wind_speed} km/h")
            
            
            weather_icon = ":/icons/p.png" 
            if self.current_weather == "Clear":
                weather_icon = ":/icons/sunny.png"
            elif self.current_weather == "Rainy":
                weather_icon = ":/icons/rainy.png"
            elif self.current_weather == "Partly Cloudy":
                weather_icon = ":/icons/partly_cloudy.png"
            
            self.label_2.setPixmap(QtGui.QPixmap(weather_icon))
            
            
            temp_difference = self.outdoor_temp - self.current_temp
            if abs(temp_difference) > 15:  
                
                if self.current_temp < self.outdoor_temp:
                    self.current_temp += 0.1
                else:
                    self.current_temp -= 0.1
                self.update_temperature_display()

        except Exception as e:
            print(f"Error updating weather: {str(e)}")

import resources

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())