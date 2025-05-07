from pydub import AudioSegment
from pydub.utils import which
import os
from logger import log_info, log_success, log_warning, log_error, log_to_file

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe   = which("ffprobe")

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
