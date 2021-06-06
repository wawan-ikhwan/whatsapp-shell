import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import subprocess


def readCmd():
    cmds=[]
    filtered=browser.find_elements(By.XPATH, ' //span[contains(text(), "//")]')
    for arr in filtered:
        cmds.append(arr.text)
    if len(cmds)>0:
        cmd=cmds[len(cmds)-1]
        return cmd
    return None

dipanggil=False
def clickCaller():
    global dipanggil
    while True:
        try:
            WebDriverWait(browser,1).until(ec.presence_of_element_located((By.XPATH, ' //span[contains(@title, "/wawan")]'))).click()
            sendPesan('*Bot Wawan dipanggil!*')
            print('called')
            dipanggil=True
            break
        except TimeoutException:
            print('no call')
        sleep(5)

def keluarListener():
    global dipanggil
    cmds=[]
    filtered=browser.find_elements(By.XPATH, ' //span[contains(text(), "/")]')
    for arr in filtered:
        cmds.append(arr.text)
    cmd=cmds[len(cmds)-1]
    if cmd=='/keluar':
        sendPesan("*Bot Wawan telah keluar!*")
        dipanggil=False

def sendPesan(pesan):
    kolomSend=browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]")
    kolomSend.send_keys('*SISTEM*:'+Keys.SHIFT+'\n')
    pesan='```'+pesan
    pesan=pesan.replace('\n','```\n```')
    pesan=pesan+'```'
    kolomSend.send_keys(str(pesan))
    kolomSend.send_keys(Keys.ENTER)

browser=webdriver.Firefox()
browser.get('https://web.whatsapp.com')
print('Sedang scanning barcode...')
WebDriverWait(browser,120).until(ec.title_contains('('))
sleep(4)
print("Masuk!")

while True:
    if dipanggil==False:
        clickCaller()
        satuPutaran=False # FLAG START
        cmdSaatIni=''
        lastCmd=cmdSaatIni
    else:
        cmdSaatIni=readCmd()
        if lastCmd!=cmdSaatIni: # command terbaru (sekali eksekusi)
            perintah=cmdSaatIni[2:]
            print(perintah)
            try:
                if perintah[:3]=='cd ':
                    try:
                        os.chdir(perintah[3:])
                        keluaran='Direketori berubah!'
                    except FileNotFoundError:
                        keluaran='Direketori tidak ditemukan!'
                else:
                    keluaran=subprocess.check_output(perintah,shell=True,universal_newlines=True)
            except subprocess.CalledProcessError:
                keluaran="*!!!*"
            sendPesan(keluaran)
        lastCmd=cmdSaatIni
        keluarListener()
    sleep(2)