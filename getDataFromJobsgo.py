import assistant
from bs4 import BeautifulSoup
import requests
import re
import csv


skills_list = assistant.readSkillsLst("skillsFromItviec.txt")

#crawl a job
def crawlJob(url, skills_list, write):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')

    salary_raw = soup.find('span', {'class': 'saraly text-bold text-green'}).text.strip()
    salary = re.findall(r'\d+', salary_raw)
    if salary == []:
        salary = -1
    elif len(salary) == 1:
        salary = int(salary[0])
    else:
        salary = (int(salary[0]) + int(salary[1]))/2 # float

    if salary == -1:
        print('Salary not found')
    else:
        DESCRIPTION = soup.find_all('div', {'class': 'content-group'})
        QUALIFICATIONS = DESCRIPTION[3].find_all('li') + DESCRIPTION[3].find_all('p') + DESCRIPTION[3].find_all('span')
        if QUALIFICATIONS == []:
            #print('this is\n')
            QUALIFICATIONS = DESCRIPTION[3].find_all('div', {'class': "clearfix"})
        #QUALIFICATIONS = DESCRIPTION[3]
        skills = soup.find('div', {'class': "list"}).text.strip().split(' ,  ')
        print(skills)
        #skills in qualification
        REQUIREMENTS = []
        for i in QUALIFICATIONS:
            REQUIREMENTS.append(i.text)
        #print(REQUIREMENTS)
        for i in REQUIREMENTS:
            for j in skills_list:
                if j in i and j not in skills:
                    skills.append(j.lower())
        #print(skills)
        skills_options = [0 for i in range(len(skills_list))] # >50
        for i in range(len(skills_list)):
            if skills_list[i] in skills:
                skills_options[i] = 1

        IT_job_check = assistant.isITJob(skills_options)
        if IT_job_check == True:
            company = soup.find('div', {'class': 'profile-cover'}).find('h2').text.strip()
            title = soup.find('h1', {'class': 'media-heading text-semibold'}).text.strip()

            location = soup.find('div', {'class': 'data giaphv'}).text.strip()
            location = assistant.locationConvert_jobsgo(location)
            location_options = assistant.locationOptionalize(location)

            YO_EXP_container = []
            BACHELOR = '0'
            for i in range(len(QUALIFICATIONS)):
                QUALIFICATIONS[i] = QUALIFICATIONS[i].text.lower()
                if ('experience' in QUALIFICATIONS[i] and 'year' in QUALIFICATIONS[i]) or ('năm' in QUALIFICATIONS[i] and 'kinh nghiệm' in QUALIFICATIONS[i]):
                    YO_EXP_container.append(assistant.convertToNumber(QUALIFICATIONS[i]).replace('.0', '').replace(', ', ''))
                if BACHELOR == '0' and ('bachelor' in QUALIFICATIONS[i] or 'diploma' in QUALIFICATIONS[i] or 'degree' in QUALIFICATIONS[i] or 'graduate' in QUALIFICATIONS[i]):
                    BACHELOR = '1'
            YO_EXP = []
            for i in YO_EXP_container:
                if ('năm' in i and 'kinh nghiệm' in i):
                    print(i)
                YO_EXP.append(re.findall(r'\d+',i))
            min_EXP = '99' # random bullshit
            if YO_EXP != []:
                for i in range(len(YO_EXP)):
                    YO_EXP[i] = assistant.min(YO_EXP[i])
                min_EXP = assistant.max(YO_EXP)
            #print(YO_EXP)
            if min_EXP == '99':
                min_EXP = '0'

            for i in range(len(REQUIREMENTS)):
                REQUIREMENTS[i] = REQUIREMENTS[i].lower()

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
    
            if skills_options != [0 for i in range(len(skills_options))]:
                #print(company, '\n', title, '\n', salary, '\n', min_EXP, '\n----')
                print(url, '\n', title, '\n', skills, '\n-----')
                title = assistant.titleClassify(title)
                title_options = assistant.titleOptionalize(title)
                row = [company, salary] + location_options + title_options + skills_options + [min_EXP, BACHELOR, level, QUALIFICATIONS, url]
                write.writerow(row)
        else:
            print('Not an IT job')

#crawl a 50-jobs page
def crawlPage(url, write):
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    jobs = soup.find_all('div', {'class': 'brows-job-position'})
    for job in jobs:
        job_url = job.find('div', {'class': 'h3'}).find('a').get('href')
        print(job_url)
        crawlJob(job_url, skills_list, write)
        print('--.--.--.--.jobsgo crawling')

def self_main():
    f = open("dataJobsgo.csv", 'w', encoding='utf-8', newline='')
    write = csv.writer(f, delimiter=';')
    titleList = ['Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist']
    locationList = ['HN', 'HCM', 'else']
    head_row = ['Company', 'Salary'] + locationList + titleList + skills_list + ['Years of experience', 'Bachelor', 'Experience level', 'QUALIFICATIONS', 'URL']
    write.writerow(head_row)

    i = 1
    while True:
        url ='https://jobsgo.vn/viec-lam-cong-nghe-thong-tin-trang-'+str(i)+'.html?view=ajax&view=ajax'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        key = soup.find('span', {'class': 'pull-right'}).text.strip()
        key_nums = re.findall(r'\d+', key)
        if int(key_nums[0]) > int(key_nums[1]):
            print('there are ', i-1, ' pages')
            break
        crawlPage(url, write)
        i += 1
        #if i == 2:
        #    break

    f.close()

self_main()
