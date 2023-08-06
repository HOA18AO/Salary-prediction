
import requests
import re
from bs4 import BeautifulSoup
import csv
import assistant

skills_list = []

def crawlJob(url, write, skills_list):
	soup = BeautifulSoup(requests.get(url).text, 'lxml')

	#salary
	salary_raw = soup.find_all('div', {'class': 'box-info'})[0].find_all('div', {'class': 'box-item'})[0].find('span', {'class': 'box-item--content'}).text.strip()
	
	salary = assistant.convertSalary(salary_raw)
	if salary == []:
		salary = -1
	elif len(salary) == 1:
		salary = int(salary[0])
	else:
		salary = (int(salary[0]) + int(salary[1]))/2 # float number

	if salary == -1:
		print('Salary not found')
	else:
		DESCRIPTION = soup.find('div', {'class': 'job-data'}).find_all('div', {'class': 'content-tab'})
		QUALIFICATIONS = DESCRIPTION[1].find_all('li') + DESCRIPTION[1].find_all('span') + DESCRIPTION[1].find_all('p')
		REQUIREMENTS = []

		#skills_options
		skills = []
		for i in QUALIFICATIONS:
			REQUIREMENTS.append(i.text.replace('/', ' '))
		for i in REQUIREMENTS:
			for j in skills_list:
				if j in i and j not in skills:
					skills.append(j.lower())
		print('skills : ', skills)
		IT_job_check = (skills != [])
		#print(skills)

		if IT_job_check == True: # is an IT job
			skills_options = assistant.skillsOptionalize(skills, skills_list)
			#company
			company = soup.find('div', {'class': 'company-title'}).text.strip()
	
			#title
			title = soup.find('h1', {'class': 'job-title text-highlight bold'}).text.strip()
			print(title)

			#location
			location = soup.find('div', {'class': 'box-address'}).find('div').text.strip().replace('- ', '')
			location = assistant.locationConvert_topcv(location)
			location_options = assistant.locationOptionalize(location)

			#exp
			min_EXP = soup.find_all('div', {'class': 'box-info'})[0].find_all('div', {'class': 'box-item box-item--bottom'})[1].find('span', {'class': 'box-item--content'}).text.strip()
			min_EXP = re.findall(r'\d+', min_EXP)
			if min_EXP == []:
				min_EXP = 0
			else:
				min_EXP = int(min_EXP[0])
			#print(min_EXP)

			#bachelor
			BACHELOR = '0'
			for i in range(len(QUALIFICATIONS)):
				QUALIFICATIONS[i] = QUALIFICATIONS[i].text
				QUALIFICATIONS[i] = QUALIFICATIONS[i].lower()
				if BACHELOR == '0' and ('bachelor' in QUALIFICATIONS[i] or 'diploma' in QUALIFICATIONS[i] or 'degree' in QUALIFICATIONS[i] or 'graduate' in QUALIFICATIONS[i]):
					BACHELOR = '1'
					break
				if BACHELOR == '0' and ('tốt nghiệp' in QUALIFICATIONS[i] or 'đại học' in QUALIFICATIONS[i] or 'cao đẳng' in QUALIFICATIONS[i] or 'cử nhân' in QUALIFICATIONS[i]):
					BACHELOR = '1'
					break
					
			for i in range(len(REQUIREMENTS)):
				REQUIREMENTS[i] = REQUIREMENTS[i].lower()

			#experience level = ['0','1','2']
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

			title = assistant.titleClassify(title)
			title_options = assistant.titleOptionalize(title)
			row = [company, salary] + location_options + title_options + skills_options + [min_EXP, BACHELOR, level, QUALIFICATIONS, url]
			write.writerow(row)
		else:
			print('not an IT job!')
	
def crawlPage(url, write, skills_list):
	soup = BeautifulSoup(requests.get(url).text, 'lxml')
	jobs = soup.find_all('div', {'class': 'box-header'})
	for i in range(len(jobs)):
		job_link = jobs[i].find('div', {'class': 'body'}).find('h3', {'class': 'title'}).find('a').get('href')
		print(i, job_link)
		if 'https://www.topcv.vn/viec-lam/' in job_link:
			crawlJob(job_link, write, skills_list)
		else:
			print('FPT special case')
		print('-.-.-.-.-topcv crawling')

def self_main():
	skills_list = assistant.readSkillsLst("skillsFromItviec.txt")
	f = open("dataTopcv.csv", "w", encoding='utf-8', newline='')
	write = csv.writer(f, delimiter=';')
	titleList = ['Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist']
	locationList = ['HN', 'HCM', 'else']
	head_row = ['Company', 'Salary'] + locationList + titleList + skills_list + ['Years of experience', 'Bachelor', 'Experience level', 'QUALIFICATIONS', 'URL']
	write.writerow(head_row)

	url = 'https://www.topcv.vn/viec-lam-it'
	i = 1
	soup = BeautifulSoup(requests.get(url).text, 'lxml')
	# ------
	# pagination style of this website is changed everyday, so there is 2 difficult way to crawl the page number
	# if this one doesn't work, try the other one

	#1
	#page_number = soup.find('ul', {'class': 'pagination'}).find_all('li')[1].find('span').text.strip()
	#page_number = int(re.findall(r'\d+', page_number)[1])	
	
	#2
	page_number = soup.find('ul', {'class': 'pagination'}).find_all('li')
	page_number = int(page_number[-2].text.strip())
	#print(page_number[-2].text)

	while i <= page_number:
		print('{page :', i, '}')
		crawlPage(url + '?page=' + str(i), write, skills_list)
		i += 1
	print('{total : ', page_number, ' pages}')
	f.close()
self_main()