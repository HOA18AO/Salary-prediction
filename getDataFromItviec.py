import assistant
#assistant.installLibraries()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import csv
import re
#import functools

skills_list = []
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login(url, username, password):
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[2]/li[2]/a').click()
    driver.find_element(By.XPATH, '//*[@id="user_email"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div/div[2]/form/div[4]/div/button').click()
    url = driver.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[1]/a').get_attribute('href')
    driver.get(url)

# CRAWL INDIVIDUAL JOBS
def crawlJob(url, skills_list, write):
    IT_job_check = True
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # SALARY------------------------------
    salary_raw = soup.find('div', {'class': 'job-details__overview'}).find_all('div', {'class': 'svg-icon__text'})[0].text.strip()
    salary = assistant.convertSalary(salary_raw) # 'print' raw salary in the function
    #print(salary)
    if salary == []:
        salary = -1
    elif len(salary) == 1:
        salary = int(salary[0])
    else:
        salary = (int(salary[0]) + int(salary[1]))/2
    #print(salary)

    if salary == -1:
        print('Salary not found')
    else:
        DESCRIPTION = soup.find('div', {'class':'jd-page__job-details'}).find_all('div', {'class':'job-details__paragraph'})
        QUALIFICATIONS = DESCRIPTION[1].find_all('span') + DESCRIPTION[1].find_all('p') + DESCRIPTION[1].find_all('li')
        # ---------------------------------------
        # NGOÀI CÁC KỸ NĂNG THÌ CÒN CÓ THỂ ĐÁNH GIÁ DỰA THEO CÁC YẾU TỐ NÀO NỮA? (CHƯA NGHĨ RA)
        # SKILLS-----------------

        #just get skills from the JD
        skills = []

        #crawl skills from QUALIFICATIONS
        REQUIREMENTS = []
        for i in QUALIFICATIONS:
            REQUIREMENTS.append(i.text)
        for i in REQUIREMENTS:
            for j in skills_list:
                if j in i and j not in skills:
                    skills.append(j.lower())
        #print(skills)
        skills_options = assistant.skillsOptionalize(skills, skills_list)

        # is this an IT job?
        IT_job_check = assistant.isITJob(skills_options)

        if IT_job_check == True:

            title = soup.find('div', {'class': 'job-details__header'}).find('h1').text.strip()
            company = soup.find('div', {'class': 'job-details__header'}).find('div', {'class': 'job-details__sub-title'}).text.strip()
            print(company, title)
            location = soup.find('div', {'class': 'job-details__overview'}).find_all('div', {'class': 'svg-icon__text'})[1].find('span').text.strip()
            # convert this location into city or province
            location = assistant.locationConvert_itviec(location)
            location_options = assistant.locationOptionalize(location)

            # JOB DESCRIPTION
        
            YO_EXP_container = []
            BACHELOR = '0'

            for i in range(len(QUALIFICATIONS)):
                QUALIFICATIONS[i] = QUALIFICATIONS[i].text
                QUALIFICATIONS[i] = QUALIFICATIONS[i].lower()
                if ('experience' in QUALIFICATIONS[i] and 'year' in QUALIFICATIONS[i]) or ('năm' in QUALIFICATIONS[i] and 'kinh nghiệm' in QUALIFICATIONS[i]):
                    YO_EXP_container.append(assistant.convertToNumber(QUALIFICATIONS[i]).replace('.0', '').replace(', ', ''))
                if BACHELOR == '0' and ('bachelor' in QUALIFICATIONS[i] or 'diploma' in QUALIFICATIONS[i] or 'degree' in QUALIFICATIONS[i] or 'graduate' in QUALIFICATIONS[i]):
                    BACHELOR = '1'
            YO_EXP = []
            for i in YO_EXP_container:
                YO_EXP.append(re.findall(r'\d+',i))

            min_EXP = '99' # a random large number

            if YO_EXP != []:
                for i in range(len(YO_EXP)):
                    YO_EXP[i] = assistant.min(YO_EXP[i])
                min_EXP = assistant.max(YO_EXP)
            #print(YO_EXP)
            if min_EXP == '99':
                min_EXP = '0'
            #print(min_EXP)
            #print('min experience: ', min_EXP)

            for i in range(len(REQUIREMENTS)):
                REQUIREMENTS[i] = REQUIREMENTS[i].lower()
            #experience level = ['Fresher': 0, 'Junior': 1, 'Senior': 2]
            level = '0'
            if 'senior' in title.lower() or 'senior' in REQUIREMENTS:
                level = '2'
            elif 'junior' in title.lower() or 'junior' in REQUIREMENTS:
                level = '1'
            elif 'fresher' in title.lower() or 'fresher' in REQUIREMENTS:
                level = '0'

            if level == '0':
                if int(min_EXP) >= 5:
                    level = '2' # Sr.
                elif int(min_EXP) >= 3:
                    level = '1'
                else:
                    level = '0'
            # ------------------------
            title = assistant.titleClassify(title)
            title_options = assistant.titleOptionalize(title)

            row = [company, salary] + location_options + title_options + skills_options + [min_EXP, BACHELOR, level, QUALIFICATIONS, url]
            write.writerow(row)

        else:
            print('Not an IT job!')
    
# CRAWL JOBS IN EACH PAGES
def crawlPage(url, soup, skills_list, write):
    jobs = soup.find_all('h3', {'class': 'title job-details-link-wrapper'})
    i = 0
    for job in jobs:
        i += 1
        job_url = job.find('a').get('href')
        print(i, job_url)
        crawlJob('https://itviec.com' + job_url, skills_list, write)
        print('--.--.--.--.itviec crawling')
    

# EVERYTHING SHOULD BE HAPPENDED IN HERE
def self_main():
    f = open("dataItviec.csv", "w", encoding='utf-8', newline="")
    write = csv.writer(f, delimiter=';')
    skills_list = assistant.readSkillsLst("skillsFromItviec.txt")
    titleList = ['Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist']
    locationList = ['HN', 'HCM', 'else']
    head_row = ['Company', 'Salary'] + locationList + titleList + skills_list + ['Years of experience', 'Bachelor', 'Experience level', 'QUALIFICATIONS', 'URL']
    write.writerow(head_row)
    
    login('https://itviec.com/viec-lam-it', 'edepchai@gmail.com', 'Dxdi@g01669')
    
    i = 1
    while True:
        url = 'https://itviec.com/viec-lam-it?page=' + str(i)
        print('{Page', i, '}')
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        jobs = soup.find_all('h3', {'class': 'title job-details-link-wrapper'})
        i += 1
        if len(jobs) == 0:
            break
        else:
            crawlPage(url, soup, skills_list, write)
        #if i == 2:
        #    break
        
    f.close()
    print('total:', i-1, 'page(s)')

self_main()
