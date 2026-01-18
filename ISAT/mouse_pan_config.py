# -*- coding: utf-8 -*-
# @Author  : LG

import json
import os

from ISAT.configs import ISAT_ROOT

MOUSE_PAN_CONFIG_FILE = os.path.join(ISAT_ROOT, "mouse_pan_config.json")
"""鼠标中键拖拽配置文件路径"""


def load_mouse_pan_config():
    """
    加载鼠标中键拖拽配置
    
    Returns:
        dict: 配置字典
    """
    default_config = {
        "enable_middle_mouse_pan": True,
        "config_version": "1.0.0"
    }
    
    if not os.path.exists(MOUSE_PAN_CONFIG_FILE):
        save_mouse_pan_config(default_config)
        return default_config
    
    try:
        with open(MOUSE_PAN_CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 确保所有必要的键都存在
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
        return config
    except (json.JSONDecodeError, FileNotFoundError):
        return default_config


def save_mouse_pan_config(config):
    """
    保存鼠标中键拖拽配置
    
    Arguments:
        config (dict): 配置字典
    """
    with open(MOUSE_PAN_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def is_middle_mouse_pan_enabled():
    """
    检查是否启用了中键拖拽功能
    
    Returns:
        bool: 是否启用
    """
    config = load_mouse_pan_config()
    return config.get("enable_middle_mouse_pan", True)


def set_middle_mouse_pan_enabled(enabled):
    """
    设置中键拖拽功能启用状态
    
    Arguments:
        enabled (bool): 是否启用
    """
    config = load_mouse_pan_config()
    config["enable_middle_mouse_pan"] = enabled
    save_mouse_pan_config(config)
