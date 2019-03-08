import requests
from bs4 import BeautifulSoup
import os
import time
# import pprint
import pandas as pd
import re
import threading
import random
import xlsxwriter

# Load dictionary
path = './dict'
dictionary_list = os.listdir(path)
word_list = list()
for f in dictionary_list:
    with open(r'%s/%s'%(path, f), 'r') as d:
        word_list += d.read().split('\n')

# Header
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

# Create a directory to saving files
path = r'./job104_resource'
if not os.path.isdir(path):
    os.mkdir(path)

work_path = r'./work_dir'
if not os.path.isdir(work_path):
    os.mkdir(work_path)

# synonym dictionary
synonym_dict = {}
synonym_path = r'./synonym/synonym.txt'
with open(synonym_path, 'r') as syn:
    syn_str = syn.read().split('\n')
for each_row in syn_str:
    synonym_dict[each_row.split(',')[0]] = [item for item in each_row.split(',')]

# Jieba then replace by synonym dictionary
def dealWithSynonym(long_str):
    # Select words we need according to /dict
    # and append each word to tmp_list
    tmp_list = []
    long_str.replace(' ','')
    for word_select in word_list:
        if word_select in long_str:
            if word_select.upper() == 'JAVA' or word_select.upper() == 'JAVASCRIPT':
                continue
            elif word_select == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0] != 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) != None:
                # print(1,word_select)
                long_str = long_str.replace(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0], '')
                # print(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0])
                if word_select in long_str:
                    tmp_list.append(word_select.upper())
                # print(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0])
                continue
            elif word_select == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) == None:
                # print(2,word_select)
                continue
            else:
                # print(3,word_select)
                tmp_list.append(word_select.upper())
    long_str = long_str.upper()
    for word_select in word_list:
        if (word_select.upper() in long_str) and (not word_select.upper() in tmp_list):
            if word_select.upper() == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0] != 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) != None:
                # print(1, word_select)
                long_str = long_str.replace(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0], '')
                if re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) == 'R':
                    tmp_list.append(word_select.upper())
                # print(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0])
                continue
            elif word_select.upper() == 'JAVA':
                continue
            elif word_select.upper() == 'JAVASCRIPT':
                long_str = long_str.replace('JAVASCRIPT', '')
                tmp_list.append(word_select.upper())
            elif word_select.upper() == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) == None:
                # print(2, word_select)
                continue
            else:
                # print(3, word_select)
                tmp_list.append(word_select.upper())
    long_str = long_str.replace('JAVASCRIPT', '')
    for word_select in word_list:
        if (word_select.upper() in long_str) and (not word_select.upper() in tmp_list):
            if word_select.upper() == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0] != 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) != None:
                # print(1, word_select)
                long_str = long_str.replace(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0], '')
                if re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) == 'R':
                    tmp_list.append(word_select.upper())
                # print(re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str)[0])
                continue
            elif word_select.upper() == 'JAVA':
                tmp_list.append(word_select.upper())
            elif word_select.upper() == 'R' and re.compile('[a-zA-Z]*R[a-zA-Z]*').search(long_str) == None:
                # print(2, word_select)
                continue
            else:
                # print(3, word_select)
                tmp_list.append(word_select.upper())

    # Replace Synonym
    for word_key in synonym_dict:
        for word_value in  synonym_dict[word_key]:
            for num, operating_word in enumerate(tmp_list):
                if operating_word.upper() == word_value.upper():
                    tmp_list[num] = word_key
    tmp_list = list(set(tmp_list))

    tmp_str = ''
    for n, w in enumerate(tmp_list):
        tmp_str += w
        if n < len(tmp_list) - 1:
            tmp_str += ','

    return tmp_str

def getSkill(titleUrl):
    job_content = '工作內容'
    job_require = '條件要求'
    job_welfare = '公司福利'
    job_contact = '聯絡方式'
    tmp_list = [job_content, job_require, job_welfare, job_contact]

    job_skill_data = ''

    try:
        res = requests.get(titleUrl, headers=headers)
    except:
        print('Error', 'getSkill(titleUrl)', titleUrl)
        print('Wait a moment!')
        time.sleep(4)
        return tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3], job_skill_data

    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.select('section[class="info"]')
    for each_content in contents:
        for i, content_name in enumerate(tmp_list):
            try:
                p = each_content.select('div p')[0].text
            except IndexError:
                p = ''

            try:
                dl = each_content.select('div dl')[0].text
            except IndexError:
                dl = ''

            if content_name == each_content.select('h2')[0].text:
                tmp_list[i] = p + dl
                if tmp_list[i] == '':
                    tmp_list[i] == 'NA'
                # if content_name == '工作內容' or content_name == '條件要求':
                #     job_skill_data += p.replace('\n', '').replace('\t', '')
                #     for j in each_content.select('div dl dd[class="cate"] span'):
                #         job_skill_data += j.text.replace('\n', '').replace('\t', '')

    return tmp_list[0], tmp_list[1], tmp_list[2], tmp_list[3], dealWithSynonym(re.sub(r'[-:_0-9、【】：)(，.&+]', '', (tmp_list[0].replace('\n', '').replace('\t', '') + tmp_list[1].replace('\n', '').replace('\t', ''))))

'''
Keyword for a list of title and url
[["Title1", "URL1", "Skill"], ["Title2", "URL2", "Skill"]]
'''
timenow = time.strftime("%Y-%m-%d_%H%M")
def keywordForTitle(keyword, max_page = 0, save_separately = 0, cache = 15, from_page = 1):

    # Create a directory
    path = r'./job104_resource/%s_%s'%(keyword, timenow)
    if not os.path.isdir(path):
        os.mkdir(path)
    work_path = r'./work_dir/%s'%(keyword)
    if not os.path.isdir(work_path):
        os.mkdir(work_path)

    col_path = r'./config/col.txt'
    ohencoding_col = open(col_path, 'r').read().lower().split('\n')

    col = ['Job_company', 'Job Openings','Job_content', 'Job_require', 'Job_welfare', 'Job_contact', 'URL']
    if len(ohencoding_col) > 0:
        col += ohencoding_col
    df = pd.DataFrame(columns=col)

    pages = from_page
    title_url_list = list()
    # skill data
    job_skill_data_sum = ''
    while True:
        process_tag = 1

        print('Page %s ...\t==' % (pages), end='')
        url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%s&order=1&asc=0&page=%s&mode=s&jobsource=2018indexpoc'%(keyword, pages)
        try:
            res = requests.get(url, headers=headers)
        except:
            print('Error', 'keywordForTitle(keyword, max_page = 0)', url)
            print('Wait a moment!')
            time.sleep(4)
            continue
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select('div[class="b-block__left"] h2[class="b-tit"] a')
        company = soup.select('div[class="b-block__left"] ul[class="b-list-inline b-clearfix"] li a')
        print('==', end='')

        # Stoping conditions
        # If the page is empty -> stop
        if len(title) == 0:
            if process_tag < 30:
                print('  ' * (30 - process_tag), end='')
            print('Empty!')
            break

        # [["Title1", "URL1"], ["Title2", "URL2"]]
        for num, each_title in enumerate(title):
            ohencoding_col_tmp = []
            if len(ohencoding_col) > 0:
                ohencoding_col_tmp = [0 for item in ohencoding_col]
            tmp_title = each_title.text
            tmp_url = each_title['href'].replace('//', 'https://')
            # job_skill_data is a list of all skills
            job_content, job_require, job_welfare, job_contact, job_skill_data = getSkill(tmp_url)
            # skill data
            job_skill_data_sum += (job_skill_data + ',')

            # Do one-hot encoding
            title_url_list.append([tmp_title, tmp_url])
            for index, skill_col in enumerate(ohencoding_col):
                for check_skill in job_skill_data.split(','):
                    if check_skill.upper() == skill_col.upper():
                        ohencoding_col_tmp[index] = 1
                        continue
            tmp_col = [company[num].text, tmp_title, job_content, job_require, job_welfare, job_contact, tmp_url] + ohencoding_col_tmp
            df = df.append(pd.DataFrame([tmp_col], columns=col), ignore_index=True)
            print('==', end='')
            process_tag += 1
            time.sleep(random.randint(3,8)/10)

         # save skill data to a file every 15 pages
        if pages % cache == 0:
            with open(r'%s/%s'%(work_path, pages), 'w', encoding='utf-8') as skill:
                skill.write(job_skill_data_sum)
            job_skill_data_sum = ''

            if save_separately != 0:
                df.to_excel(r'%s/title_url_%s.xlsx' % (path, time.strftime("%Y-%m-%d_%H%M")), engine='xlsxwriter')
                col = ['Job_company', 'Job Openings', 'Job_content', 'Job_require', 'Job_welfare', 'Job_contact', 'URL']
                if len(ohencoding_col) > 0:
                    col += ohencoding_col
                df = pd.DataFrame(columns=col)

        # Stoping conditions
        if max_page != 0:
            if pages >= max_page:
                if process_tag < 30:
                    print('==' * (30 - process_tag), end='')
                print('Done!')
                break

        if process_tag < 30:
            print('=='*(30-process_tag), end='')
        print('Done!')
        if pages % cache == 0 and save_separately != 0:
            print('File has saved to %s' % (path))

        # Pause for 30 sec every 15 pages
        if pages % 15 == 0:
            print('----------\nTake a break for 30 sec.\n----------')
            time.sleep(30)
        pages += 1

    with open(r'%s/%s' % (work_path, pages), 'w', encoding='utf-8') as skill:
        skill.write(job_skill_data_sum)

    df.to_excel(r'%s/title_url_%s.xlsx'%(path, time.strftime("%Y-%m-%d_%H%M")), engine='xlsxwriter')
    print('File has saved to %s/title_url.xlsx'%(path))
    return title_url_list

# Count title amount
def keywordForTitle_countTitle(keyword, max_page = 0, from_page = 1):

    pages = from_page
    count_title = 0
    while True:
        url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%s&order=1&asc=0&page=%s&mode=s&jobsource=2018indexpoc'%(keyword, pages)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select('div[class="b-block__left"] h2[class="b-tit"] a')

        # Stoping conditions
        # If the page is empt -> stop
        if len(title) == 0:
            break

        # [["Title1", "URL1"], ["Title2", "URL2"]]
        for each_title in title:
            count_title += 1

        # Stoping conditions
        if max_page != 0:
            if pages >= max_page:
                break
        pages += 1
    return count_title

# Map reduce
def mrThread(file_path, mr_path, save_name):
    mr_dict = {}
    tmp_str = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        tmp_list = f.read().replace('\n','').split(',')
    for w in tmp_list:
        if w in mr_dict:
            mr_dict[w] += 1
        else:
            mr_dict[w] = 1

    for d in mr_dict:
        tmp_str += '%s:%s\n'%(d, mr_dict[d])

    with open(r'%s/%s'%(mr_path, save_name), 'w', encoding='utf-8') as f:
        f.write(tmp_str)
    # return tmp_str

if __name__ == "__main__":
    kyword = '大數據分析'
    pages = 0
    save_separately = 1
    cache = 15
    ori_par = [kyword, pages, save_separately, cache]
    with open(r'./config/conf.txt', 'r') as con:
        par = con.read().split('\n')
    # print(par)
    for n, p in enumerate(par):
        par[n] = p.split('=')[1].replace(' ', '')
        if n != 0:
            par[n] = int(par[n])
        if n == 1 or n == 2:
            if par[n] < 0:
                par[n] = ori_par[n]
        if n == 3:
            if par[n] < 1:
                par[n] = ori_par[n]
    # print(par)
    kyword = par[0]
    pages = par[1]
    save_separately = par[2]
    cache = par[3]

    print('[Config]')
    print('\tKeyword:\t\t\t%s'%(kyword))
    if pages == 0:
        print('\tPages:\t\t\t\t%s' % ('ALL'))
    else:
        print('\tPages:\t\t\t\t%s' % (pages))
    print('\tSave separately:\t\t%s' % (save_separately))
    print('\tCache:\t\t\t\t%s' % (cache))
    print('\n')

    print('[Querying for %s ...]'%(kyword))
    time.sleep(2)

    # Compute the amount of title
    print('Computing the amount of title... ', end='')
    title_amount = keywordForTitle_countTitle(kyword, pages)
    print('(%s)'%(title_amount))
    print('\n')
    time.sleep(2)

    print('[Loading data...]')
    # Crawl all title, url and content and save as file
    keyword_for_title_and_url = keywordForTitle(kyword, pages, save_separately, cache)
    time.sleep(1)

    # Print data
    # pprint.pprint(keyword_for_title_and_url)
    print('')
    print('[Done!]')

    # Map-reduce
    time.sleep(1)
    print('\n')
    print('[Computing the amount of each skill...]')

    work_path = r'./work_dir/%s' % (kyword)
    mr_path = r'%s/mr_%s' % (work_path, time.strftime("%Y-%m-%d_%H%M"))

    # cache_list = os.listdir(work_path)
    cache_list = [f for f in os.listdir(work_path) if f[0:2] != 'mr']
    threadList = list()
    for save_name, thr in enumerate(cache_list):
        threadList.append(threading.Thread(target=mrThread, args=(r'%s/%s' % (work_path, thr), mr_path, save_name)))

    if not os.path.isdir(mr_path):
        os.mkdir(mr_path)

    for i in threadList:
        i.start()
        # time.sleep(0.1)
    for i in threadList:
        i.join()

    tmp_mr = []
    tmp_mr_dict = {}
    for i in os.listdir(mr_path):
        with open(r'%s/%s'%(mr_path, i), 'r', encoding='utf-8') as f:
            tmp_mr += f.read().split('\n')
    # print(tmp_mr)
    for i in tmp_mr:
        if len(i.split(':')) != 2 or i.split(':')[0] == '':
            continue
        if i.split(':')[0] in tmp_mr_dict:
            tmp_mr_dict[i.split(':')[0]] += int(i.split(':')[1])
        else:
            tmp_mr_dict[i.split(':')[0]] = int(i.split(':')[1])

    tmp_str = ''
    for d in tmp_mr_dict:
        tmp_str += '%s:%s\n'%(d, tmp_mr_dict[d])

    path = r'./job104_resource/%s_%s' % (kyword, timenow)
    with open(r'%s/map_reduce_%s.txt'%(path, timenow), 'w', encoding='utf-8') as f:
        f.write(tmp_str)

    # Remove temporary MR file
    for rm in cache_list:
        os.remove(r'%s/%s'%(work_path, rm))

    print('Processes all done.\n')
    print('Check the following directories.')
    print('./job104_resource/%s_%s'%(kyword, timenow))

    time.sleep(100)