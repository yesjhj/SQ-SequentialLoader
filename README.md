# ComfyUI-SeqImageLoader

![icon](docs/icon.png)

A ComfyUI extension node for loading video frames in bulk and performing masking/sketching on each frame through a GUI editor.

## Features

- **Sequential Image Loading**: Load images from a folder sequentially with customizable sorting options
- **Video Frame Extraction**: Extract frames directly from video files (MP4)
- **Built-in Mask Editor**: Draw masks and sketches on each frame with an intuitive GUI
- **Magic Wand Tool**: Quick selection tool for efficient masking
- **Undo/Redo Support**: Full history support for mask editing
- **Multiple Sorting Options**: Sort by name, creation time, modification time, or keep original order

![Demo](docs/dogcat.gif)

## Installation

### Via ComfyUI Manager (Recommended)

Search for `SQ-ImageLoader` in ComfyUI Manager and install.

### Manual Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/bruefire/ComfyUI-SeqImageLoader.git
```

Restart ComfyUI after installation.

## Nodes

### Sequential Image Loader

Load images from a folder one by one, controlled by seed value.

**Inputs:**
- `folder_path`: Path to the image folder
- `seed`: Index control (use with seed_mode)
- `seed_mode`: increment / decrement / randomize / fixed
- `sort_by`: name / created_time / modified_time / none

**Outputs:**
- `image`: Current frame image
- `mask_image`: Mask for the current frame
- `current_index`: Current image index
- `total_images`: Total number of images
- `seed`: Current seed value

### VFrame Loader With Mask Editor

Upload image sequences and edit masks/sketches through the built-in editor.

### Video Loader With Mask Editor

Load video files directly and extract frames for mask editing.

## Mask Editor Usage

1. Right-click on the node and select "Open in MaskEditor"
2. Use left mouse button to draw mask
3. Use right mouse button to erase
4. Use `[` and `]` keys to adjust brush size
5. Use arrow keys to navigate between frames
6. Click ✨ to toggle Magic Wand mode
7. Switch between "inpaint" and "sketch" modes

**Keyboard Shortcuts:**
- `[` / `]`: Decrease / Increase brush size
- `←` / `→`: Previous / Next frame
- `Alt + Z`: Undo
- `Alt + Shift + Z`: Redo
- `Enter`: Save

## Supported Formats

**Images:** PNG, JPG, JPEG, BMP, GIF, WEBP

**Videos:** MP4 (and other formats supported by browser)

## Sample Workflows

Check the `sample_workflows` folder for example workflows:
- `cat2dog_with_animatediff.json`
- `faceswap_masking_helper.json`
- `wan_video_wrapper.json`

## License

MIT License - see [LICENSE.txt](LICENSE.txt)

## Links

- [GitHub Repository](https://github.com/bruefire/ComfyUI-SeqImageLoader)
- [ComfyUI Registry](https://comfyregistry.org)
