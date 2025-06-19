#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom PyQt5 widgets for the car dashboard application
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QApplication
from PyQt5.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation, QRect, pyqtProperty
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtProperty, QTime, QEasingCurve, QPropertyAnimation
from PyQt5.QtGui import QColor, QPainter, QPen, QFont, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSlider,
    QPushButton,
    QGraphicsDropShadowEffect,
    QDial,
    QLabel
)


class AnimatedToggle(QCheckBox):
    """
    Animated toggle switch widget
    """
    def __init__(self, parent=None, width=60, bg_color="#777", circle_color="#DDD", 
                 active_color="#00BCff", animation_curve=QEasingCurve.OutBounce):
        super().__init__(parent)
        
        # Set properties
        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)
        
        # Colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        
        # Animation
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        
        # Connect signals
        self.stateChanged.connect(self.start_transition)
        
    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
        
    def start_transition(self, value):
        """Start animation when toggle state changes"""
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)
        self.animation.start()
        
    def hitButton(self, pos):
        """Define clickable area"""
        return self.contentsRect().contains(pos)
        
    def paintEvent(self, e):
        """Custom paint event for the toggle switch"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Set pen
        p.setPen(Qt.NoPen)
        
        # Draw background
        rect = QRect(0, 0, self.width(), self.height())
        if self.isChecked():
            p.setBrush(QColor(self._active_color))
        else:
            p.setBrush(QColor(self._bg_color))
        p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)
        
        # Draw circle
        p.setBrush(QColor(self._circle_color))
        p.drawEllipse(self._circle_position, 3, 22, 22)
        p.end()


class CircularProgressBar(QWidget):
    """
    Circular progress bar widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Properties
        self.value = 0
        self.width_val = 240
        self.height_val = 240
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.max_value = 100
        self.progress_color = "#05B8CC"
        self.enable_text = True
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = "#FFFFFF"
        self.enable_bg = True
        self.bg_color = "#44475a"
        
        # Resize
        self.resize(self.width_val, self.height_val)
        
    def add_shadow(self, enable):
        """Add shadow effect"""
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 80))
            self.setGraphicsEffect(self.shadow)
            
    def set_value(self, value):
        """Set progress value"""
        self.value = value
        self.repaint()
        
    def paintEvent(self, e):
        """Custom paint event"""
        # Set progress parameters
        width = self.width_val - self.progress_width
        height = self.height_val - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value
        
        # Painter
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setFont(QFont(self.font_family, self.font_size))
        
        # Create rectangle
        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)
        
        # Pen
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        
        # Set round cap
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)
            
        # Enable background
        if self.enable_bg:
            pen.setColor(QColor(self.bg_color))
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)
            
        # Create arc / circular progress
        pen.setColor(QColor(self.progress_color))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)
        
        # Create text
        if self.enable_text:
            pen.setColor(QColor(self.text_color))
            paint.setPen(pen)
            paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")
            
        # End
        paint.end()


class CustomSlider(QSlider):
    """
    Custom styled slider widget
    """
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        
        # Styling
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #d4d4d4, stop:1 #afafaf);
            }
            
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #66e, stop:1 #bbf);
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::add-page:horizontal {
                background: #fff;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
        """)


class GlowButton(QPushButton):
    """
    Button with glow effect
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        
        # Set default styling
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(43, 87, 151, 100);
                border: 2px solid rgba(43, 87, 151, 150);
                border-radius: 15px;
                color: white;
                font: bold 12px;
                padding: 8px 16px;
            }
            
            QPushButton:hover {
                background-color: rgba(43, 87, 151, 150);
                border: 2px solid rgba(43, 87, 151, 200);
            }
            
            QPushButton:pressed {
                background-color: rgba(43, 87, 151, 200);
                border: 2px solid rgba(43, 87, 151, 255);
            }
        """)
        
        # Add glow effect
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(43, 87, 151, 150))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)


class AnalogClock(QWidget):
    """
    Analog clock widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Timer for updating clock
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)  # Update every second
        
        self.setWindowTitle("Analog Clock")
        self.resize(200, 200)
        
    def paintEvent(self, event):
        """Paint the clock"""
        side = min(self.width(), self.height())
        time = QTime.currentTime()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)
        
        # Hour hand
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawLine(0, 0, 0, -50)
        painter.restore()
        
        # Minute hand
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawLine(0, 0, 0, -70)
        painter.restore()
        
        # Second hand
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.save()
        painter.rotate(6.0 * time.second())
        painter.drawLine(0, 0, 0, -80)
        painter.restore()
        
        # Hour markers
        painter.setPen(QPen(Qt.black, 2))
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)
            
        # Center dot
        painter.setPen(QPen(Qt.black, 3))
        painter.drawPoint(0, 0)


class CustomDial(QDial):
    """
    Custom styled dial widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set styling
        self.setStyleSheet("""
            QDial {
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, 
                    stop:0 rgba(43, 87, 151, 255), 
                    stop:0.5 rgba(85, 170, 255, 255), 
                    stop:1 rgba(43, 87, 151, 255));
                border: 2px solid rgba(255, 255, 255, 50);
                border-radius: 50px;
            }
        """)


# Test application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    # Test window
    window = QWidget()
    window.setWindowTitle("Custom Widgets Test")
    window.resize(400, 300)
    
    layout = QVBoxLayout(window)
    
    # Add test widgets
    toggle = AnimatedToggle(window)
    layout.addWidget(toggle)
    
    progress = CircularProgressBar(window)
    progress.set_value(75)
    layout.addWidget(progress)
    
    button = GlowButton("Glow Button", window)
    layout.addWidget(button)
    
    clock = AnalogClock(window)
    layout.addWidget(clock)
    
    window.show()
    sys.exit(app.exec_())