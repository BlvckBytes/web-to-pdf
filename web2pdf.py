# Selenium (used as headless browser)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Pillow (used for PDF generation)
from PIL import Image

# Miscellaneous
from datetime import datetime
from os import path
import argparse

# Logging messages prefixed with timestamp to stdout
def log(message: str):
  pref = datetime.now().strftime('%H:%M:%S')
  print(f'[{pref}]: {message}')

# Parse required and optional arguments
parser = argparse.ArgumentParser()
parser.add_argument(
  '-u', dest='url', help='Full URL of target website',
  required=True
)
parser.add_argument(
  '-o', dest='output', help='Output directory path, defaults to Desktop',
  default=path.join(path.expanduser('~'), 'Desktop')
)
parser.add_argument(
  '-n', dest='fileName', help='Name of PDF file (excluding .pdf), defaults to "result"',
  default='result'
)
parser.add_argument(
  '-p', dest='pageClass', help='Class of page wrapping container (no leading .)',
  required=True
)
parser.add_argument(
  '-w', dest='waitClass', help='Class of item to wait for until rendered (no leading .)'
)
args = parser.parse_args()

# Save screenshots of all elements having the provided class
# An array of paths is returned, representing individual images
def save_screenshots(driver: webdriver.Chrome, elClass: str, basePath: str):
  baseScript = f'return document.getElementsByClassName("{elClass}")'
  numElems = driver.execute_script(f'{baseScript}.length')
  paths = []

  # Loop all elements having this class name on entire page
  for i in range(0, numElems):
    # Calculate height and width of element to avoid clipping
    targetScript = f'{baseScript}[{i}].getBoundingClientRect()'
    required_width = driver.execute_script(f'{targetScript}.width')
    required_height = driver.execute_script(f'{targetScript}.height')

    # Set window height and find current target element
    driver.set_window_size(required_width, required_height)
    el = driver.find_elements(By.CLASS_NAME, elClass)[i]

    # Screenshot element and append output path to list
    currPath = f'{basePath}/{elClass}-{i}.png'
    el.screenshot(currPath)
    log(f'Took screenshot and saved it to {currPath}')
    paths.append(currPath)

  return paths

# Spin up a headless chrome instance
beginStamp = datetime.now()
o = Options()
o.add_argument('--headless')
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=o, service=s)
log('Created chrome driver')

# Navigate to target page
driver.get(args.url)
log('Fetched target site')

# Wait for element with provided class to render
if args.waitClass is not None:
  try:
    con = EC.presence_of_element_located((By.CLASS_NAME, args.waitClass))
    WebDriverWait(driver, 5000).until(con)
    log('Successfully waited until element rendered!')
  except TimeoutException:
    log('Loading elements took too long!')

# Take screenshots to TMP
log('Starting to take screenshots...')
paths = save_screenshots(driver, args.pageClass, '/tmp')
log('Done taking screenshots!')

# Quit
log('Quitting driver...')
driver.close()
log('Quitted driver!')

# Combine into PDF
log('Combining images into final PDF...')
pdfPath = f'{args.output}/{args.fileName}.pdf';
imgs = [Image.open(p).convert('RGB').resize((2480, 3508)) for p in paths]
imgs[0].save(pdfPath, 'PDF', resolution=100.0, save_all=True, append_images=imgs[1:])
log(f'PDF saved at {pdfPath}!')

# Print how long this process took
endStamp = datetime.now()
log(f'Took {(endStamp - beginStamp).total_seconds()}s, goodbye!')