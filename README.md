# DV_Cancer
using :
pyton(flask,Plotly,Altair)

### 資料夾結構 ###

├─code (程式碼&網站程式碼html)  
│  │  DV2022S_FP_Cancer.py (主程式)  
│  │  readme.txt  
│  │  
│  ├─assets  
│  │  └─img  
│  │      favicon.ico (網站用到的圖片)  
│  │
│  ├─js  
│  │      scripts.js (網站模板)  
│  │
│  ├─static  
│  │      styles.css (網站模板)  
│  │  
│  └─templates  
│          index.html (網站主頁面)  
│
├─input (資料集)  
│      air.csv (空污資料)  
│      cancer.csv (癌症資料)  
│      new_cancer_air.csv (空污癌症資料)  
│      new_cancer_air_region.csv (空污癌症區域資料)  
│      region.csv (台灣區域資料)  
│      twCounty2010.geo.json (台灣經緯度資料)  
│  
└─output (輸出的html)  
        AgeMed_Pyramid.html (癌症發生年齡中位數分布)  
        air_country_count_heatmap.html (空污對比癌症發生率)  
        cancer_count.html (每年各類別癌症發生數量)  
        cancer_rate.html (每年各癌症發生率變化)  
        countsANDrate_vs_who2000.html (每年發生癌症數-台灣發生率 vs WHO2000年齡標準化發生率)  
        county_AvgAge.html (各縣市癌症的平均年齡)  
        county_count_heatmap.html (每年各地區癌症發生數量)  
        Sex_top5_2019.html (2019年男女癌症前五名)  
        top10.html (發生數前十名的癌症種類)  
        who_rate_bubbleChart.html (各縣市who v.s 台灣發生率)  
        year_cancer_top5.html (歷年各癌症發生數前五縣市)  

#### 各類癌症發生數
<img width="494" alt="各類癌症發生數" src="https://github.com/hizirong/DV_Cancer/assets/91252074/8ec3eb9b-f0fe-4d89-a084-ab1f4693ee5a">

#### 每年各地癌症發生數
<img width="494" alt="每年各地癌症發生數" src="https://github.com/hizirong/DV_Cancer/assets/91252074/3bc229f1-cce2-4914-818e-484fff74682f">

#### 空汙對比癌症發生率
<img width="524" alt="空汙對比癌症發生率" src="https://github.com/hizirong/DV_Cancer/assets/91252074/fb71f964-ec3f-44ec-8758-8827f5795b37">

#### 台灣vsWHO2000癌症發生數
![台灣vsWHO2000癌症發生數](https://github.com/hizirong/DV_Cancer/assets/91252074/4f56d30b-e9a3-41a9-92ab-e28fbd3ff4f4)


### 使用套件與環境設定 ###
python 3.7 or 3.8  
flask 		      (pip install flask)  
numpy           (pip install numpy)  
plotly 		      (pip install plotly)  
pandas 		      (pip install pandas)  
plotly-express	(pip install plotly-express)  
json		        (pip install jsons)  
altair          (pip install altair)  

### 執行步驟 ###
執行Code資料夾中的DV2022S_FP_Cancer.py
並按下輸出的網址進入網站(網站會跑有點久)
