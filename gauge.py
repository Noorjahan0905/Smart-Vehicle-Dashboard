import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
from PyQt5.QtWidgets import QWidget


class AnalogGaugeWidget(QWidget):
    """Analog gauge widget for displaying values with a needle indicator"""
    
    def __init__(self, parent=None):
        super(AnalogGaugeWidget, self).__init__(parent)
        
        self.use_timer_event = False
        self.black = QtCore.Qt.black
        self.white = QtCore.Qt.white
        self.gray = QtCore.Qt.gray
        self.blue = QtCore.Qt.blue
        self.green = QtCore.Qt.green
        self.red = QtCore.Qt.red
        self.yellow = QtCore.Qt.yellow
        
        # Initialize values
        self.value = 0
        self.minValue = 0
        self.maxValue = 1000
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.95
        self.center_horizontal_value = 0
        self.center_vertical_value = 0
        self.gauge_width = 400
        self.gauge_height = 400
        
        # Colors
        self.needle_color = self.red
        self.needle_color_drag = self.red
        self.needle_color_released = self.green
        self.scale_value_color = self.white
        self.display_value_color = self.white
        self.center_point_color = self.black
        
        # Gauge properties
        self.scale_angle_start_value = 135
        self.scale_angle_size = 270
        self.angle_offset = 0
        
        # Scale properties
        self.scala_main_count = 10
        self.scala_subdiv_count = 5
        
        # Visual properties
        self.enable_filled_polygon = True
        self.enable_big_scaled_grid = True
        self.enable_fine_scaled_grid = True
        self.enable_scale_text = True
        self.enable_barGraph = True
        self.enable_value_text = True 
        self.enable_center_point = True
        self.enable_needle_polygon = True
        self.enable_value_text_display = True # This is the flag
        
        # Mouse interaction
        self.mouse_control = False
        self.units = ""
        
        # Set initial size
        self.resize(400, 400)
        
    def set_MaxValue(self, value):
        """Set maximum value for the gauge"""
        if value > self.minValue:
            self.maxValue = value
            
    def set_MinValue(self, value):
        """Set minimum value for the gauge"""
        if value < self.maxValue:
            self.minValue = value
            
    def set_scala_main_count(self, count):
        """Set number of major scale divisions"""
        if count > 0:
            self.scala_main_count = count
            
    def set_DisplayValueColor(self, R, G, B):
        """Set color for displayed value text"""
        self.display_value_color = QtGui.QColor(R, G, B, 255)
        
    def set_NeedleColor(self, R, G, B):
        """Set color for needle"""
        self.needle_color = QtGui.QColor(R, G, B, 255)
        
    def set_NeedleColorDrag(self, R, G, B):
        """Set color for needle when dragging"""
        self.needle_color_drag = QtGui.QColor(R, G, B, 255)
        
    def set_ScaleValueColor(self, R, G, B):
        """Set color for scale values"""
        self.scale_value_color = QtGui.QColor(R, G, B, 255)
        
    def set_CenterPointColor(self, R, G, B):
        """Set color for center point"""
        self.center_point_color = QtGui.QColor(R, G, B, 255)
        
    def set_enable_big_scaled_grid(self, enable):
        """Enable/disable big scale grid"""
        self.enable_big_scaled_grid = enable
        
    def set_enable_barGraph(self, enable):
        """Enable/disable bar graph"""
        self.enable_barGraph = enable
        
    def set_enable_filled_Polygon(self, enable):
        """Enable/disable filled polygon"""
        self.enable_filled_polygon = enable

    # THIS IS THE METHOD THAT WAS MISSING
    def set_enable_value_text_display(self, enable):
        """Enable/disable the display of the value text on the gauge."""
        self.enable_value_text_display = enable
        self.update()
            
    def update_value(self, value):
        """Update the gauge value"""
        if value <= self.maxValue and value >= self.minValue:
            self.value = value
            self.update()
        elif value > self.maxValue:
            self.value = self.maxValue
            self.update()
        else:
            self.value = self.minValue
            self.update()
            
    def value_to_angle(self, value):
        """Convert value to angle"""
        return (self.scale_angle_size * (value - self.minValue) / 
                (self.maxValue - self.minValue) + self.scale_angle_start_value)
    
    def paintEvent(self, event):
        """Paint the gauge"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.gauge_width = self.width()
        self.gauge_height = self.height()
        
        self.center_horizontal_value = self.gauge_width / 2
        self.center_vertical_value = self.gauge_height / 2
        
        self.draw_gauge_background(painter)
        self.draw_scale(painter)
        
        if self.enable_scale_text:
            self.draw_scale_text(painter)
            
        if self.enable_barGraph:
            self.draw_bar_graph(painter)
            
        self.draw_needle(painter)
        
        if self.enable_center_point:
            self.draw_center_point(painter)
            
        # Check the flag here before drawing value text
        if self.enable_value_text and self.enable_value_text_display: 
            self.draw_value_text(painter)
            
    def draw_gauge_background(self, painter):
        """Draw the gauge background"""
        outer_radius = min(self.gauge_width, self.gauge_height) / 2 * 0.95
        inner_radius = outer_radius * 0.85
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor(60, 60, 60)))
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 2))
        painter.drawEllipse(
            int(self.center_horizontal_value - outer_radius),
            int(self.center_vertical_value - outer_radius),
            int(outer_radius * 2),
            int(outer_radius * 2)
        )
        
        painter.setBrush(QtGui.QBrush(QtGui.QColor(40, 40, 40)))
        painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 80), 1))
        painter.drawEllipse(
            int(self.center_horizontal_value - inner_radius),
            int(self.center_vertical_value - inner_radius),
            int(inner_radius * 2),
            int(inner_radius * 2)
        )
        
    def draw_scale(self, painter):
        """Draw the scale marks"""
        if not self.enable_big_scaled_grid:
            return
            
        painter.setPen(QtGui.QPen(self.scale_value_color, 2))
        
        outer_radius = min(self.gauge_width, self.gauge_height) / 2 * 0.9
        inner_radius = outer_radius * 0.85
        
        for i in range(self.scala_main_count + 1):
            angle = (self.scale_angle_start_value + 
                    (self.scale_angle_size / self.scala_main_count) * i) * math.pi / 180
            
            x1 = self.center_horizontal_value + (inner_radius * math.cos(angle))
            y1 = self.center_vertical_value + (inner_radius * math.sin(angle))
            x2 = self.center_horizontal_value + (outer_radius * math.cos(angle))
            y2 = self.center_vertical_value + (outer_radius * math.sin(angle))
            
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
    def draw_scale_text(self, painter):
        """Draw scale text values"""
        painter.setPen(QtGui.QPen(self.scale_value_color))
        painter.setFont(QtGui.QFont("Arial", 10))
        
        text_radius = min(self.gauge_width, self.gauge_height) / 2 * 0.75
        
        for i in range(self.scala_main_count + 1):
            angle = (self.scale_angle_start_value + 
                    (self.scale_angle_size / self.scala_main_count) * i) * math.pi / 180
            
            value = self.minValue + (self.maxValue - self.minValue) / self.scala_main_count * i
            
            x = self.center_horizontal_value + (text_radius * math.cos(angle))
            y = self.center_vertical_value + (text_radius * math.sin(angle))
            
            text = str(int(value))
            fm = painter.fontMetrics()
            text_width = fm.width(text)
            text_height = fm.height()
            
            painter.drawText(int(x - text_width/2), int(y + text_height/4), text)
            
    def draw_bar_graph(self, painter):
        """Draw bar graph representation"""
        outer_radius = min(self.gauge_width, self.gauge_height) / 2 * 0.8
        
        current_angle = self.value_to_angle(self.value)
        
        gradient = QtGui.QConicalGradient(
            self.center_horizontal_value, 
            self.center_vertical_value, 
            self.scale_angle_start_value
        )
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(255, 0, 0))
        
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.transparent))
        
        rect = QtCore.QRectF(
            self.center_horizontal_value - outer_radius,
            self.center_vertical_value - outer_radius,
            outer_radius * 2,
            outer_radius * 2
        )
        
        painter.drawPie(rect, int(self.scale_angle_start_value * 16), 
                       int((current_angle - self.scale_angle_start_value) * 16))
        
    def draw_needle(self, painter):
        """Draw the needle"""
        if not self.enable_needle_polygon:
            return
            
        painter.setBrush(QtGui.QBrush(self.needle_color))
        painter.setPen(QtGui.QPen(self.needle_color))
        
        angle = self.value_to_angle(self.value) * math.pi / 180
        
        needle_length = min(self.gauge_width, self.gauge_height) / 2 * 0.8
        needle_width = 3
        
        tip_x = self.center_horizontal_value + needle_length * math.cos(angle)
        tip_y = self.center_vertical_value + needle_length * math.sin(angle)
        
        base_x1 = self.center_horizontal_value + needle_width * math.cos(angle + math.pi/2)
        base_y1 = self.center_vertical_value + needle_width * math.sin(angle + math.pi/2)
        
        base_x2 = self.center_horizontal_value + needle_width * math.cos(angle - math.pi/2)
        base_y2 = self.center_vertical_value + needle_width * math.sin(angle - math.pi/2)
        
        needle_polygon = QtGui.QPolygonF([
            QtCore.QPointF(tip_x, tip_y),
            QtCore.QPointF(base_x1, base_y1),
            QtCore.QPointF(base_x2, base_y2)
        ])
        
        painter.drawPolygon(needle_polygon)
        
    def draw_center_point(self, painter):
        """Draw center point"""
        painter.setBrush(QtGui.QBrush(self.center_point_color))
        painter.setPen(QtGui.QPen(self.center_point_color))
        
        radius = 8
        painter.drawEllipse(
            int(self.center_horizontal_value - radius),
            int(self.center_vertical_value - radius),
            radius * 2,
            radius * 2
        )
        
    def draw_value_text(self, painter):
        """Draw the current value as text"""
        painter.setPen(QtGui.QPen(self.display_value_color))
        painter.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        
        text = f"{self.value:.1f} {self.units}"
        fm = painter.fontMetrics()
        text_width = fm.width(text)
        
        # Position text below the center point
        x_pos = self.center_horizontal_value - text_width / 2
        y_pos = self.center_vertical_value + min(self.gauge_width, self.gauge_height) / 4 
        
        painter.drawText(int(x_pos), int(y_pos), text)
        
    def resizeEvent(self, event):
        """Handle widget resize"""
        self.update()
        
    def mousePressEvent(self, event):
        """Handle mouse press for interactive control"""
        if self.mouse_control:
            dx = event.x() - self.center_horizontal_value
            dy = event.y() - self.center_vertical_value
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad)
            
            if angle_deg < 0:
                angle_deg += 360
                
            # Normalize angle relative to gauge scale
            # This logic needs to be robust for angles wrapping around 360
            current_value_angle = angle_deg
            
            # Check if the click is within the angular range of the scale
            # Start angle of scale
            start_arc = self.scale_angle_start_value
            # End angle of scale
            end_arc = self.scale_angle_start_value + self.scale_angle_size

            # Handle cases where the arc crosses the 0/360 degree line
            in_range = False
            if start_arc <= end_arc: # Normal case, arc doesn't cross 0/360
                if start_arc <= current_value_angle <= end_arc:
                    in_range = True
            else: # Arc crosses 0/360 (e.g., starts at 270, ends at 90)
                if current_value_angle >= start_arc or current_value_angle <= end_arc % 360 : # end_arc % 360 handles the wrap
                     in_range = True
            
            if in_range:
                # Map angle to value
                # Relative angle from the start of the scale
                relative_angle = current_value_angle - start_arc
                if relative_angle < 0:
                    relative_angle += 360 # Adjust if angle is smaller than start_arc due to wrap

                # Ensure relative_angle is within scale_angle_size
                relative_angle = relative_angle % 360 
                if relative_angle > self.scale_angle_size : # If click is outside arc but was miscalculated as in range
                    # This can happen if scale is small and click is far from it
                    # For simplicity, we might ignore clicks too far out of the desired sweep
                    # or clamp to min/max. Here, we proceed if initial 'in_range' was true.
                    pass


                value = self.minValue + (self.maxValue - self.minValue) * (relative_angle / self.scale_angle_size)
                # Clamp value to min/max as a safeguard
                value = max(self.minValue, min(self.maxValue, value))
                self.update_value(value)