from pydub import AudioSegment
from pydub.utils import which
import os
from logger import log_info, log_success, log_warning, log_error, log_to_file

# Check if ffmpeg and ffprobe are available
FFMPEG_PATH = which("ffmpeg")
FFPROBE_PATH = which("ffprobe")

if not FFMPEG_PATH or not FFPROBE_PATH:
    log_warning("FFmpeg or ffprobe not found in PATH. Audio conversion may fail.")
else:
    AudioSegment.converter = FFMPEG_PATH
    AudioSegment.ffprobe = FFPROBE_PATH
    log_info(f"Using ffmpeg: {FFMPEG_PATH}")
    log_info(f"Using ffprobe: {FFPROBE_PATH}")

def convert_audio(input_file, output_file, output_format, overwrite=False, log_file=None):
    try:
        if os.path.exists(output_file) and not overwrite:
            log_warning(f"File exists: {output_file}. Skipping...")
            return

        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=output_format)

        log_success(f"Converted: {input_file} -> {output_file}")
        if log_file:
            log_to_file(log_file, f"Converted: {input_file} -> {output_file}")
    except Exception as e:
        log_error(f"Failed to convert {input_file}: {e}")
        if log_file:
            log_to_file(log_file, f"Error converting {input_file}: {e}")

def batch_convert(input_folder, output_folder, input_format, output_format, overwrite=False, log_file=None):
    if not os.path.isdir(input_folder):
        log_error(f"Invalid input folder: {input_folder}")
        return

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(f".{input_format.lower()}")
    ]

    if not files:
        log_warning(f"No '.{input_format}' files found in: {input_folder}")
        return

    for file in files:
        input_file = os.path.join(input_folder, file)
        base_name = os.path.splitext(file)[0]
        output_file = os.path.join(output_folder, f"{base_name}.{output_format}")
        convert_audio(input_file, output_file, output_format, overwrite, log_file)
