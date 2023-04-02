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

keyword = ['쉐어하우스', '집콕', '홈술', '편의점', '식단', '재활용', '배민','혼밥', '방음', '밥해결', '집들이', '정수기', '행거', '빨래']
key=['인테리어소품', '셀프인테리어', '셀프리모델링', '가구배치', '구축리모델링', '알파룸', '아파트게스트룸', '쉐어하우스', '테라스', '베란다확장', '이케아가구', '신혼가전', '원룸가구', '빌트인']
key_keywords = []
for i in key:
    for j in keyword:
        key_keywords.append(i + '+' + j)
final_keywords = key + keyword + key_keywords

#크롤링 함수
def next_page():
    current = driver.current_url
    sleep(0.5)
    res = driver.page_source #html 코드 가져오기
    soup = BeautifulSoup(res, "html.parser")
    data_url = soup.select('#container > div.wrap.articles > article > a') #페이지에 있는 글의 url 가져오기
    data_url_list = []
    if len(data_url) == 0:
        return False
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
            a = []
            if len(name) == 0: #소제목이 없을 때
                a.append(" ")
                a.append(text)
                b = ",".join(a)
                comment_num_list.append(comment_num)
                #name_list.append(" ")
                #text_list.append(text)
                comment_time_list.append(comment_time)
                comment_list.append(b)

            else:
                a.append(name[0].text)
                a.append(text)
                b = ",".join(a)
                comment_num_list.append(comment_num)
                #name_list.append(name[0].text)
                #text_list.append(text)
                comment_time_list.append(comment_time)
                comment_list.append(b)

        elif comment_num == 1: #댓글의 갯수가 1일 때
            try:
                comment = driver.find_element(By.CSS_SELECTOR, '#container > div.wrap.articles > article > div > article > p').text #댓글 크롤링
                a = []
                if len(name) == 0: #소제목이 없을 때
                    a.append(" ")
                    a.append(text)
                    a.append(comment)
                    b = ",".join(a)
                    comment_num_list.append(comment_num)
                    #name_list.append(" ")
                    #text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(b)

                else:
                    a.append(name[0].text)
                    a.append(text)
                    a.append(comment)
                    b = ",".join(a)
                    comment_num_list.append(comment_num)
                    #name_list.append(name[0].text)
                    #text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(b)

            except:
                pass
        elif comment_num > 1: #댓글의 갯수가 1이상 일 때
            try:
                comments = driver.find_elements(By.CSS_SELECTOR, '#container > div.wrap.articles > article > div > article > p') #댓글들을 list형태로 크롤링
                a = []
                if len(name) == 0: #소제목이 없을 때
                    a.append(" ")
                    a.append(text)

                    for j in range(len(comments)):  # 댓글을 차례대로 append
                        a.append(comments[j].text)
                    b = ",".join(a)
                    comment_num_list.append(comment_num)
                    #name_list.append(" ")
                    #text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(b)

                else:
                    a.append(name[0].text)
                    a.append(text)
                    for j in range(len(comments)): #댓글을 차례대로 append
                        a.append(comments[j].text)
                    b = ",".join(a)
                    comment_num_list.append(comment_num)
                    #name_list.append(name[0].text)
                    #text_list.append(text)
                    comment_time_list.append(comment_time)
                    comment_list.append(b)

            except:
                pass
    driver.get(current)
    driver.find_element(By.CSS_SELECTOR, 'a.next').click()

comment_num_list = []
#name_list = []
#text_list = []
comment_time_list = []
comment_list = []
url_list = []

for i in final_keywords:

    #전체검색어에 키워드 입력
    driver.find_element(By.CSS_SELECTOR,"#container > div.rightside > form > input").send_keys(i)
    driver.find_element(By.CSS_SELECTOR,"#container > div.rightside > form > input").send_keys(Keys.ENTER)
    for _ in range(1):
        if next_page() == False:
            pass
        else:
            next_page()
            if len(driver.find_elements(By.CSS_SELECTOR, 'a.next')) == 0:
                break

df = pd.DataFrame({
    'comment_num': comment_num_list,
    #'title': name_list,
    #'body': text_list,
    'url': url_list,
    'comment': comment_list,
    'comment_time': comment_time_list
})
df.to_csv("everytime_crawling.csv", encoding='utf-8-sig')
driver.quit()

df = pd.read_csv('everytime_crawling.csv', encoding='utf-8-sig', index_col=0)
for i in df['comment_time']:
    if len(i) == 11:
        df = df.replace(i,'2023.'+i[0:2]+'.'+i[3:5])
    else:
        df = df.replace(i, '20'+i[0:2]+'.'+i[3:5]+'.'+i[6:8])