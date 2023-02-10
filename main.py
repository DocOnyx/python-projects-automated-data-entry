import datetime
from pypdf import PdfReader
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

GOOGLE_FORM_URL = "https://forms.gle/qdMniUw7YmMKeM1M7"

texts = [PdfReader("assets/path_report2.pdf").pages[0].extract_text() for i in range(5)]

# reader = PdfReader("assets/path_report2.pdf")
# page2 = reader.pages[0]
# text = page2.extract_text()

names = []
age = []
dob = []
gender = []
px_diagnosis = []
for text in texts:
    try:
        names.append(re.search(r'Patient:\s\w+,\s\w+\s', text).group()[9:])
        age.append(re.search(r'Age:\s\w+\s+\(\w\w/\w\w/\w\w\)', text).group()[5:7])
        dob_ = re.search(r'Age:\s\w+\s+\(\w\w/\w\w/\w\w\)', text).group()[-9:-1]
        dob_ = datetime.datetime.strptime(dob_, '%m/%d/%y').strftime('%d/%m/%Y')
        dob.append(dob_)
        gender.append(re.search(r'Sex:\s\w+\s', text).group()[5:])
        px_diagnosis.append(re.search(r'PAP DIAGNOSIS:\s[\w\s]+', text).group()[16:])
    except Exception as e:
        print(e)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for i in range(len(texts)):
    driver.get(GOOGLE_FORM_URL)
    name = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    name.send_keys(names[i])
    px_age = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    px_age.send_keys(age[i])
    bday = driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
    bday.send_keys(dob[i])
    diag = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    diag.send_keys(px_diagnosis[i])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
print('data entry completed')
