<h1 align='center'>ISAT_with_segment_anything [isat-sam]</h1>
<h2 align='center'>一款基于SAM的交互式半自动图像分割标注工具</h2>
<p align='center'>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/stargazers' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/stars/yatengLG/ISAT_with_segment_anything"></a>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/forks' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/forks/yatengLG/ISAT_with_segment_anything"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/isat-sam?style=social&logo=pypi"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/isat-sam?style=social&logo=pypi"></a>
</p>
<p align='center'>
<b>⭐️ 如果你觉得这个项目有用，欢迎点个 Star 支持一下！ ⭐️</b>
</p>
<p align='center'>
    <a href='README-cn.md'><b>[中文]</b></a>
    <a href='README.md'><b>[English]</b></a>
</p>
<p align='center'><img src="./display/software.gif" alt="software.gif"></p>

专注于图像分割领域，我们致力于打造最好的图像分割标注软件。

请查阅我们最新的[中文文档](https://isat-sam.readthedocs.io/zh-cn/latest/) 或 [Documentation in English](https://isat-sam.readthedocs.io/en/latest/#)

---

# 更新
- **🆕 新增边缘检测与自动吸附功能**
    
    <details>
        <summary>边缘检测与自动吸附</summary>
        <p>增强多边形标注功能，支持智能边缘检测和自动吸附。在绘制多边形时按住 <kbd>Alt</kbd> 键，顶点将自动吸附到附近的边缘。</p>
        <h4>核心特性：</h4>
        <ul>
            <li>🎯 <strong>智能边缘检测</strong>：使用Canny和Sobel算法进行精确边缘检测</li>
            <li>⚡ <strong>实时吸附</strong>：顶点自动吸附到可配置距离内的最近边缘</li>
            <li>🚀 <strong>高性能</strong>：智能缓存机制，确保大图像上的流畅操作</li>
            <li>🔧 <strong>可配置</strong>：可调节吸附距离和检测参数</li>
            <li>🎨 <strong>无缝集成</strong>：与现有的Shift+角度约束功能完美配合</li>
        </ul>
        <h4>使用方法：</h4>
        <ol>
            <li>切换到多边形标注模式</li>
            <li>绘制时按住 <kbd>Alt</kbd> 键</li>
            <li>顶点将自动吸附到附近边缘</li>
            <li>松开 <kbd>Alt</kbd> 键禁用吸附</li>
        </ol>
        <p><em>此功能显著提升了处理复杂物体边界时的标注精度和效率。</em></p>
    </details>

- **V1.5.2版本，支持基于sam3的视觉提示（visual prompt）功能**
    <details>
        <summary>视觉提示</summary>
            <p align='center'><img src="./display/visual_prompt.gif" alt="visual_prompt.gif"></p>
    </details>

- **V1.5.0版本，支持SAM3模型，并添加了文本提示（text prompt）功能**

    <details>
        <summary>文本提示</summary>
            <h3>单类别</h3>
                <p align='center'><img src="./display/text_prompt1.gif" alt="text_prompt1.gif"></p>
            <h3>多类别</h3>
                <p align='center'><img src="./display/text_prompt2.gif" alt="text_prompt2.gif"></p>
    </details>

- **V1.4.0版本添加了插件系统。** 可以使用较少量的代码，扩展ISAT的功能。
  
    以下是一些插件示例:
  - [ISAT_plugin_auto_annotate](https://github.com/yatengLG/ISAT_plugin_auto_annotate) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-auto-annotate?style=social&logo=pypi)
 ![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-auto-annotate?style=social) : 仅用240行代码实现的**自动标注**功能（使用yolo模型）。
  - [ISAT_plugin_mask_export](https://github.com/yatengLG/ISAT_plugin_mask_export) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-mask-export?style=social&logo=pypi)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-mask-export?style=social) : 仅用160行代码实现的**mask导出**功能。

- 其他版本以及更新日志，请查阅[发布页](https://github.com/yatengLG/ISAT_with_segment_anything/releases)

# 安装

- 新建conda环境（推荐，可选）
    ```shell
    # 创建环境
    conda create -n isat_env python=3.8
    
    # 激活环境
    conda activate isat_env
    ```

- 安装
    ```shell
    pip install isat-sam
    ```

- 运行
    ```shell
    isat-sam
    ```

# Star History

**请给该项目一个star，您的点赞就是对我最大的支持与鼓励**
[![Star History Chart](https://api.star-history.com/svg?repos=yatengLG/ISAT_with_segment_anything&type=Date)](https://star-history.com/#yatengLG/ISAT_with_segment_anything&Date)


# 核心贡献者

<table border="0">
<tr>
    <td><img alt="yatengLG" src="https://avatars.githubusercontent.com/u/31759824?v=4" width="60" height="60" href="">
    <td><img alt="Alias-z" src="https://avatars.githubusercontent.com/u/66273343?v=4" width="60" height="60" href="">
    <td>...
</td>
</tr>
<tr>
  <td><a href="https://github.com/yatengLG">yatengLG</a>
  <td><a href="https://github.com/Alias-z">Alias-z</a>
    <td><a href="https://github.com/yatengLG/ISAT_with_segment_anything/graphs/contributors">...</a>
</tr>
</table>


# 引用
```text
@misc{ISAT_with_segment_anything,
  title={{ISAT with Segment Anything: An Interactive Semi-Automatic Annotation Tool}},
  author={Ji, Shuwei and Zhang, Hongyuan},
  url={https://github.com/yatengLG/ISAT_with_segment_anything},
  note={Updated on 2025-02-07},
  year={2024},
  version={1.33}
}
```
