import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option("excludeSwitches", ["enable-popup-blocking"])
options.add_argument('--disable-popup-blocking')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Crawl all job of FPT on Topcv.vn

def crawlJob(soup):
    title = soup.find('div', {'class': 'box-white box-detail-job'})
    print(title)

driver.get('https://www.topcv.vn/cong-ty/fpt-software/3.html')
soup = BeautifulSoup(driver.page_source, 'lxml')
next_page_button = soup.find('a', {'class': 'btn btn-paginate btn-next'})
#driver.find_element(By.CLASS_NAME, 'btn btn-paginate btn-next').click()

element = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-paginate.btn-next')
for i in range(17):
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # detect popup ad:
    popup = soup.find('body', {'class': 'modal-open'}, {'style': 'padding-right: 17px'})
    if popup != None:
        print('popup found')
        #close_button = soup.find('div', {'class': 'modal-dialog modal-lg'}).find('button', {'class': 'close'}, {'type': 'button'})
        close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
        close_button.click()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
    
    pagination = soup.find('div', {'class': 'text-center'}).find('span', {'class': 'hight-light'}).text.strip()
    print(i, '--\n', pagination, '\n', crawlJob(soup))

    element.click()
    time.sleep(2)
    
    
driver.quit()

#class="modal-open"
# body
# style = 'padding-right: 17px;'

'''
<div class="modal-dialog modal-lg" role="document">
<div class="modal-content">
<div class="modal-header">
<h5 class="modal-title" id="exampleModalLabel">
TopCV - Tiếp lợi thế, nối thành công
</h5>
<button type="button" class="close" data-dismiss="modal" aria-label="Close">
<span aria-hidden="true">
<i class="fa-solid fa-xmark"></i>
</span>
</button>
</div>
<div class="modal-body">
<iframe id="video-brand-communication" src="https://www.youtube.com/embed/5y9EYHhAwPs?autoplay=1&amp;mute=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen=""></iframe>
</div>
<div class="modal-footer">
<div class="icon">
<img src="https://www.topcv.vn/v4/image/welcome/section-header/toppy-hr-tech.png?v=1.0.0" alt="">
</div>
<div class="comunication-content">
<div class="comunication-content__text">
<p>
Trong sự nghiệp, chọn đúng việc, đi đúng hướng là một <span class="hight-light">lợi thế</span>
</p>
<p>
Định vị bản thân chính xác là một <span class="hight-light">lợi thế</span>
</p>
<p>
Kết nối bền chặt cùng đồng nghiệp cũng là một <span class="hight-light">lợi thế</span>
</p>
<p>
TopCV hiểu rõ, <span class="hight-light">lợi thế</span> nằm trong tay bạn!
</p>
</div>
<p class="hight-light comunication-content__footer">
Với Hệ sinh thái HR Tech, TopCV luôn đồng hành để bạn thành công trong sự nghiệp
</p>
</div>
</div>
<div class="find-out">
<div class="form-check checkbox-dont-show">
<label class="checkbox-dont-show__input">
Không hiển thị lại
<input type="checkbox" id="dont-show_popup_brand_community">
<span class="checkmark"></span>
</label>
</div>
<a href="https://blog.topcv.vn/topcv-tiep-loi-the-noi-thanh-cong/" target="__blank" class="btn btn-find-out">
Tìm hiểu thêm
</a>
</div>
</div>
</div>
'''