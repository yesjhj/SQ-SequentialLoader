# ComfyUI Sequential Image Loader

A ComfyUI custom node for loading images sequentially from a folder.

一个用于从文件夹顺序加载图片的 ComfyUI 自定义节点。

## Features / 功能

- Load images from a specified folder path / 从指定文件夹路径加载图片
- Seed-based index control for sequential access / 基于种子值控制索引，实现顺序访问
- Multiple sorting options / 多种排序方式：按名称、创建时间、修改时间或原始顺序
- Supports formats / 支持格式：PNG, JPG, JPEG, BMP, GIF, WEBP

## Installation / 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/bruefire/ComfyUI-SeqImageLoader.git
```

## Node: Sequential Image Loader / 节点说明

### Inputs / 输入

| Parameter | Type | Description / 说明 |
|-----------|------|-------------|
| folder_path | STRING | Path to image folder / 图片文件夹路径 |
| seed | INT | Index control value / 索引控制值 (0 ~ max) |
| seed_mode | LIST | increment / decrement / randomize / fixed |
| sort_by | LIST | name / created_time / modified_time / none |

### Outputs / 输出

| Output | Type | Description / 说明 |
|--------|------|-------------|
| image | IMAGE | Current loaded image / 当前加载的图片 |
| mask_image | IMAGE | Empty mask (all zeros) / 空遮罩（全零） |
| current_index | INT | Current image index / 当前图片索引 |
| total_images | INT | Total images in folder / 文件夹中图片总数 |
| seed | INT | Current seed value / 当前种子值 |

## Usage / 使用方法

1. Add "Sequential Image Loader" node (Category: SQ) / 添加节点（分类：SQ）
2. Set `folder_path` to your image directory / 设置图片文件夹路径
3. Use `seed` to control which image to load (index = seed % total_images) / 使用种子值控制加载哪张图片
4. Choose `sort_by` to determine image ordering / 选择排序方式

## License / 许可证

MIT License
