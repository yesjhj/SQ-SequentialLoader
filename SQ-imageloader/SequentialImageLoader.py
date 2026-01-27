import os
import torch
import numpy as np
from PIL import Image, ImageOps


class LoadImagesSequentially:
    """顺序读取图片节点 - 使用种子控制索引"""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "seed_mode": (["increment", "decrement", "randomize", "fixed"],),
                "sort_by": (["name", "created_time", "modified_time", "none"],),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("image", "mask_image", "current_index", "total_images", "seed")
    FUNCTION = "load_sequential"

    CATEGORY = "SQ"

    def load_sequential(self, folder_path: str, seed: int = 0, seed_mode: str = "increment", sort_by: str = "name"):
        # 确保文件夹路径存在
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Directory '{folder_path}' cannot be found.")

        # 获取所有图片文件
        img_files = self.getImagePaths(folder_path, sort_by)
        total_images = len(img_files)

        # 使用种子作为索引（取模确保在范围内）
        image_index = seed % total_images

        # 加载指定索引的图片
        image_path = img_files[image_index]

        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        # 创建对应的mask（全0）
        mask = image.clone()
        mask.fill_(0)

        return (image, mask, image_index, total_images, seed)

    def getImagePaths(self, imageDir, sort_by="name"):
        if not os.path.isdir(imageDir):
            raise FileNotFoundError(f"Directory '{imageDir}' cannot be found.")

        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

        img_files = []
        for file in os.listdir(imageDir):
            if file.lower().endswith(supported_formats):
                img_files.append(file)

        if len(img_files) == 0:
            raise FileNotFoundError(f"No supported image files found in directory '{imageDir}'. Supported formats: {supported_formats}")

        # 根据排序方式排序
        if sort_by == "name":
            img_files = sorted(img_files)
        elif sort_by == "created_time":
            img_files = sorted(img_files, key=lambda x: os.path.getctime(os.path.join(imageDir, x)))
        elif sort_by == "modified_time":
            img_files = sorted(img_files, key=lambda x: os.path.getmtime(os.path.join(imageDir, x)))
        # sort_by == "none" 时保持文件系统返回的原始顺序

        img_files = [os.path.join(imageDir, x) for x in img_files]

        return img_files
