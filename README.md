# SQ-ImageLoader

ComfyUI 自定义节点插件，提供顺序加载图片和视频的功能。

## 安装

将此文件夹放入 `ComfyUI/custom_nodes/` 目录下，重启 ComfyUI 即可。

### 依赖

- `opencv-python` - 视频加载功能需要（`pip install opencv-python`）

## 节点说明

### SQ-SequentialLoader（顺序图片加载器）

从指定文件夹中顺序读取图片，通过种子值控制当前读取的图片索引。

**输入参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| folder_path | STRING | 图片文件夹路径 |
| seed | INT | 种子值，用于控制读取哪张图片 |
| seed_mode | LIST | 种子模式：increment（递增）、decrement（递减）、randomize（随机）、fixed（固定） |
| sort_by | LIST | 排序方式：name（文件名）、created_time（创建时间）、modified_time（修改时间）、none（原始顺序） |

**输出：**
| 输出 | 类型 | 说明 |
|------|------|------|
| image | IMAGE | 加载的图片 |
| mask_image | IMAGE | 空白遮罩 |
| current_index | INT | 当前图片索引 |
| total_images | INT | 图片总数 |
| seed | INT | 当前种子值 |

**支持格式：** PNG, JPG, JPEG, BMP, GIF, WEBP

---

### SQ-VideoFileLoader（视频文件加载器）

从视频文件或文件夹中加载视频帧，支持帧率控制、尺寸调整等功能。

**输入参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| path | STRING | 视频文件路径或包含视频的文件夹路径 |
| seed | INT | 种子值，用于控制读取哪个视频（文件夹模式） |
| seed_mode | LIST | 种子模式：increment、decrement、randomize、fixed |
| sort_by | LIST | 排序方式：name、created_time、modified_time、none |
| force_rate | INT | 强制输出帧率（默认24） |
| custom_width | INT | 自定义宽度（0=保持原始） |
| custom_height | INT | 自定义高度（0=保持原始） |
| frame_load_cap | INT | 最大加载帧数（0=无限制） |
| skip_first_frames | INT | 跳过开头帧数 |
| select_every_nth | INT | 每N帧选取一帧 |
| format | LIST | 输出格式：AnimateDiff、VideoHelperSuite、raw |

**输出：**
| 输出 | 类型 | 说明 |
|------|------|------|
| 图像 | IMAGE | 视频帧序列 |
| 帧计数 | INT | 加载的帧数 |
| 音频 | AUDIO | 音频（暂未实现） |
| 视频信息 | STRING | 视频元信息 |
| 视频路径 | STRING | 当前视频文件路径 |
| 当前索引 | INT | 当前视频索引 |
| 视频总数 | INT | 文件夹中视频总数 |

**支持格式：** MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V

## 使用技巧

### 批量处理工作流

1. 将 `seed_mode` 设为 `increment`
2. 使用 ComfyUI 的队列功能批量执行
3. 每次执行会自动加载下一个文件

### 随机选择

将 `seed_mode` 设为 `randomize`，每次执行随机选择一个文件。

### 指定文件

将 `seed_mode` 设为 `fixed`，通过手动设置 `seed` 值来指定加载第几个文件。

## 开发心得

这个插件的核心设计思路是使用 **种子值（seed）** 来控制文件索引，而不是在节点内部维护状态。这样做的好处是：

1. **可预测性** - 相同的种子值总是加载相同的文件
2. **可控性** - 用户可以通过 seed_mode 灵活控制遍历方式
3. **兼容性** - 与 ComfyUI 的队列系统完美配合

视频加载器使用 OpenCV 进行帧提取，支持帧率转换和尺寸调整，适合与 AnimateDiff 等视频生成工作流配合使用。

## License

MIT License
