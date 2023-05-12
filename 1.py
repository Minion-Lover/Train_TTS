import os
from pydub import AudioSegment
LOGIN_URL = "https://revoicer.app/user/login"
DOWNLOAD_DIR = "C:/Users/Administrator/Downloads"
WAV_DIR = "corpus/nate/angry/wav"
import ffmpeg
import subprocess
# converting mp3 to wav file


def mp3_to_wav(wav_file):
    file_name = ""
    file_names = os.listdir(DOWNLOAD_DIR)
    for fn in file_names:
        if ".mp3" in fn:
            file_name = fn
            break
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    print(file_path)
    target_path = os.path.join(WAV_DIR, wav_file) + ".wav"
    input_video = ffmpeg.input(file_path)
    output_video = ffmpeg.output(input_video, target_path, vcodec='wav')
    ffmpeg.run(output_video)

    
    # _command = f"ffmpeg -i \"{file_path}\" -ss 00:00:00.000 -vframes 1 \"{target_path}\""
    # os.system(_command)
    os.remove(file_path)

if __name__ == "__main__":
    mp3_to_wav("11111111111111111111111111")