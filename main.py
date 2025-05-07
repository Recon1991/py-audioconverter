import argparse
import json
import os
from converter import convert_audio, batch_convert
from logger import log_info, log_warning

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def parse_args():
    parser = argparse.ArgumentParser(description="Audio Converter CLI Tool")
    parser.add_argument("--input", help="Input file or directory")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--in-format", help="Input format (e.g., wav)")
    parser.add_argument("--out-format", help="Output format (e.g., mp3)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--log", help="Log file path")

    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config()

    input_path = args.input or config["input_path"]
    output_path = args.output or config["output_path"]
    in_format = args.in_format or config["input_format"]
    out_format = args.out_format or config["output_format"]
    overwrite = args.overwrite or config.get("overwrite", False)
    log_file = args.log or config.get("log_file", None)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.path.isdir(input_path):
        log_info(f"Processing folder: {input_path}")
        batch_convert(input_path, output_path, in_format, out_format, overwrite, log_file)

        for file in os.listdir(input_path):
            if file.lower().endswith(f".{in_format}"):
                input_file = os.path.join(input_path, file)
                base_name = os.path.splitext(file)[0]
                output_file = os.path.join(output_path, f"{base_name}.{out_format}")
                convert_audio(input_file, output_file, out_format, overwrite, log_file)
    elif os.path.isfile(input_path):
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_file = os.path.join(output_path, f"{base_name}.{out_format}")
        convert_audio(input_path, output_file, out_format, overwrite, log_file)
    else:
        log_warning(f"Input path '{input_path}' is not valid.")

if __name__ == "__main__":
    main()
