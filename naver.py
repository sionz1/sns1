from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import numpy  
import pandas as pd  
import random
import os
import re

print("=" *80)
print(" 연습문제8-1 :네이버 영화 리뷰 정보 수집하기")
print("=" *80)
print("\n")


query_txt = input("1.크롤링 할 영화의 제목을 입력하세요: ")
cnt = int(input(' 2.크롤링 할 리뷰건수는 몇건입니까?: '))
page_cnt = math.ceil(cnt / 10)

f_dir = input("3.파일을 저장할 폴더명만 쓰세요(예:c:\temp\):")

now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)
ff_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'
fc_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'
fx_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'






s_time = time.time( )
path = "c:/temp/chromedriver_240/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://movie.naver.com/")
time.sleep(2)



html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
element = driver.find_element_by_id("ipt_tx_srch")
element.send_keys(query_txt)
time.sleep(2)
driver.find_element_by_xpath("""//*[@id="jSearchArea"]/div/button""").click()
time.sleep(2)
driver.find_element_by_xpath("""//*[@id="old_content"]/ul[2]/li[1]/dl/dt/a""").click()
time.sleep(2)
driver.find_element_by_link_text("별점(평점)").click()
time.sleep(2)
cnt2=0


time.sleep(2)
driver.switch_to.frame('pointAfterListIframe') 
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser') 
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
search_cnt_1 = soup.find('strong','total').get_text()
search_cnt_2 = search_cnt_1.split("|")[1].replace("총","").replace("건","").replace(",","")

    

if cnt > int(search_cnt_2) :
    
    cnt2 = int(search_cnt_2)

else :

    cnt2 = cnt
    
no = 0
no2 =[ ]          
star2=[ ]     
opinion2=[ ]         
name2=[]             
date2=[]         
good2=[]       
bad2=[]    



while(True) :    

    print("총 %s 건중 % 번째  리뷰 데이터를 수집 시작합니다 =======================" %(x,count))
    print("\n")
    count=0   
    for i in content_list:   

        no=no+1
        count += 1
        print("%s 번째 댓글 수집 중 ==================" %count)
        no2.append(no)
        print('번호:',no)

    

        star = i.find('div',class_='star_score').get_text( )
        print('별점:',star.strip())
        star2.append(star)
        opinion = i.find('div',class_='score_reple').find('p').get_text( )
        print('리뷰내용:',opinion.strip())
        opinion2.append(opinion)
        name = i.find('div',class_='score_reple').find('span').get_text( )
        print('작성자:',name.strip())
        name2.append(name)
        date = i.find('div',class_='score_reple').find_all("em")[1].get_text( )
        print('작성일자:',date.strip())
        date2.append(date)
        good = i.find('div',class_='btn_area').find_all("strong")[0].get_text()
        print('공감:',good.strip())
        good2.append(good)
        bad = i.find('div',class_='btn_area').find_all("strong")[1].get_text()
        print('비공감:',bad.strip())   
        bad2.append(bad)        
        if cnt2 == no:
            break
    if cnt2 == no:
        break
    else:

        driver.find_element_by_class_name('pg_next').click()
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content_list = soup.find('div','score_result').find_all('li')
movie_reple = pd.DataFrame()
movie_reple['별점(평점)']=pd.Series(star2)
movie_reple['리뷰내용']=pd.Series(opinion2)
movie_reple['작성자']=pd.Series(name2)
movie_reple['작성일자']=pd.Series(date2)
movie_reple['공감횟수']=pd.Series(good2)
movie_reple['비공감횟수']=pd.Series(bad2)
movie_reple.to_csv(fc_name,encoding="utf-8-sig",index=True)
movie_reple.to_excel(fx_name ,index=True)
e_time = time.time( )
t_time = e_time - s_time

print("\n") 
print("=" *80)
print("1.요청된 총 %s 건의 리뷰 중에서 실제 크롤링 된 리뷰수는 %s 건입니다" %(cnt,count))
print("2.총 소요시간은 %s 초 입니다 " %round(t_time,1))
print("3.파일 저장 완료: txt 파일명 : %s " %ff_name)
print("4.파일 저장 완료: csv 파일명 : %s " %fc_name)
print("5.파일 저장 완료: xls 파일명 : %s " %fx_name)
print("=" *80)
driver.close( )
