### Work104功能說明
將104人力銀行上使用關鍵字搜索結果，包含公司資訊、職缺名稱、聯絡資訊、所需技能等結果
以Excel逐筆呈現，並將技能數量以TXT檔做個別小計。

### Work104使用方式

※	以下步驟中文字檔維護方式：英文不分大小寫，不同技能需換行輸入。

1.	將班級內所有可在104上做關鍵字搜尋的技能維護至dict \ bigData.txt文字檔內。

2.	並將同義字（例如AI=artificial intelligence=人工智慧）維護至synonym \ synonym.txt文字檔內，以半形逗號分隔。

3.	且在config \ col.txt文字檔內，將要呈現在爬取結果Excel上的技能逐筆維護。

4.	config \ conf.txt則是設定檔案的輸出方式。設定方式如下：
kyword=設定成要做為在104上搜尋的關鍵字。
pages=要抓取的搜尋結果頁數。設0=全部。
save_separately=爬取結果的檔案存放份數。設0代表全部資料輸出成同一份Excel，其他數字代表要分開存，此欄位不可輸入負數。
cache=設定爬蟲抓取幾頁搜尋結果就存成一份新的Excel。

5.	以上設定完後，點選work104_v2.exe，等到出現
[Computing the amount of each skill...]
Processes all done.，就代表資料抓取完畢囉。

6.	到job104_resource資料夾內查看爬取結果，map_reduce開頭的文字檔是技能個別小計數量；title_url開頭的Excel檔則是公司資訊、職缺名稱、聯絡資訊、所需技能(1=有，0=無)….等詳細資料。

### 輸出範例
#### 資料夾畫面
![dataframe](https://github.com/uuboyscy/work104/blob/master/output-folder.png)
#### Excel畫面
![excel](https://github.com/uuboyscy/work104/blob/master/output-dataframe.png)
#### Word count
![word count](https://github.com/uuboyscy/work104/blob/master/output-wordcount.png)
