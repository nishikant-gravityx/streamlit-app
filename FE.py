import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta

import os


#Style

st.set_page_config(layout="wide")
path=str(date.today())+".csv"

if st.button("Fetch deals"):
    if(os.path.isfile(path)):
        st.warning("Already detected accounts for today, Try Again Tomorrow")
    else:
        st.warning("running script")
        os.system("python fetch_deals.py")
        st.warning("Done")



# from pages import page1
# from pages import page2
# from pages import page3

# x=pd.read_csv("../test_11_nov.csv")
x=pd.read_csv("main.csv")
x=x[["detected_at","created_at","name", "username", "description","tier","category","VC","followers_count"]]

#showing deals detected today, weekly, biweekly, monthly
detect_time = st.selectbox('Select:',['Today','Yesterday','2 Days back','Last week','Last 2 weeks','Month']) 


if detect_time == "Today" :
    st.write(x[x["detected_at"] == str(date.today()) ])

if detect_time == "Yesterday" :
    st.write(x[x["detected_at"] == str(date.today()-timedelta(days=1)) ])

if detect_time == "2 Days back" :
    st.write(x[x["detected_at"] == str(date.today()-timedelta(days=2)) ])


def stage(x):
    if x<=100:
        return "Very Early"
    if x<=300:
        return "Alpha"
    if x<=500:
        return "Early"
    if x<=1000:
        return "Pre-Seed"
    if x<=2000:
        return "Seed"
    return "Public"

x['stage'] =x['followers_count'].apply(stage)


def time(x):
    if  x >= date.today()-timedelta(days=7):
        return 'Last Week'
    elif x >= date.today()-timedelta(days=15):
        return 'Last Two Weeks'
    elif x >= date.today()-timedelta(days=30):
        return 'Last Month'
    elif x >= date.today()-timedelta(days=90):
        return 'Last 3 Months'
    elif x >= date.today()-timedelta(days=120):
        return 'Last 4 Months'
    elif x >= date.today()-timedelta(days=150):
        return 'Last 5 Months'
    elif x >= date.today()-timedelta(days=180):
        return 'Last 6 Months'
    elif x >= date.today()-timedelta(days=210):
        return 'Last 7 Months'
    elif x >= date.today()-timedelta(days=240):
        return 'Last 8 Months'
    elif x >= date.today()-timedelta(days=365):
        return 'Last 12 Months'
    elif x >= date.today()-timedelta(days=500):
        return 'Last 18 Months'
    elif x >= date.today()-timedelta(days=720):
        return 'Last 24 Months'
    elif x >= date.today()-timedelta(days=1080):
        return 'Last 36 Months'
    elif x >= date.today()-timedelta(days=1440):
        return 'Last 48 Months'
    elif x >= date.today()-timedelta(days=1800):
        return 'Last 60 Months'
    elif x >= date.today()-timedelta(days=2190):
        return 'Last 72 Months'
    elif x >= date.today()-timedelta(days=2555):
        return 'Last 84 Months'
    elif x >= date.today()-timedelta(days=2920):
        return 'Last 96 Months'
    elif x >= date.today()-timedelta(days=3285):
        return 'Last 108 Months'
    elif x >= date.today()-timedelta(days=3650):
        return 'Last 120 Months'
    return 'More than 10 years'

x['created_at'] = pd.to_datetime(x['created_at']).dt.date
x['Created'] =x['created_at'].apply(time)
    

    

with st.sidebar:
    st.markdown("Welcome")
    page = st.selectbox('Select:',['Home','VC','Category','Tier','Followers','Stage']) 

if page == 'Home':
    st.write("HomePage - Deals Dashboard")
    col1, col2,col3 = st.columns(3)

    with col1:
        fig,ax=plt.subplots()
        ax = x['category'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Category Name")
        ax.set_xlabel("Category Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col2:
        fig,ax=plt.subplots()
        ax = x['tier'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Tier Name")
        ax.set_xlabel("Tier Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col3:
        fig,ax=plt.subplots()
        ax = x['Created'].value_counts().plot(kind='bar',
                                            figsize=(14,8),
                                            title="Count for Stage of Creation")
        ax.set_xlabel("Account Creation")
        ax.set_ylabel("Age")
        st.pyplot(fig)


    cl1,cl2,cl3=st.columns(3)
    with cl1:
        fig,ax=plt.subplots()
        ax = x['stage'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Tier Name")
        ax.set_xlabel("Tier Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with cl2:
        fig,ax=plt.subplots()
        ax = x['VC'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Tier Name")
        ax.set_xlabel("Tier Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with cl3:
        st.write("Mean", x["followers_count"].describe())
    

    c1,c2,c3,c4=st.columns(4)

    with c1:
        vc=x["VC"].unique()
        vc=st.selectbox("Select VC",tuple(vc))

    with c2:
        category=x["category"].unique()
        category=st.selectbox("Select Category",tuple(category))

    with c3:
        stage=x["stage"].unique()
        stage=st.selectbox("Select Stage",tuple(stage))

    with c4:
        tier=x["tier"].unique()
        tier=st.selectbox("Select Tier",tuple(tier))

    st.write( 
        x[(x["VC"]==vc)
        & (x["category"]== category)
        & (x["stage"]== stage )
        & (x["tier"]== tier ) 
        ]
    )

    
if page == 'VC':
    st.write("VC View")
    vc=x["VC"].unique()
    vc=st.selectbox("Select VC",tuple(vc))


    x=x[x["VC"]==vc]
    c1,c2,c3=st.columns(3)

    with c1:


        fig,ax=plt.subplots()
        ax = x['category'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Category Name")
        ax.set_xlabel("Category Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)


    with c2:

        fig,ax=plt.subplots()
        ax = x['tier'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Tier Name")
        ax.set_xlabel("Tier Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with c3:
        fig,ax=plt.subplots()
        ax = x['stage'].value_counts().plot(kind='pie',
                                            figsize=(14,8),
                                            title="Number for each Tier Name")
        ax.set_xlabel("Tier Names")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    
    st.dataframe(x[x["VC"]==vc])
    
    s1,s2,s3=st.columns(3)

    with s1:
        category=x["category"].unique()
        category=st.selectbox("Select Category",tuple(category))

    with s2:
        stage=x["stage"].unique()
        stage=st.selectbox("Select Stage",tuple(stage))


    with s3:
        tier=x["tier"].unique()
        tier=st.selectbox("Select Tier",tuple(tier))

    # st.write( 
    #     x[(x["VC"]==vc)
    #     & (x["category"]== category)
    #     & (x["stage"]== stage )
    #     & (x["tier"]== tier ) 
    #     ]
    # )




if page == 'Category':
    st.write("Category View")
    category=x["category"].unique()
    category=st.selectbox("Select Category",tuple(category))
    st.dataframe(x[x["category"]==category])
    # Page3.run()

if page=="Followers":
    st.write("followerrs")

if page=="Stage":
    st.write("Stage")
    stage=x["stage"].unique()
    stage=st.selectbox("Select Stage",tuple(stage))
    st.dataframe(x[x["stage"]==stage])

if page=="Tier":
    st.write("Category View")
    tier=x["tier"].unique()
    tier=st.selectbox("Select Tier",tuple(tier))
    st.dataframe(x[x["tier"]==tier])


# #Style End


# st.title('Deals Dashboard')



# # with col1:
# #    #category
# #     category=st.selectbox("Select Category",tuple(category))
# #     st.dataframe(x[x["category"]==category])

# # with col2:
# #     tier=st.selectbox("Select Tier",tuple(tier))
# #     st.dataframe(x[x["tier"]==tier])


# # time_frame=(7,14,30,90,180)
# # with col3:
# #     time_selection=st.selectbox("Select Days",time_frame)
# #     st.dataframe(x.loc[(x["created_at"]>=str(date.today()-timedelta(days=time_selection)))])



# category=st.selectbox("Select Category",tuple(category))
# st.dataframe(x[x["category"]==category])

# tier=st.selectbox("Select Tier",tuple(tier))
# st.dataframe(x[x["tier"]==tier])

# time_frame=(7,14,30,90,180)
# time_selection=st.selectbox("Select Days",time_frame)
# st.dataframe(x.loc[(x["created_at"]>=date.today()-timedelta(days=int(time_selection)))])

# # st.write("Selected Tier :- "+str(tier))
# # st.write("Selected Category :- "+str(category))
# # st.dataframe(x[(x["tier"]==tier) & (x["category"]==category) ])



# #Stage




