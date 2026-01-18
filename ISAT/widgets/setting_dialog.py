# -*- coding: utf-8 -*-
# @Author  : LG

from PyQt5 import QtCore, QtGui, QtWidgets

from ISAT.ui.setting_dialog import Ui_Dialog
from ISAT.mouse_pan_config import is_middle_mouse_pan_enabled, set_middle_mouse_pan_enabled


class SettingDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent, mainwindow):
        QtWidgets.QDialog.__init__(self, parent)
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        # 添加中键拖拽复选框
        self.checkBox_middle_mouse_pan = QtWidgets.QCheckBox("启用中键拖拽")
        self.checkBox_middle_mouse_pan.setChecked(is_middle_mouse_pan_enabled())
        self.checkBox_middle_mouse_pan.stateChanged.connect(self.middle_mouse_pan_state_changed)
        
        # 找到合适的位置添加复选框（在现有复选框附近）
        # 这里我们添加到垂直布局中
        if hasattr(self, 'verticalLayout'):
            # 尝试找到现有的垂直布局
            existing_layout = None
            for child in self.findChildren(QtWidgets.QWidget):
                if hasattr(child, 'layout') and child.layout():
                    layout = child.layout()
                    if isinstance(layout, QtWidgets.QVBoxLayout):
                        existing_layout = layout
                        break
            
            if existing_layout:
                # 在现有布局中添加新的复选框
                existing_layout.insertWidget(existing_layout.count() - 2, self.checkBox_middle_mouse_pan)
            else:
                # 如果找不到合适的布局，添加到主布局
                self.verticalLayout.addWidget(self.checkBox_middle_mouse_pan)

        self.checkBox_auto_save.stateChanged.connect(
            self.mainwindow.change_auto_save_state
        )
        self.checkBox_real_time_area.stateChanged.connect(
            self.mainwindow.change_real_time_area_state
        )
        self.checkBox_approx_polygon.stateChanged.connect(
            self.mainwindow.change_approx_polygon_state
        )
        self.checkBox_polygon_invisible.stateChanged.connect(
            self.mainwindow.change_create_mode_invisible_polygon_state
        )
        self.checkBox_show_edge.stateChanged.connect(self.mainwindow.change_edge_state)
        self.checkBox_show_prompt.stateChanged.connect(
            self.mainwindow.change_prompt_visiable
        )
        self.checkBox_use_bfloat16.stateChanged.connect(
            self.mainwindow.change_bfloat16_state
        )
        self.checkBox_use_video_segmentation.stateChanged.connect(
            self.mainwindow.change_use_video_segmentation_state
        )
        self.horizontalSlider_vertex_size.valueChanged.connect(
            self.mainwindow.change_vertex_size
        )
        self.horizontalSlider_mask_alpha.valueChanged.connect(
            self.mainwindow.change_mask_alpha
        )
        self.comboBox_contour_mode.currentIndexChanged.connect(
            self.contour_mode_index_changed
        )
        self.comboBox_contour_method.currentIndexChanged.connect(
            self.contour_method_index_changed
        )
        self.horizontalSlider_polygon_alpha_hover.valueChanged.connect(
            self.mainwindow.change_polygon_alpha_hover
        )
        self.horizontalSlider_polygon_alpha_no_hover.valueChanged.connect(
            self.mainwindow.change_polygon_alpha_no_hover
        )
        self.pushButton_close.clicked.connect(self.close)

    def middle_mouse_pan_state_changed(self, state):
        """中键拖拽状态改变时的处理"""
        enabled = state == QtCore.Qt.Checked
        set_middle_mouse_pan_enabled(enabled)

    def contour_mode_index_changed(self, index):
        if index == 0:
            contour_mode = "external"
        elif index == 1:
            contour_mode = "max_only"
        else:
            contour_mode = "all"
        self.mainwindow.change_contour_mode(contour_mode)

    def contour_method_index_changed(self, index):
        if index == 0:
            contour_method = "SIMPLE"
        elif index == 1:
            contour_method = "TC89_KCOS"
        else:
            contour_method = "NONE"
        self.mainwindow.change_contour_method(contour_method)