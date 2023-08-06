from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import unidecode
import glob
import os
import requests
import re
import csv
import pandas

def  installPackage(package):
	return_value = os.system('pip show ' + package)
	if return_value != 0:
		os.system('pip install ' + package)
	else:
		print(package + ' is already existed')

def installLibraries():
	installPackage('Selenium')
	installPackage('requests')
	installPackage('bs4')

def readSkillsLst(path):
	fi = open(path, "r", encoding='utf-8')
	read = fi.readlines()
	skills_list = []
	for i in read:
		skills_list.append(i.replace('\n', ''))
	fi.close()
	return skills_list

def skillsFunction(skills_raw):
	skills = []
	for i in skills_raw:
		skills.append(i.text.lower().strip())
	return skills

def skillsOptionalize(skills, skills_list):
	skills_options = [0 for i in range(len(skills_list))]
	for i in range(len(skills_list)):
		if skills_list[i].lower() in skills:
			#print(skills_list[i])
			skills_options[i] = 1 #integer
	return skills_options

def usdToVnd(num):
	return num*23.4/1000

def convertSalary(s):
	s = s.lower()
	print(s)
	if '$' in s or 'usd' in s: # Dollars
		salary = s.replace(',','').replace('$','').replace('.','').split(' ')
		i = 0
		while i < len(salary):
			if salary[i].isnumeric() == False:
				del salary[i]
				i -= 1
			i += 1
		if len(salary) > 0:
			for i in range(len(salary)):
				salary[i] = usdToVnd(int(salary[i]))
	else:
		salary = s.replace(',','').replace('.','').replace('tr','').replace('m','').replace('t','').split(' ')
		i = 0
		while i < len(salary):
			if salary[i].isnumeric() == False:
				del salary[i]
				i -= 1
			i += 1
		if len(salary) > 0:
			for i in range(len(salary)):
				if int(salary[i]) > 200: # dollars
					salary[i] = usdToVnd(int(salary[i]))
				else:
					salary[i] = int(salary[i])
	return salary

def convertToNumber(s):
	s = s.lower()
	s = s.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5')
	s = s.replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace('ten', '10')
	return s

def delLeadingZeroes(s):
	if s == '0':
		return s
	if len(s) > 0:
		while s[0] == '0':
			s = s[1:]
			if len(s) <= 1:
				break
	return s

def minOfStringLst(box):
	m = box[0]
	for i in range(1, len(box)):
		if int(box[i]) < int(m):
			m = box[i]
	return m

def isITJob(skills_options):
	if skills_options == [0 for i in range(len(skills_options))]:
		return False
	else:
		return True

def min(box):
	min_val = '99'
	for i in range(len(box)):
		if int(box[i]) < int(min_val):
			min_val = box[i]
	if min_val != '99':
		return min_val
	else:
		return '0'

def max(box):
	max_val = '0'
	for i in range(len(box)):
		if int(box[i]) > int(max_val):
			max_val = box[i]
	return max_val

def titleClassify(s):
	s = unidecode.unidecode(s)
	if 'engineer' in s.lower() or 'ky su' in s.lower() or 'fullstack' in s.lower() or 'full-stack' in s.lower() or 'compliance' in s.lower() or 'auditor' in s.lower() or 'software' in s.lower() or 'phan mem' in s.lower() or 'trien khai' in s.lower() or 'se' in s.lower():
		return 'Engineer'
	elif 'dev' in s.lower() or 'app' in s.lower() or 'thuc tap' in s.lower() or 'embedded' in s.lower() or 'lap trinh' in s.lower() or 'phat trien' in s.lower() or 'research' in s.lower() or 'game' in s.lower() or 'coder' in s.lower() or 'phat trien' in s.lower() or 'system' in s.lower():
		return 'Developer'
	elif 'admin' in s.lower() or 'van hanh' in s.lower() or 'giam sat' in s.lower() or 'master' in s.lower() or 'quan tri' in s.lower() or 'coach' in s.lower() or 'erp' in s.lower() or ('end' in s.lower() and ('back' in s.lower() or 'front' in s.lower())) or 'dba' in s.lower():
		return 'Administrator'
	elif 'manage' in s.lower() or 'leader' in s.lower() or 'lead' in s.lower() or 'quan ly' in s.lower() or 'chief' in s.lower() or 'phong' in s.lower() or 'owner' in s.lower() or 'director' in s.lower() or 'operation' in s.lower() or 'giam doc' in s.lower():
		return 'Manager'
	elif 'test' in s.lower() or 'tester' in s.lower() or 'kiem thu' in s.lower():
		return 'Tester'
	elif 'design' in s.lower() or 'architect' in s.lower() or 'thiet ke' in s.lower():
		return 'Designer'
	elif 'support' in s.lower() or 'helpdesk' in s.lower() or 'ho tro' in s.lower() or 'ky thuat' in s.lower():
		return 'Support'
	elif 'analyst' in s.lower() or 'phan tich' in s.lower() or 'data' in s.lower():
		return 'Analyst'
	elif 'science' in s.lower() or 'scientist' in s.lower():
		return 'Scientist'
	elif 'middle' in s.lower():
		return 'Engineer'
	else:
		return s

def titleOptionalize(s):
	result = ['Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist']
	for i in range(len(result)):
		if result[i] != s:
			result[i] = 0
		else:
			result[i] = 1
	return result

#print(titleOptionalize('Dev'))

def locationConvert_itviec(s):
	s = unidecode.unidecode(s)
	s = s.split(',')
	s = s[-1].replace('tp.', '').strip().lower()
	return s

def locationConvert_topcv(s):
	s = s.split(':')
	s = unidecode.unidecode(s[0].lower()).strip()
	return s

def locationConvert_jobsgo(s):
	s = unidecode.unidecode(s)
	s = s.lower()
	s = s.split('viec lam tai')
	s = s[-1].strip()
	return s

def locationOptionalize(s): #[Ha Noi, Ho Chi Minh, else]
	if s == 'ha noi':
		return [1, 0, 0]
	elif s == 'ho chi minh':
		return [0, 1, 0]
	else:
		return [0, 0, 1]

def mergeDataFrame():
	datasetPath = 'E:/DataPre-handle/dataset'
	dataset = []
	csvFiles = glob.glob(datasetPath + '/*.csv')
	for f in csvFiles:
		df = pandas.read_csv(f, delimiter=';')
		dataset.append(df)
		
	finalDf = pandas.concat(dataset, ignore_index=True)
	finalDf = finalDf.drop_duplicates(keep='first', ignore_index=True)
	return finalDf
