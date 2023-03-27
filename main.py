from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

#driver = webdriver.Chrome(ChromeDriverManager().install()) #mac 전용

driver = webdriver.Chrome('C:/Users/jongi/Downloads/chromedriver_win32/chromedriver') #윈도우 전용
driver.implicitly_wait(1)

#로그인
driver.get('https://everytime.kr/login')
driver.find_element(By.NAME,'userid').send_keys('***') #아이디
driver.find_element(By.NAME,'password').send_keys('***') #비밀번호
driver.find_element(By.XPATH,'//*[@id="container"]/form/div/div/div/iframe').click()
sleep(10)
driver.find_element(By.XPATH,'//*[@id="container"]/form/p[3]/input').click()

#크롤링 함수
def next_page():
    current = driver.current_url
    sleep(0.5)
    res = driver.page_source #html 코드 가져오기
    soup = BeautifulSoup(res, "html.parser")
    data_url = soup.select('#container > div.wrap.articles > article > a') #페이지에 있는 글의 url 가져오기
    data_url_list = []
    for i in range(len(data_url)):
        data_url_list.append('https://everytime.kr' + data_url[i].get('href')) #url을 하이퍼링크로 전환하여 data_url_list에 넣기
        url_list.append('https://everytime.kr' + data_url[i].get('href'))

    for i in data_url_list:
        driver.get(i) #data_url_list안에 있는 하이퍼링크를 차례로 방문
        name = driver.find_elements(By.CSS_SELECTOR, 'h2.large') #제목을 list 형태로 가져옴. 존재한다면 len(name) == 1 존재하지않는다면 len(name) == 0
        text = driver.find_element(By.CSS_SELECTOR, 'p.large').text
        comment_num = int(driver.find_element(By.CSS_SELECTOR, 'li.comment').text) #data_url_list안에 있는 페이지들을 돌면서 각각의 제목, 내용, 댓글 갯수를 가져옴
        comment_time = driver.find_element(By.CSS_SELECTOR, 'time.large').text

        if comment_num == 0: #댓글의 갯수가 0일 때
            if len(name) == 0: #소제목이 없을 때
                comment_num_list.append(comment_num)
                name_list.append(" ")
                text_list.append(text)
                comment_time_list.append(comment_time)
                comment_list.append(" ")

            else:
                comment_num_list.append(comment_num)
                name_list.append(name[0].text)
                text_list.append(text)
                comment_time_list.append(comment_time)
                comment_list.append(" ")

        elif comment_num == 1: #댓글의 갯수가 1일 때
            try:
                comment = driver.find_element(By.CSS_SELECTOR, '#container > div.wrap.articles > article > div > article > p').text #댓글 크롤링
                a = []
                if len(name) == 0: #소제목이 없을 때
                    a.append(comment)
                    comment_num_list.append(comment_num)
                    name_list.append(" ")
                    text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(a)

                else:
                    a.append(comment)
                    comment_num_list.append(comment_num)
                    name_list.append(name[0].text)
                    text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(a)

            except:
                pass
        elif comment_num > 1: #댓글의 갯수가 1이상 일 때
            try:
                comments = driver.find_elements(By.CSS_SELECTOR, '#container > div.wrap.articles > article > div > article > p') #댓글들을 list형태로 크롤링
                if len(name) == 0: #소제목이 없을 때
                    a = []
                    for j in range(len(comments)):  # 댓글을 차례대로 append
                        a.append(comments[j].text)
                    comment_num_list.append(comment_num)
                    name_list.append(" ")
                    text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(a)

                else:
                    a = []
                    for j in range(len(comments)): #댓글을 차례대로 append
                        a.append(comments[j].text)
                    comment_num_list.append(comment_num)
                    name_list.append(name[0].text)
                    text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(a)

            except:
                pass
    driver.get(current)
    driver.find_element(By.CSS_SELECTOR, 'a.next').click()

keywords = ["자취", "취두부"]

for i in keywords:
    comment_num_list = []
    name_list = []
    text_list = []
    comment_time_list = []
    comment_list = []
    url_list = []
    #전체검색어에 키워드 입력
    driver.find_element(By.CSS_SELECTOR,"#container > div.rightside > form > input").send_keys(i)
    driver.find_element(By.CSS_SELECTOR,"#container > div.rightside > form > input").send_keys(Keys.ENTER)
    for _ in range(2):
        next_page()
        if len(driver.find_elements(By.CSS_SELECTOR, 'a.next')) == 0:
            break
    df = pd.DataFrame({
        'comment_num' : comment_num_list,
        'title' : name_list,
        'body' : text_list,
        'url' : url_list,
        'comment' : comment_list,
        'comment_time' : comment_time_list
    })
    df.to_csv("everytime_crawling" + "_"+ i + ".csv", encoding='utf-8-sig')
driver.quit()

