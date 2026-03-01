# 视频批量重命名OCR工具

## 概述

本工具可以从视频的第3秒关键帧中提取文字内容，并使用提取到的文字对视频文件进行重命名。脚本可以自动批量处理当前目录下的所有常见视频格式文件。

## 灵感来源

本项目的灵感来源于 [VideoFrameTextExtractor](https://github.com/tanrivertarik/VideoFrameTextExtractor) 项目，并在其基础上进行了功能扩展和优化。

## 使用方法

1. 将脚本 `video_batch_renamer_ocr.py` 放置在包含视频文件的目录中
2. 确保已安装所需依赖库：`paddleocr`, `opencv-python`
3. 运行脚本：`python video_batch_renamer_ocr.py`

## 支持的视频格式

- .mp4
- .avi  
- .mov
- .mkv
- .wmv
- .flv
- .webm
- .m4v
- .mpg
- .mpeg

## 注意事项

- 脚本会自动跳过已经处理过的文件（以纯数字命名的文件）
- 脚本会处理当前目录下所有支持格式的视频文件
- 如果提取的文本已作为文件名存在于当前目录，脚本会跳过重命名以避免覆盖

## 技术细节

- 使用 OpenCV 读取视频帧
- 使用 PaddleOCR 进行中文光学字符识别
- 提取视频第3秒的关键帧画面进行识别
- 自动过滤提取结果中的特殊字符，确保文件名合法