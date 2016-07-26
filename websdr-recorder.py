#!/usr/bin/env python

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import gmtime, strftime
import os, glob

websdr_url = "http://websdr.ewi.utwente.nl:8901/"
websdr_freq = "8992.0"
record_duration = 70 * 60 # in seconds
record_filedir = os.path.dirname(os.path.abspath(__file__)) + "/recordings"
record_filename = "websdr_recording_" + strftime("%Y%m%d-%H%M", gmtime()) + "Z_" + websdr_freq + "kHz"
firefox_tmpdir = "/tmp/mozilla_x-f0/"

# ---------------------------------------------------------

def log(msg):
  
  logmsg = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  logmsg = "[" + logmsg + "] " + str(msg)
  # cmd = "echo \"" + logmsg + "\" >> " + file
  print logmsg
  # os.system(cmd)


display = Display(visible=0, size=(800, 600))
display.start()

# FirefoxProfile does not seem to be working
# fp = webdriver.FirefoxProfile()
# fp.set_preference("browser.download.folderList", 2)
# fp.set_preference("browser.download.dir", os.getcwd())
# fp.set_preference("browser.download.downloadDir", os.getcwd())
# fp.set_preference("browser.download.useDownloadDir", False)
# fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
# fp.set_preference("browser.download.manager.focusWhenStarting", False)
# fp.set_preference("browser.download.manager.showWhenStarting", False)
# fp.set_preference("browser.download.manager.closeWhenDone", True)
# fp.set_preference("browser.download.manager.showAlertOnComplete", False)
# fp.set_preference("browser.download.manager.useWindow", False)
# fp.set_preference("browser.download.manager.showAlertOnComplete", False)
# fp.set_preference("pdfjs.disabled", True)
# fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
# fp.set_preference("browser.helperApps.alwaysAsk.force", False)
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream, audio/x-wav, audio/wav")

log("starting browser..")

# now Firefox will run in a virtual display. 
# you will not see the browser.
# browser = webdriver.PhantomJS()
browser = webdriver.Firefox()
#browser = webdriver.Firefox(firefox_profile=fp)
log("started")

browser.get(websdr_url)
log("page: " + browser.title)
# time.sleep(3)

# waterfall off
browser.find_element_by_css_selector("span#viewformbuttons input:last-child").click()

freq = browser.find_element_by_name("frequency")
freq.clear()
freq.send_keys(websdr_freq)
freq.send_keys(Keys.ENTER)

# browser.save_screenshot("./wsdr-1.jpg")

recbtn = browser.find_element_by_id("recbutton")
log("start recording..")
recbtn.click()

time.sleep(record_duration)
# browser.save_screenshot("./wsdr-2.jpg")

# stop
recbtn.click()
log("stop recording")

recfile = browser.find_element_by_css_selector("#reccontrol a")
#filename = recfile.get_attribute("download")

log("downloading..")
recfile.click()
# not known when download finishes, just sleep and hope
time.sleep(5)
log("done")
# browser.save_screenshot("./wsdr-4.jpg")


browser.quit()
display.stop()
log("browser closed")

# /tmp/mozilla_x-f0/YEf2Nonx.wav.part
lasttmpfile = max(glob.iglob(firefox_tmpdir + '/*.part'), key=os.path.getctime)
log(lasttmpfile + " (" + str(os.path.getsize(lasttmpfile)/1024) + "K)")
cmd = "cp " + lasttmpfile + " " + record_filedir + "/" + record_filename + ".wav"
os.system(cmd)
# log(filename)
# print cmd

log("converting audio file..")
# -loglevel error -hide_banner
cmd = "ffmpeg -loglevel error -hide_banner -i " + record_filedir + "/" + record_filename + ".wav -vn -ar 16000 -ac 1 -codec:a libmp3lame -qscale:a 9 -f mp3 " + record_filedir + "/" + record_filename + ".mp3"
os.system(cmd)
# print cmd
log(record_filename + ".mp3 (" + str(os.path.getsize(record_filedir + "/" + record_filename + ".mp3")/1024) + "K)")

log("done")