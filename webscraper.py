import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



 
def init_driver():
    binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    #driver.set_window_position(-3000, 0) # driver.set_window_position(0, 0) to get it back
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
def lookupImage(driver, query):
    driver.get("http://images.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnG")))
        box.send_keys(query)
        button.click()

        images =  driver.find_elements_by_tag_name('img')
        for img in images:
            if(img.get_attribute('class') == "rg_ic rg_i"):
                print(img.get_attribute('src'))
                break

    
    except TimeoutException:
        print("Box or Button not found in google.com")

def lookupPage(driver, query, keyword1, keyword2 = ""):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
        RESULTS_LOCATOR = "//div/h3/a"

        WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))

        page1_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)
        for item in page1_results: 
            if keyword1 in item.text:
                item.click()
                return driver.current_url
                break

        page1_results[0].click()
        return(driver.current_url)
    except TimeoutException:
        print("Box or Button not found in google.com")
 
 
if __name__ == "__main__":
    
    driver = init_driver()

    nameFile = open("songs.txt", 'r')
    outputFile = open("htmlData.txt", 'w')
    names = nameFile.read().split('\n')
    print("Processing " + str(len(names)) + " Songs")

    for songName in names:
        print("Processed " + songName + "...",end = "")
        chordSearch = songName.strip() + " chords"
        lyricsSearch = songName.strip() + " lyrics"
        chordsUrl = lookupPage(driver, chordSearch, "Ultimate")
        print("found chords...", end = "");
        lyricsUrl = lookupPage(driver, lyricsSearch, "Genius")
        print("found lyrics...")

        try:
            outputFile.write("<tr>\n <td>" + songName + "</td><td> <a href = " + '"' + chordsUrl + '" target = "_blank">Chords</a>' + 
                " <a href = " + '"' + lyricsUrl + '" target = "_blank">Lyrics</a></td>\n</tr>\n\n')
        except:
            print("ERROR! Skipping...")
            continue

    nameFile.close()
    outputFile.close()
    driver.quit()

   
