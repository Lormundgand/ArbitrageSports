Pour installer ChromeDriver : 

1:
Connaitre la version de Chrome que l'on utilise (trois points en haut à droite - aide - à propos)

2:
On installe ChromeDriver correspondant à cette version sur ce lien :
https://googlechromelabs.github.io/chrome-for-testing/

3: 
On Décompresse le dossier et on place tout dans C:\WebDriver\ (à créer s'il n'y est pas encore)

4:
Dans les init_driver, on ajoute : 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service("C:/WebDriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
