import cv2
from paddleocr import PaddleOCR
import os
import glob
import re

# 初始化PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def extract_text_from_video(video_path):
    """
    从视频的第3秒提取左上角的汉字
    """
    print(f"正在处理视频: {video_path}")
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}")
        return []
    
    # 获取视频的FPS和总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 计算第3秒对应的帧索引
    target_frame_index = int(3 * fps)
    
    # 检查视频是否足够长
    if target_frame_index >= total_frames:
        print(f"警告: 视频 {video_path} 长度不足3秒，将在最后一帧进行文字提取。")
        target_frame_index = total_frames - 1
    
    # 跳转到目标帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_index)
    
    # 读取目标帧
    ret, frame = cap.read()
    if not ret:
        print(f"读取视频帧失败: {video_path}")
        cap.release()
        return []
    
    # 定义ROI（感兴趣区域），例如左上角1/4区域
    height, width, _ = frame.shape
    roi = frame[0:int(height*0.5), 0:int(width*0.5)]
    
    # 使用OCR进行文字识别
    result = ocr.ocr(roi, det=True)
    
    # 提取可信度高于0.5的文字
    all_ocr_results = []
    if result and len(result) > 0 and result[0]:
        for item in result[0]:
            text, confidence = item[1]
            if confidence > 0.5:
                all_ocr_results.append(text)
    
    cap.release()
    
    # 去重并返回结果
    unique_texts = list(set(all_ocr_results))
    return unique_texts

def rename_video_based_on_text(video_file):
    """
    根据从视频中提取的文本重命名视频文件
    """
    if not os.path.exists(video_file):
        print(f"警告：视频文件 {video_file} 不存在。")
        return False
        
    extracted_texts = extract_text_from_video(video_file)
    
    if extracted_texts:
        # 使用第一个提取到的文本作为新文件名
        new_name = extracted_texts[0]
        # 确保文件名合法
        new_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if new_name:  # 确保新名称不为空
            # 保留原始文件扩展名
            base_name, ext = os.path.splitext(video_file)
            new_filename = f"{new_name}{ext}"
            
            # 检查新文件名是否已存在
            if os.path.exists(new_filename):
                print(f"文件 {new_filename} 已存在，跳过重命名: {video_file}")
                return False
            
            try:
                os.rename(video_file, new_filename)
                print(f"已将 {video_file} 重命名为 {new_filename}")
                return True
            except OSError as e:
                print(f"重命名失败: {e}")
                return False
        else:
            print("提取的文本不适合作为文件名。")
            return False
    else:
        print(f"{video_file} 中未找到可信的汉字。")
        return False

def is_already_processed(filename):
    """
    检查文件是否已经被处理过（根据文件名判断）
    """
    # 检查是否是以数字开头的文件名，这种通常是原始文件
    name_part = os.path.splitext(filename)[0]
    return bool(re.fullmatch(r'\d+', name_part))

def main():
    # 定义视频文件扩展名
    video_extensions = [
        "*.mp4", "*.avi", "*.mov", "*.mkv", 
        "*.wmv", "*.flv", "*.webm", "*.m4v",
        "*.mpg", "*.mpeg"
    ]
    
    # 获取当前目录下所有视频文件
    video_files = []
    for extension in video_extensions:
        video_files.extend(glob.glob(extension))
    
    # 遍历所有视频文件
    for video_file in video_files:
        # 跳过已处理过的文件（以纯数字命名的视频 - 现在改为保留所有视频文件）
        # if is_already_processed(os.path.basename(video_file)):
        #     continue
        rename_video_based_on_text(video_file)

if __name__ == "__main__":
    main()