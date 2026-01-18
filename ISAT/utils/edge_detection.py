# -*- coding: utf-8 -*-
# @Author  : LG

import cv2
import numpy as np
from typing import Tuple, Optional, Dict, List
import hashlib
import time
from functools import lru_cache


class EdgeDetector:
    """
    边缘检测工具类，支持多种边缘检测算法和缓存机制
    """
    
    def __init__(self):
        self._edge_cache: Dict[str, np.ndarray] = {}
        self._cache_max_size = 10  # 最大缓存数量
        self._cache_access_times: Dict[str, float] = {}
        
    def _generate_image_hash(self, image: np.ndarray) -> str:
        """
        生成图像的唯一哈希值用于缓存键
        
        Args:
            image (np.ndarray): 输入图像
            
        Returns:
            str: 图像哈希值
        """
        # 使用图像的形状、数据类型和部分像素生成哈希
        sample_pixels = image[::max(1, image.shape[0]//100), ::max(1, image.shape[1]//100)]
        hash_input = f"{image.shape}_{image.dtype}_{sample_pixels.tobytes()}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _clean_cache(self):
        """
        清理最旧的缓存项，保持缓存大小在限制范围内
        """
        if len(self._edge_cache) > self._cache_max_size:
            # 按访问时间排序，删除最旧的项
            sorted_items = sorted(self._cache_access_times.items(), key=lambda x: x[1])
            for key, _ in sorted_items[:len(self._edge_cache) - self._cache_max_size + 1]:
                if key in self._edge_cache:
                    del self._edge_cache[key]
                if key in self._cache_access_times:
                    del self._cache_access_times[key]
    
    def _update_cache_access(self, key: str):
        """
        更新缓存访问时间
        
        Args:
            key (str): 缓存键
        """
        self._cache_access_times[key] = time.time()
    
    def detect_canny_edges(self, 
                          image: np.ndarray, 
                          low_threshold: int = 50, 
                          high_threshold: int = 150,
                          use_cache: bool = True) -> np.ndarray:
        """
        使用Canny算法检测边缘
        
        Args:
            image (np.ndarray): 输入图像
            low_threshold (int): Canny算法低阈值
            high_threshold (int): Canny算法高阈值
            use_cache (bool): 是否使用缓存
            
        Returns:
            np.ndarray: 边缘图像（二值图像）
        """
        if use_cache:
            cache_key = f"canny_{self._generate_image_hash(image)}_{low_threshold}_{high_threshold}"
            if cache_key in self._edge_cache:
                self._update_cache_access(cache_key)
                return self._edge_cache[cache_key]
        
        # 转换为灰度图像
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # 应用高斯模糊减少噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny边缘检测
        edges = cv2.Canny(blurred, low_threshold, high_threshold)
        
        if use_cache:
            self._edge_cache[cache_key] = edges
            self._update_cache_access(cache_key)
            self._clean_cache()
        
        return edges
    
    def detect_sobel_edges(self, 
                          image: np.ndarray, 
                          kernel_size: int = 3,
                          threshold: int = 100,
                          use_cache: bool = True) -> np.ndarray:
        """
        使用Sobel算法检测边缘
        
        Args:
            image (np.ndarray): 输入图像
            kernel_size (int): Sobel核大小（奇数）
            threshold (int): 边缘阈值
            use_cache (bool): 是否使用缓存
            
        Returns:
            np.ndarray: 边缘图像（二值图像）
        """
        if use_cache:
            cache_key = f"sobel_{self._generate_image_hash(image)}_{kernel_size}_{threshold}"
            if cache_key in self._edge_cache:
                self._update_cache_access(cache_key)
                return self._edge_cache[cache_key]
        
        # 转换为灰度图像
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
        
        # 计算x和y方向的Sobel梯度
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
        
        # 计算梯度幅值
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # 归一化到0-255范围
        gradient_magnitude = np.uint8(gradient_magnitude / gradient_magnitude.max() * 255)
        
        # 应用阈值
        edges = np.where(gradient_magnitude > threshold, 255, 0).astype(np.uint8)
        
        if use_cache:
            self._edge_cache[cache_key] = edges
            self._update_cache_access(cache_key)
            self._clean_cache()
        
        return edges
    
    def get_edge_points(self, edges: np.ndarray) -> List[Tuple[int, int]]:
        """
        从边缘图像中提取边缘点坐标
        
        Args:
            edges (np.ndarray): 边缘图像（二值图像）
            
        Returns:
            List[Tuple[int, int]]: 边缘点坐标列表 [(x, y), ...]
        """
        # 找到边缘点的坐标
        edge_points = np.column_stack(np.where(edges > 0))
        
        # 转换为(x, y)格式并返回为列表
        return [(int(point[1]), int(point[0])) for point in edge_points]
    
    def find_nearest_edge_point(self, 
                               edges: np.ndarray, 
                               query_point: Tuple[int, int], 
                               max_distance: int = 10) -> Optional[Tuple[int, int]]:
        """
        查找距离查询点最近的边缘点
        
        Args:
            edges (np.ndarray): 边缘图像（二值图像）
            query_point (Tuple[int, int]): 查询点坐标 (x, y)
            max_distance (int): 最大搜索距离
            
        Returns:
            Optional[Tuple[int, int]]: 最近的边缘点坐标，如果没找到返回None
        """
        x, y = query_point
        
        # 获取搜索区域的边界
        height, width = edges.shape
        x_min = max(0, x - max_distance)
        x_max = min(width, x + max_distance + 1)
        y_min = max(0, y - max_distance)
        y_max = min(height, y + max_distance + 1)
        
        # 提取搜索区域
        search_region = edges[y_min:y_max, x_min:x_max]
        
        # 如果搜索区域内没有边缘点，直接返回
        if not np.any(search_region > 0):
            return None
        
        # 找到搜索区域内的所有边缘点
        edge_points = np.column_stack(np.where(search_region > 0))
        
        # 计算距离并找到最近的点
        distances = np.sqrt((edge_points[:, 1] + x_min - x)**2 + (edge_points[:, 0] + y_min - y)**2)
        min_idx = np.argmin(distances)
        
        if distances[min_idx] <= max_distance:
            nearest_y, nearest_x = edge_points[min_idx]
            return (nearest_x + x_min, nearest_y + y_min)
        
        return None
    
    def clear_cache(self):
        """
        清空所有缓存
        """
        self._edge_cache.clear()
        self._cache_access_times.clear()
    
    def get_cache_info(self) -> Dict[str, any]:
        """
        获取缓存信息
        
        Returns:
            Dict[str, any]: 缓存统计信息
        """
        return {
            "cache_size": len(self._edge_cache),
            "max_size": self._cache_max_size,
            "cached_keys": list(self._edge_cache.keys())
        }


# 全局边缘检测器实例
_edge_detector = EdgeDetector()


def get_edge_detector() -> EdgeDetector:
    """
    获取全局边缘检测器实例
    
    Returns:
        EdgeDetector: 边缘检测器实例
    """
    return _edge_detector


def detect_edges(image: np.ndarray, 
                method: str = "canny", 
                **kwargs) -> np.ndarray:
    """
    便捷函数：检测图像边缘
    
    Args:
        image (np.ndarray): 输入图像
        method (str): 检测方法 ("canny" 或 "sobel")
        **kwargs: 算法参数
        
    Returns:
        np.ndarray: 边缘图像
    """
    detector = get_edge_detector()
    
    if method.lower() == "canny":
        return detector.detect_canny_edges(image, **kwargs)
    elif method.lower() == "sobel":
        return detector.detect_sobel_edges(image, **kwargs)
    else:
        raise ValueError(f"不支持的边缘检测方法: {method}")
