from selenium.webdriver import ActionChains
from selenium import webdriver
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from corpus_dir import CORPUS_NATE_ANGRY
import os, time, ffmpeg
from pandas import read_csv
from os import path
from pydub import AudioSegment
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

LOGIN_URL = "https://revoicer.app/user/login"
DOWNLOAD_DIR = "C:/Users/Administrator/Downloads"
WAV_DIR = "corpus/nate/angry/wav"

def read_corpus(root):
    path_to_transcript = dict()
    with open(os.path.join(root, "metadata.csv"), "r", encoding="utf8") as file:
        lookup = file.read()
    for line in lookup.split("\n"):
        if line.strip() != "":
            norm_transcript = line.split("|")[1]
            wav_path = os.path.join(root, "wav", line.split("|")[0] + ".wav")
            path_to_transcript[wav_path] = norm_transcript
    return path_to_transcript

def login_revoicer():
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(LOGIN_URL)

    try:
        email_edit = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginemail"]')))
        email_edit.send_keys('perfomancedev@gmail.com')
        time.sleep(1)
        email_edit = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginpassword"]')))
        email_edit.send_keys('rlBKAyXfqj0Ks')
        time.sleep(1)
        login_btn = WebDriverWait(driver, 1000).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="login_button"]')))
        login_btn.click()
        time.sleep(1)
        select_nova = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ttsVoiceen-US-SaraNeural"]/div/div[2]/p')))
        select_nova.click()
        time.sleep(1)

    except:
        pass
    
    return driver

def mp3_to_wav(wav_file):
    file_name = ""
    
    flag = 1
    while flag:
        file_names = os.listdir(DOWNLOAD_DIR)
        print(file_names)
        for fn in file_names:
            if "Nova" in fn:
                file_name = fn
                flag = 0
                break
        time.sleep(0.3)
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    target_path = wav_file
    # input_video = ffmpeg.input(file_path)
    # output_video = ffmpeg.output(input_video, target_path, vcodec='wav')
    # ffmpeg.run(output_video)

    _command = f"ffmpeg -i \"{file_path}\" -ss 00:00:00.000 -vframes 1 \"{target_path}\""
    os.system(_command)

    os.remove(file_path)

def get_audio(driver, wav_file, text):
    text_editor = WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bubble-editor"]/div[1]')))
    text_editor.send_keys(text)
    time.sleep(0.3)

    generate_audio = WebDriverWait(driver, 20000).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="generate_now"]')))
    generate_audio[0].click()
    time.sleep(3)  
    
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    generate_ok = WebDriverWait(driver, 10000, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[5]/div/div[3]/button[1]')))
    generate_ok[0].click()
    time.sleep(0.3)
    
    body = WebDriverWait(driver, 5000).until(EC.presence_of_all_elements_located((By.XPATH, '//body')))
    body[0].click()
    body[0].send_keys(Keys.END)
    time.sleep(0.3)

    download_btn = WebDriverWait(driver, 10000).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="generated_row"]/div/div/div/div[2]/div/div[2]/div/a')))
    download_btn[0].click()
    time.sleep(11)

    select_all = WebDriverWait(driver, 10000).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="select_all_voices"]/span[2]')))
    select_all[0].click()
    time.sleep(0.3)

    delete_all = WebDriverWait(driver, 10000).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="delete_selected_voices"]')))
    delete_all[0].click()
    time.sleep(1)

    delete_all_audio = WebDriverWait(driver, 10000).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[5]/div/div[3]/button[1]')))
    delete_all_audio[0].click()
    time.sleep(3)
 
    delete_ok = WebDriverWait(driver, 50000).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[5]/div/div[3]/button[1]')))
    delete_ok[0].click()
    time.sleep(1)    
    
    text_editor.send_keys(Keys.CONTROL+"A")
    time.sleep(0.5)    
    text_editor.send_keys(Keys.DELETE)
    mp3_to_wav(wav_file)
    return

def _main():
    path_to_transcript = read_corpus(root = CORPUS_NATE_ANGRY)
    wav_names = list(path_to_transcript.keys())
    texts = list(path_to_transcript.values())

    driver = login_revoicer()
    limit = len(os.listdir(WAV_DIR)) + 11000
    for i, wav_file in enumerate(wav_names):
        # if i == limit:
        #     fp = open("error.txt", "r")
        #     t = fp.read()
        #     t = t + "\n" + wav_file
        #     fp.close()
        #     fp = open("error.txt", "w")
        #     fp.write(t)
        #     fp.close()
        if i < limit: continue
        
        text = path_to_transcript[wav_file]
        if text[len(text) -1] == ":" or text[len(text) - 1] == ",":
            text = text[:len(text) - 1] + "."
        elif text[len(text) -1] != ".":
            text = path_to_transcript[wav_file] + "."
        get_audio(driver, wav_file, text)

    time.sleep(1)


if __name__ == '__main__':
    _main()
    # mp3_to_wav("1.wav")