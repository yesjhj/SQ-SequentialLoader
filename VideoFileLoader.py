import os
import torch
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


class LoadVideoFile:
    """视频文件加载器 - 支持文件夹或单个视频文件，使用种子控制索引"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "seed_mode": (["increment", "decrement", "randomize", "fixed"],),
                "sort_by": (["name", "created_time", "modified_time", "none"],),
                "force_rate": ("INT", {"default": 24, "min": 1, "max": 120, "step": 1}),
                "custom_width": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
                "custom_height": ("INT", {"default": 0, "min": 0, "max": 8192, "step": 1}),
                "frame_load_cap": ("INT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
                "skip_first_frames": ("INT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
                "select_every_nth": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),
                "format": (["AnimateDiff", "VideoHelperSuite", "raw"],),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "AUDIO", "STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("图像", "帧计数", "音频", "视频信息", "视频路径", "当前索引", "视频总数")
    FUNCTION = "load_video"
    CATEGORY = "SQ"

    def get_video_files(self, folder_path, sort_by):
        """获取文件夹中的所有视频文件"""
        supported_formats = ('.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v')
        
        video_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith(supported_formats):
                video_files.append(file)
        
        if len(video_files) == 0:
            raise FileNotFoundError(f"No video files found in '{folder_path}'. Supported: {supported_formats}")

        # 根据排序方式排序
        if sort_by == "name":
            video_files = sorted(video_files)
        elif sort_by == "created_time":
            video_files = sorted(video_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
        elif sort_by == "modified_time":
            video_files = sorted(video_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
        # sort_by == "none" 时保持文件系统返回的原始顺序
        
        video_files = [os.path.join(folder_path, x) for x in video_files]
        return video_files

    def load_video(self, path: str, seed: int = 0, seed_mode: str = "increment", 
                   sort_by: str = "name", force_rate: int = 24,
                   custom_width: int = 0, custom_height: int = 0, frame_load_cap: int = 0,
                   skip_first_frames: int = 0, select_every_nth: int = 1,
                   format: str = "AnimateDiff"):
        
        if not HAS_CV2:
            raise ImportError("opencv-python is required. Please install it with: pip install opencv-python")
        
        # 判断是文件夹还是文件
        if os.path.isdir(path):
            video_files = self.get_video_files(path, sort_by)
            total_videos = len(video_files)
            
            # 使用种子作为索引（取模确保在范围内）
            current_index = seed % total_videos
            video_path = video_files[current_index]
            
        elif os.path.isfile(path):
            video_path = path
            current_index = 0
            total_videos = 1
        else:
            raise FileNotFoundError(f"Path '{path}' cannot be found.")
        
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file '{video_path}'")

        # 获取视频信息
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / original_fps if original_fps > 0 else 0
        
        video_info = f"File: {os.path.basename(video_path)}, FPS: {original_fps:.2f}, Frames: {total_frames}, Size: {width}x{height}, Duration: {duration:.2f}s"
        
        # 计算帧率采样
        frame_skip = max(1, int(original_fps / force_rate)) if force_rate > 0 else 1
        
        # 跳过开头帧
        start_frame = skip_first_frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames = []
        frame_count = 0
        current_frame_num = start_frame
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 每N帧选择一帧
            if (current_frame_num - start_frame) % select_every_nth == 0:
                # 帧率采样
                if frame_count % frame_skip == 0:
                    # BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # 自定义尺寸
                    if custom_width > 0 and custom_height > 0:
                        frame_rgb = cv2.resize(frame_rgb, (custom_width, custom_height), interpolation=cv2.INTER_LANCZOS4)
                    elif custom_width > 0:
                        ratio = custom_width / frame_rgb.shape[1]
                        new_height = int(frame_rgb.shape[0] * ratio)
                        frame_rgb = cv2.resize(frame_rgb, (custom_width, new_height), interpolation=cv2.INTER_LANCZOS4)
                    elif custom_height > 0:
                        ratio = custom_height / frame_rgb.shape[0]
                        new_width = int(frame_rgb.shape[1] * ratio)
                        frame_rgb = cv2.resize(frame_rgb, (new_width, custom_height), interpolation=cv2.INTER_LANCZOS4)
                    
                    frames.append(frame_rgb)
                    
                    # 检查帧数限制
                    if frame_load_cap > 0 and len(frames) >= frame_load_cap:
                        break
                
                frame_count += 1
            
            current_frame_num += 1
        
        cap.release()
        
        if len(frames) == 0:
            raise ValueError(f"No frames extracted from video '{video_path}'")
        
        # 转换为tensor
        frames_np = np.array(frames).astype(np.float32) / 255.0
        images = torch.from_numpy(frames_np)
        
        frame_count_out = len(frames)
        
        # 音频占位
        audio = None
        
        return (images, frame_count_out, audio, video_info, video_path, current_index, total_videos)
