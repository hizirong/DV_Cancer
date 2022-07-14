#from lib2to3.pgen2.pgen import DFAState
from flask import Flask, render_template,request # pip install flask
import plotly # pip install plotly
import plotly.graph_objs as go

import numpy as np
import pandas as pd # pip install pandas
import json

import altair as alt
import requests

import plotly.express as px
from plotly.subplots import make_subplots
import os
inputPath = os.path.join("..", "Input")
outputPath = os.path.join("..", "Output")

app = Flask(__name__)

@app.route('/')
def index():
    df = LoadData()
    p1_plot = country_count_heatmap(df)
    p2_plot = cancer_count(df)
    p3_plot = Sex_top5_2019(df) # county_count_bar(df)
    p4_plot = county_AvgAge(df)
    p5_plot = who_rate_bubbleChart(df)
    p6_plot = year_cancer_top5(df)
    p7_plot = air_country_count_heatmap(df)
    p8_plot = cancer_rate(df)
    p9_plot = countsANDrate_vs_who2000(df)
    p10_plot = top10(df)
    p11_plot = AgeMed_Pyramid(df)
    p12_plot = country_Peoplecount_heatmap(df)
    return render_template('index.html', 
        plot1 = p1_plot, plot2 = p2_plot, plot3 = p3_plot, 
        plot4 = p4_plot, plot5 = p5_plot, plot6 = p6_plot,
        plot7 = p7_plot, plot8 = p8_plot, plot9 = p9_plot, 
        plot10 = p10_plot, plot11 = p11_plot, plot12 = p12_plot)
 
# ======== 資料前處理

# #-- 合併癌症與空汙資料
# def data_merge_air():
#     cancer_df = pd.read_csv(inputPath + "/cancer.csv",encoding = "utf-8-sig")
#     air_data = pd.read_csv(inputPath + "/air.csv",encoding = "utf-8-sig")
#     new_data = pd.merge(cancer_df, air_data, on=['Year','Country'],how='outer')
#     new_data.to_csv(inputPath +"/new_cancer_air.csv",encoding = "utf-8-sig") # 存檔
#     print(new_data)

# #-- 合併癌症空汙與地區資料
# def data_merge_air_region():
#     cance_air_df = pd.read_csv(inputPath + "/new_cancer_air.csv",encoding = "utf-8-sig")
#     region_data = pd.read_csv(inputPath + "/region.csv",encoding = "utf-8-sig")
#     new_data = pd.merge(cance_air_df, region_data, on=['Country'],how='outer')
#     new_data.to_csv(inputPath +"/new_cancer_air_region.csv",encoding = "utf-8-sig") # 存檔
#     print(new_data)

# #-- 合併癌症空汙與地區資料與人口資料
# def data_merge_air_region():
#     cance_air_df = pd.read_csv(inputPath + "/new_cancer_air_region.csv",encoding = "utf-8-sig")
#     region_data = pd.read_csv(inputPath + "/county_peopleCount.csv",encoding = "utf-8-sig")
#     new_data = pd.merge(cance_air_df, region_data, on=['Year','Country'],how='outer')
#     new_data.to_csv(inputPath +"/new_cancer_air_region_people.csv",encoding = "utf-8-sig") # 存檔
#     print(new_data)
    

def LoadData(dataset=inputPath+'/new_cancer_air_region_people.csv'):
    # Read File
    cancer_df = pd.read_csv(dataset, encoding = 'utf-8')
    # preview dataframe
    print("Cancer history data head-10 -->", cancer_df.head(10))
    print("Cancer history data shape -->", cancer_df.shape)
    print("Cancer history data info. -->", cancer_df.info())
    print("Cancer history numerical data -->\n", cancer_df.describe())
    print("Cancer history categorical data -->\n",cancer_df.describe(include=object))
    return cancer_df
# 1: 每年各地癌症發生數量熱度圖 
def country_count_heatmap(df):
    fliter1 = (df["Cancer"] == "全癌症")# 刪除全癌症總和類型
    fliter2 = (df["Country"] != "全國") # 刪除全國總和資訊
    fliter3 = (df["Sex"] == "全")       # 刪除男女總和資訊
    new_data = df[fliter1&fliter2&fliter3]
    #print(new_data)
    new_data["Country"] = new_data["Country"].str.replace("桃園市", "桃園縣") # 調整桃園市為桃園縣(地圖為2010版本，當時為縣)
    
    # 開啟台灣地區經緯度
    with open(inputPath + "/twCounty2010.geo.json", encoding="utf-8") as fp:
        geojson_map = json.load(fp)
    
    # 繪製台灣癌症發生率熱度圖
    fig = px.choropleth(new_data,
                        geojson = geojson_map,
                        featureidkey = "properties.COUNTYNAME",
                        locations = "Country",
                        color = "Count",
                        animation_frame = "Year",
                        range_color = (0,20000), # color range
                        height=560, width= 900,
                        color_continuous_scale="plasma" # 熱度圖顏色
                    )  
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        mapbox_style = "carto-positron", 
        mapbox_zoom = 6, # 比例設定
        mapbox_center = {"lat": 23.9, "lon": 121.52}, # 地圖中心經緯度
    )
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>每年各地癌症發生數變化</b>", title_x=0.5)
    fig.write_html(outputPath +"/county_count_heatmap.html")
    return plot_json
# 2: 每年各類癌症發生數量折線圖 
def cancer_count(df): 
    # 篩選所需資料
    all = (df['Country'] == '全國')&(df['Cancer'] != '全癌症')&(df['Sex'] == '全')
    df = df.loc[all]
    # plot
    fig = px.line(df, x="Year", y="Count", 
                  color='Cancer', 
                  range_y=[0,17100], 
                  range_x=[1979,2019], 
                  height=650, width= 900,
                  markers=True, color_discrete_sequence=px.colors.qualitative.Set2)
    # update menu setting
    Cancer_type = df['Cancer'].unique()
    buttons=[]
    buttons.append(dict(label='All',
                            method='update',
                            args=[{'visible':[True for j in Cancer_type]},
                                {'showlegend':True}]
                            ))   
    for index,i in enumerate(Cancer_type):
        buttons.append(dict(label=i,
                            method='update',
                            args=[{'visible':[True if j==(index) 
                                              else False for j in range((len(Cancer_type)))]},
                                {'showlegend':True}]))    
    fig.update_layout(
        template="ggplot2",
        xaxis=dict(rangeslider=dict(visible=True)), # add slider
        legend=dict(y=0.87),  # adjust legend position
        updatemenus=[         # updatemenu setting & position
            dict(
                direction = "down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.02,
                xanchor="left",
                y=1.02,
                # yanchor="top",
                buttons=buttons
            )
        ]
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>每年各類癌症發生數量變化</b>", title_x=0.5)
    fig.write_html(outputPath+'/cancer_count.html')
    return plot_json
# 3: 2019男女top5
def Sex_top5_2019(df):
    # 篩選資料
    need = (df['Country'] == '全國')&(df['Sex'] != '全')&(df['Cancer'] != '全癌症')&(df['Year'] == 2019)
    df = df.loc[need]
    # 資料整理(排序)
    dfsort = df.sort_values(by=['Count'])
    df_m = dfsort.loc[(dfsort['Sex'] == '男')]
    df_f = dfsort.loc[(dfsort['Sex'] == '女')]

    male = go.Bar(  x=df_m['Count'],
                    y=df_m['Cancer'],
                    orientation='h',
                    text=df_m['Cancer'],
                    marker = {'color' : 'rgb(128,177,211)'},
                    # name="male",
                    )
    female = go.Bar(x=df_f['Count'],
                    y=df_f['Cancer'],
                    orientation='h',
                    text=df_f['Cancer'],
                    marker = {'color' : 'rgb(251,128,114)'},
                    # name="female",
                    )

    fig = make_subplots(rows=1,cols=2,subplot_titles=("<b>男性</b>", "<b>女性</b>"))
    fig.append_trace(male,1,1)
    fig.append_trace(female,1,2)

    # 取前五筆資料
    fig.layout.yaxis1.range = [31.5,37.5] #男性癌症數: 38
    fig.layout.yaxis2.range = [33.5,39.5] #女性癌症數: 40
    fig.layout.xaxis1.range = [0,15500]
    fig.layout.xaxis2.range = [0,15500]
    fig.layout.yaxis1.visible= False
    fig.layout.yaxis2.visible= False

    fig.update_traces(textposition='inside')
    fig.update_layout(width=900, height=560, showlegend=False)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>2019年男女癌症前五名</b>", title_x=0.5)
    fig.write_html(outputPath+'/Sex_top5_2019.html')
    return plot_json
# 4: 各縣市癌症的平均年齡 
def county_AvgAge(df):
    # need data 
    need = (df['Country'] != '全國')&(df['Sex'] == '全')&(df['Cancer'] == '全癌症')
    df = df.loc[need]
    # plot
    fig = px.scatter(df, x="Year", y="AgeAvg", color='Country',height=650, width= 900, template='none',
                    marginal_y = "histogram", range_y=[35,68], color_discrete_sequence = px.colors.qualitative.T10)#,text="AgeAvg")
    # updatemenu
    County_type = df['Country'].unique()
    buttons=[]
    buttons.append(dict(label='全國',
                            method='update',
                            args=[{'visible':[True for j in County_type]},
                                {'showlegend':True}]
                            )) 
    for index,i in enumerate(County_type):
        buttons.append(dict(label=i,
                            method='update',
                            args=[{'visible':[True if j==2*(index) else True if j==2*(index)+1 else False for j in range(2*(len(County_type)))]},
                                {'showlegend':True}]
                            ))
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        legend=dict(y=0.85),  # adjust legend position
        updatemenus=[         # updatemenu setting & position
            dict(
                direction = "down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.02,
                xanchor="left",
                y=0.99,
                yanchor="top",
                buttons=buttons
            )
        ]
    )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>各地區癌症的平均年齡</b>", title_x=0.5)
    fig.write_html(outputPath+'/county_AvgAge.html')
    return plot_json
# 5: 各縣市who與發生率泡泡圖 
def who_rate_bubbleChart(df):
    #刪除全癌症總和類型
    fliter1 = (df["Cancer"] != "全癌症")
    #刪除全國總和資訊
    fliter2 = (df["Country"] != "全國")
    #刪除男女總和資訊
    fliter3 = (df["Sex"] != "全")
    new_data = df[fliter1&fliter2&fliter3]
    fig = px.scatter(new_data, x="WHO2000", y="IncidenceRate",
                      #title="全國癌症發生率 v.s WHO區域發生率",
                      size="Count", color="Cancer",
                      animation_frame="Year",
                      animation_group="Country",
                      facet_col="Region",
                      hover_name="Country",
                      size_max=60,
                      range_x=[0,100], # x軸範圍
                      range_y=[0,140], # y軸範圍
                      color_discrete_sequence=px.colors.cyclical.mygbm
                      )
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>各縣市who與發生率變化圖</b>", title_x=0.5)
    fig.write_html(outputPath +"/who_rate_bubbleChart.html")
    return plot_json
# 6: 歷年癌症發生數前五地區 
def year_cancer_top5(df):
    #刪除全癌症總和類型
    fliter1 = (df["Cancer"] != "全癌症")
    #刪除全國總和資訊
    fliter2 = (df["Country"] != "全國")
    #刪除男女總和資訊
    fliter3 = (df["Sex"] == "全")
    new_data = df[fliter1&fliter2&fliter3]
    
    # 資料整理(排序)
    dfsort = new_data.sort_values(by=['Year','Cancer','Count'],ascending=False)
    fig = px.bar(dfsort, x='Count', y='Country',#,hover_data=['Sex'], 
                orientation='h',
                range_y=[-0.5,4.5] ,
                #text='Count', 
                color='Cancer',
                animation_frame='Year', 
                height=580, width= 900,
                title="",
                color_discrete_sequence=px.colors.qualitative.Set3
                )
    
    Cancer_type = dfsort['Cancer'].unique()
    #print(Cancer_type)
    buttons=[]
    for index,i in enumerate(Cancer_type):
        buttons.append(dict(label=i,
                            method='update',
                            args=[{'visible':[True if j==(index) else False for j in range(len(Cancer_type))]},
                                {'showlegend':True}]
                            ))
    buttons.append(dict(label='All',
                            method='update',
                            args=[{'visible':[True for j in Cancer_type]},
                                {'showlegend':True}]
                            ))   
    fig["layout"].pop("updatemenus") # optional, drop animation buttons
    
    fig.update_layout(
        legend=dict(y=0.90),
        updatemenus=[
            dict(
                type='dropdown',
                showactive=False,
                direction='down',# right for type = 'buttons'
                active=0,
                x=1.43,
                y=1.02,
                buttons=buttons,
            )
        ]
    )
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save to output
    fig.update_layout(title_text="<b>歷年各癌症發生數前五縣市</b>", title_x=0.5)
    fig.write_html(outputPath +"/year_cancer_top5.html")
    return plot_json
# 7: 空污對比肺、支氣管及氣管發生率 
def air_country_count_heatmap(df):   
    alt.data_transformers.enable('default', max_rows=None) # 解決altair to json問題
    # 刪除空汙空值
    df = df.dropna(subset=['PSI_AQI'])
    #刪除全癌症總和類型
    fliter1 = (df["Cancer"] != "全癌症")
    #刪除全國總和資訊
    fliter2 = (df["Country"] != "全國")
    #刪除男女總和資訊
    fliter3 = (df["Sex"] == "全")
    
    new_data = df[fliter1&fliter2&fliter3]
    
    highlight = alt.selection_single() 
    
    select = alt.selection_single(encodings=['x', 'y']) # 選取熱度圖格子
    
    chart = alt.Chart(new_data).mark_rect().encode(
        x=alt.X('Year:N'), #bin=True, 
        y=alt.X('Country') ,#bin=True),
        color=alt.condition(highlight, 'PSI_AQI', alt.value('linen'), scale=alt.Scale(scheme="lightmulti"))
    ).add_selection(
        highlight, select
    ).properties(height=550)


    hist = alt.Chart(new_data).mark_bar().encode(
        y='Cancer',
        x='IncidenceRate',
        tooltip=['Year', 'Country', 'Count'],
        color=alt.value('lightcoral'),
        
    ).transform_filter(
        select
    ).properties(height=550)

    fig = alt.hconcat(chart, hist)
    # fig.save(outputPath+'/p7addcircle.json')
    with open(outputPath+'/p7.json') as p7:
        data = json.load(p7)

    fig_title = alt.hconcat(chart, hist, center=True, title="台灣空汙指數 v.s 癌症發生率")
    fig_title = fig_title.configure_title(fontSize=25, offset=5, orient='top', anchor='middle')   
    fig_title.save(outputPath +"/air_country_count_heatmap.html") # 有標題
    
    return data

# 8: 每年各癌症發生率變化 
def cancer_rate(df):
    # need data
    all = (df['Country'] == '全國')&(df['Sex'] == '全')&(df['Cancer'] != '全癌症')
    df_all = df.loc[all]
    # print(df_all.head(30))
    # plot
    fig = px.line(df_all, x="Year", y="IncidenceRate", color='Cancer', height=650, width= 900,
                    range_y=[0,75], hover_data=['Country'], color_discrete_sequence = px.colors.qualitative.Vivid)#,text="AgeAvg")
    # updatemenu
    Cancer_type = df_all['Cancer'].unique()
    buttons=[]
    buttons.append(dict(label='All',
                            method='update',
                            args=[{'visible':[True for j in Cancer_type]},
                                {'showlegend':True}]
                            ))  
    for index,i in enumerate(Cancer_type):
        buttons.append(dict(label=i,
                            method='update',
                            args=[{'visible':[True if j==(index) else False for j in range(len(Cancer_type))]},
                                {'showlegend':True}]
                            ))
    fig.update_layout(
        legend=dict(y=0.87),  # adjust legend position
        updatemenus=[         # updatemenu setting & position
            dict(
                direction = "down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.02,
                xanchor="left",
                y=1.03,
                yanchor="top",
                buttons=buttons
            )
        ]
    )
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # save
    fig.update_layout(title_text="<b>每年各癌症發生率變化</b>", title_x=0.5)
    fig.write_html(outputPath+'/cancer_rate.html')

    return plot_json
# 9: 每年發生癌症數(男女比) - 台灣發生率 vs WHO2000年齡標準化發生率 
def countsANDrate_vs_who2000(df):
    need = (df['Country'] == '全國')&(df['Cancer'] == '全癌症')
    df = df.loc[need]#.drop_duplicates(subset=['Year', 'Cancer'])
    print('need data : \n',df[['Year','Count','Sex','WHO2000','IncidenceRate']])
    print('Check data : \n',df.loc[(df['Sex'] == '全')][['Year','IncidenceRate']])
    # for Year,  Sex, WHO2000, Count, IncidenceRate in df_all['0','1','4','5','8']:
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df_m = df_all = df.loc[(df['Sex'] == '男')]
    df_f = df_all = df.loc[(df['Sex'] == '女')]
    
    #-- Bar
    fig.add_trace(go.Bar(
        x=df_m['Year'],
        y=df_m['Count'],    
        name='男性',
        marker = {'color':px.colors.qualitative.Set3[6]},#{'color' : 'rgb(57,105,172)'}
        ),secondary_y = False)
    fig.add_trace(go.Bar(
        x=df_f['Year'],
        y=df_f['Count'],
        name='女性',
        marker = {'color':px.colors.qualitative.Set3[5]},#{'color' : 'rgb(248,156,116)'}
        ),secondary_y = False)
    
    df_all = df.loc[(df['Sex'] == '全')]
    #-- Line
    fig.add_trace(go.Scatter(
        x=df_all['Year'],
        y=df_all['WHO2000'],
        name='WHO2000',
        marker = {'color':px.colors.qualitative.T10[0]},#{'color' : 'rgb(242,183,1)'}
    ),secondary_y = True)
    fig.add_trace(go.Scatter(
        x=df_all['Year'],
        y=df_all['IncidenceRate'],
        name='IncidenceRate',
        marker = {'color':px.colors.qualitative.T10[2]},#{'color' : 'rgb(128,186,90)'}
    ),secondary_y = True)    
    
    # axes setting
    fig.update_layout(barmode='stack', template='seaborn',legend=dict(x=0.03,y=0.95))
    fig.update_yaxes(title_text="<b>人數</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>每十萬人口</b>", secondary_y=True,range=[0,600])
    fig.update_xaxes(title_text="<b>年</b>")

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save
    fig.update_layout(title_text="<b>每年發生癌症數 - 台灣發生率 vs WHO2000年齡標準化發生率</b>", title_x=0.5)
    fig.write_html(outputPath+'/countsANDrate_vs_who2000.html')
    return plot_json
# 10: 全國每年發生數量top10的癌症 
def top10(df):
    # 篩選資料
    need = (df['Country'] == '全國')&(df['Sex'] == '全')&(df['Cancer'] != '全癌症')
    df = df.loc[need]
    # 資料整理(排序)
    dfsort = df.sort_values(by=['Year','Count'])
    dfsort = dfsort.drop_duplicates(subset=['Year','Cancer'], keep='first') # drop重複值
    # plot
    fig = px.bar(dfsort, x='Count', y='Cancer',#,hover_data=['Sex'], 
                orientation='h',
                range_y=[23.5,33.5], 
                range_x=[100,18000],
                # text='Count',
                color_discrete_sequence=['Chocolate'],#px.colors.diverging.RdYlGn[3],
                #template='none',
                animation_frame='Year', height=650,width= 850)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # save
    fig.update_layout(title_text="<b>全國每年十大癌症</b>", title_x=0.5)
    fig.write_html(outputPath+'/top10.html')
    return plot_json

# 癌症發生年齡中位數分布
def AgeMed_Pyramid(df):
    # 男女資料
    df_m = df.loc[(df['Country'] == '全國')&(df['Cancer'] != '全癌症')&(df['Sex']=='男')]
    df_f = df.loc[(df['Country'] == '全國')&(df['Cancer'] != '全癌症')&(df['Sex']=='女')]

    # 顯示年齡區間的人數
    m_count = df_m['AgeMed'].value_counts(bins=40,sort=False) # 男
    f_count = df_f['AgeMed'].value_counts(bins=40,sort=False) # 女
    # print('male\n',m_count,'female\n',f_count)

    fig = go.Figure()
    y = list(range(40,80,5))

    #=== age : under30, 31-40, 41-50, 51-60, 61-70, 71-80
    men_bins = np.array([113,102,221,456,604,63])
    women_bins = np.array([-94,-112,-306,-522,-541,-84])

    fig.add_trace(go.Bar(y=y,
                x=men_bins,
                orientation='h',
                name='Men',
                text=men_bins,
                # hoverinfo='text',
                marker=dict(color='powderblue')
                ))
    fig.add_trace(go.Bar(y=y,
                x=women_bins,
                orientation='h',
                name='Women',
                text=-1 * women_bins.astype('int'),
                # hoverinfo='text',
                marker=dict(color='salmon')
                ))
    fig.update_layout(barmode='overlay',bargap=0.1,width=650,height=600)
    fig.update_xaxes(range=[-610,610],title='Number',
                    tickvals=[-610,-500,-400,-300,-200,-100, 0, 100,200,300,400,500,610],
                    ticktext=[610,500,400,300,200,100, 0,100,200,300,400,-610])
    fig.update_yaxes(tickvals=[30,31,41,51,61,71],ticktext=['30歲以下','30-40', '40-50', '50-60', '60-70', '70-80']) 
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig.update_layout(title_text="<b>癌症發生年齡中位數分布</b>", title_x=0.5)
    fig.write_html(outputPath+'/AgeMed_Pyramid.html')   
    return plot_json  

#-- 歷年台灣地區發生數熱度圖 v.s 人口數  
def country_Peoplecount_heatmap(df):
    
    # 刪除全癌症總和類型
    fliter1 = (df["Cancer"] == "全癌症")
    # 刪除全國總和資訊
    fliter2 = (df["Country"] != "全國")
    # 刪除男女總和資訊
    fliter3 = (df["Sex"] == "全")
    fliter4 = (df["Year"] == 2019)
    new_data = df[fliter1&fliter2&fliter3&fliter4]
    
    # 調整桃園市為桃園縣
    new_data["Country"] = new_data["Country"].str.replace("桃園市", "桃園縣")
    
    # 開啟台灣地區經緯度
    with open(inputPath + "/twCounty2010.geo.json", encoding="utf-8") as fp:
        geojson_map = json.load(fp)
        
    mapbox = requests.get('https://api.mapbox.com/?access_token=myaccesstoken').text
    fig = make_subplots(
        rows=1, cols=2, subplot_titles=('2019 各縣市人口', '2019 各縣市癌症發生人口'),
        specs=[[{"type": "mapbox"}, {"type": "mapbox"}]]
    )
    
    fig.add_trace(go.Choroplethmapbox(geojson=geojson_map, 
                                      locations=new_data['Country'], 
                                      z=new_data['PeopleCount'],
                                      featureidkey="properties.COUNTYNAME",
                                      colorscale='matter_r',
                                      name='人口數',
                                      colorbar=dict(thickness=20, x=0.46),
                                      marker=dict(opacity=0.75)), row=1, col=1)
    fig.add_trace(go.Choroplethmapbox(geojson=geojson_map, 
                                      locations=new_data['Country'], 
                                      z=new_data['Count'],
                                      featureidkey="properties.COUNTYNAME",
                                      colorscale='matter_r',
                                      name='癌症發生數',
                                      colorbar=dict(thickness=20, x=1.02),
                                      marker=dict(opacity=0.75, line_width=0.5)), row=1, col=2)
    fig.update_mapboxes(
            bearing=0,
            accesstoken=mapbox,
            center = {"lat": 23.9, "lon": 121.52},
     )
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=10));
    #HERE YOU CAN CONTROL zoom
    fig.update_layout(mapbox1=dict(zoom=5.9, style='carto-positron'),
                      mapbox2=dict(zoom=5.9, style='carto-positron'));
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    fig.update_layout(title_text="<b>2019年癌症發生數 V.S 人口數</b>", title_x=0.5)
    fig.write_html(outputPath +"/country_Peoplecount_heatmap.html") 
    return plot_json         

if __name__ == '__main__':
    app.run()
