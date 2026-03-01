# Video Batch Renamer OCR

## Overview

This tool extracts text from the 3rd second keyframe of a video and renames the video file using the extracted text. It can automatically batch process all common video formats in the current directory.

## Inspiration

The idea for this project comes from the [VideoFrameTextExtractor](https://github.com/tanrivertarik/VideoFrameTextExtractor) project, and has been extended and optimized based on it.

## Usage

1. Place the script `video_batch_renamer_ocr.py` in the directory containing the video files.
2. Ensure the required libraries are installed: `paddleocr`, `opencv-python`.
3. Run the script: `python video_batch_renamer_ocr.py.

## Supported Video Formats

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

## Notes

- The script automatically skips processed files (files named with pure numbers).
- The script processes all supported video formats in the current directory.
- If the extracted text already exists as a filename in the current directory, the script will skip renaming to avoid overwriting.

## Technical Details

- Uses OpenCV to read video frames.
- Uses PaddleOCR for Chinese optical character recognition.
- Extracts the keyframe at the 3rd second of the video for recognition.
- Automatically filters special characters from the extraction results to ensure valid filenames.