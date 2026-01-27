[README_CN.md](https://github.com/user-attachments/files/24879601/README_CN.md)
# SQ-SequentialLoader

## 简介

SQ-SequentialLoader 是一个用于 ComfyUI 的自定义节点，可以通过种子值控制顺序读取文件夹中的图片文件。

## 功能特点

- 顺序加载文件夹中的图片
- 使用种子值控制图片索引，方便在不同批次之间保持同步
- 支持多种种子模式：递增、递减、随机、固定
- 支持多种排序方式：文件名、创建时间、修改时间
- 自动返回当前索引和总图片数，方便循环处理

## 安装

将此文件夹放置到 ComfyUI 的 `custom_nodes/` 目录下即可。

## 使用方法

### 节点信息

- **节点名称**: SQ-SequentialLoader
- **分类**: SQ

### 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| folder_path | STRING | - | 图片所在文件夹路径 |
| seed | INT | 0 | 种子值，用于控制图片索引 |
| seed_mode | STRING | increment | 种子模式，可选：increment（递增）、decrement（递减）、randomize（随机）、fixed（固定） |
| sort_by | STRING | name | 排序方式，可选：name（文件名）、created_time（创建时间）、modified_time（修改时间）、none（不排序） |

### 输出参数

| 输出 | 类型 | 说明 |
|------|------|------|
| image | IMAGE | 加载的图片张量 |
| mask_image | IMAGE | 对应的遮罩图片（全0） |
| current_index | INT | 当前图片的索引 |
| total_images | INT | 文件夹中的图片总数 |
| seed | INT | 使用的种子值 |

### 使用技巧

1. **索引计算**: 图片索引通过 `seed % total_images` 计算，确保索引始终在有效范围内
2. **循环处理**: 通过递增种子值可以实现图片的循环遍历
3. **批量处理**: 配合 ComfyUI 的循环或批处理功能，可以高效处理多张图片

## 支持的图片格式

- .png
- .jpg / .jpeg
- .bmp
- .gif
- .webp

## 示例工作流

1. 设置 `folder_path` 为包含图片的文件夹
2. 设置初始 `seed` 值（如 0）
3. 设置 `sort_by` 为 "name" 以按文件名排序
4. 连接输出到后续处理节点
5. 如需处理下一张图片，递增 seed 值即可

## 注意事项

- 确保文件夹路径正确且存在
- 文件夹中至少需要包含一张支持的图片格式
- seed 值会自动取模处理，超出范围时自动循环
