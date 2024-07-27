# Importing all the libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

# Connecting to MYSQL database
mydb = mysql.connector.connect(host="localhost", user="root", password="sakthi", auth_plugin='mysql_native_password')
mycursor = mydb.cursor()
mycursor.execute("USE PhonePe")

# Collecting all the data from database from all tables
mycursor.execute('''SELECT * FROM aggregated_insurance''')
table1 = mycursor.fetchall()
aggregated_insurance = pd.DataFrame(table1, columns=["States", "Year", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM aggregated_transaction''')
table2 = mycursor.fetchall()
aggregated_transaction = pd.DataFrame(table2, columns=["States", "Year", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM aggregated_user''')
table3 = mycursor.fetchall()
aggregated_user = pd.DataFrame(table3, columns=["States", "Year", "Quarter", "Transaction_device", "Transaction_count","Transaction_percentage"])


mycursor.execute('''SELECT * FROM map_insurance''')
table4 = mycursor.fetchall()
map_insurance = pd.DataFrame(table4, columns=["States", "Year", "Quarter", "District_name", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM map_transaction''')
table5 = mycursor.fetchall()
map_transaction = pd.DataFrame(table5, columns=["States", "Year", "Quarter", "District_name", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM map_user''')
table6 = mycursor.fetchall()
map_user = pd.DataFrame(table6, columns=["States", "Year", "Quarter", "District_name", "Registered_users","App_opens"])


mycursor.execute('''SELECT * FROM top_insurance''')
table7 = mycursor.fetchall()
top_insurance = pd.DataFrame(table7, columns=["States", "Year", "Quarter", "Pincodes", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM top_transaction''')
table8 = mycursor.fetchall()
top_transaction = pd.DataFrame(table8, columns=["States", "Year", "Quarter", "Pincodes", "Transaction_count","Transaction_amount"])

mycursor.execute('''SELECT * FROM top_user''')
table9 = mycursor.fetchall()
top_user = pd.DataFrame(table9, columns=["States", "Year", "Quarter", "Pincodes", "Registered_users"])


# Geo Json contains latitudes and longitudes which helps us to present data as Geo visualization
def geo_json():

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response = requests.get(url)

    mapping = json.loads(response.content)

    return mapping


# Function for transaction and insurance data visualization for country analysis
# choropleth is used for graphical representation 
def trans_ins_map(df,fet,tit):

    geo_features = geo_json()

    if fet == "Transaction amount":

        map1 = px.choropleth(df, geojson= geo_features, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_amount",
                color_continuous_scale= "viridis", range_color=(df['Transaction_amount'].min(), df['Transaction_amount'].max()),  
                title= tit + " " + "Transaction Amount", fitbounds="locations", height = 700)
        
        map1.update_geos(visible = False)

        st.plotly_chart(map1, use_container_width=True)

        bar1 = px.bar(df,x= "States",y = "Transaction_amount", title = tit + " " + "Transaction Amount", 
                        color_discrete_sequence = px.colors.sequential.Blackbody_r, height = 500, text_auto=True)
        
        bar1.update_xaxes(tickangle=90)
    
        st.plotly_chart(bar1)

   
    elif fet == "Transaction Count":

        map2 = px.choropleth(df, geojson= geo_features, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_count",
        color_continuous_scale= "viridis", range_color=(df['Transaction_count'].min(), df['Transaction_count'].max()),  
        title=  tit + " " + "Transaction Count", fitbounds="locations", height = 700)
        
        map2.update_geos(visible = False)

        st.plotly_chart(map2, use_container_width=True)


        bar2 = px.bar(df,x= "States",y = "Transaction_count", title = tit + " " + "Transaction Count", 
                    color_discrete_sequence = px.colors.sequential.matter, height = 500, text_auto=True)
        
        bar2.update_xaxes(tickangle=90)
        
        st.plotly_chart(bar2)
        

# Function for transaction and insurance tab buttons for country analysis
def inp_buttons_trans(df, k):

        yt = st.toggle("Year wise", key = k[0])
        qt = st.toggle("Quarter wise", key= k[1])
        fet = st.radio("Select Feature",["Transaction amount", "Transaction Count"],key=k[2])

        if yt:
            selected_y = st.slider("Select Year", df['Year'].min(),df['Year'].max())

            state_y = df[df['Year'] == selected_y]
            state_y.reset_index(drop= True, inplace= True)

            state_gy = state_y.groupby('States')[['Transaction_amount', 'Transaction_count']].sum()
            state_gy.reset_index(inplace= True)


            if qt:
                opt = df[df["Year"]  == selected_y]['Quarter'].unique().tolist()
                selected_q = st.radio("Select Quarter", opt, key =k[3] )

                state_q = state_y[state_y['Quarter'] == selected_q]
                state_q.reset_index(drop= True, inplace= True)

                state_gq = state_q.groupby('States')[['Transaction_amount', 'Transaction_count']].sum()
                state_gq.reset_index(inplace= True)

                trans_ins_map(state_gq, fet, str(selected_y) + " " + "Quarter" + " " + str(selected_q))


            else:
                trans_ins_map(state_gy, fet, str(selected_y) )


        else :
            tot_st = df.groupby('States')[['Transaction_amount', 'Transaction_count']].sum()
            tot_st.reset_index(inplace= True)
            trans_ins_map(tot_st,fet,"Total")



# Function for User data visualization for country analysis
def users_map(df,tit):

    geo_features = geo_json()

    map1 = px.choropleth(df, geojson= geo_features, locations= "States", featureidkey= "properties.ST_NM", color= "Registered_users",
              color_continuous_scale= "Hot", range_color=(df['Registered_users'].min(), df['Registered_users'].max()),  
              title= tit + " " + "Registered Users", fitbounds="locations", height=700)
    
    map1.update_geos(visible = False)

    st.plotly_chart(map1, use_container_width=True)


    bar3 = px.bar(df,x= "States",y = "Registered_users", title = tit + " " + "Registered Users", 
                color_discrete_sequence = px.colors.sequential.Purples_r, height = 500,text_auto=True)

    bar3.update_xaxes(tickangle=90)

    st.plotly_chart(bar3)


    bar4 = px.bar(df,x= "States",y = "App_opens", title = tit + " " + "App Opens", 
                color_discrete_sequence = px.colors.sequential.thermal_r, height = 500, text_auto=True)

    bar4.update_xaxes(tickangle=90)

    st.plotly_chart(bar4)


# Function for User tab buttons for country analysis
def inp_but_user(df):
            
    yt = st.toggle("Year wise", key='a')
    qt = st.toggle("Quarter wise", key='b')

    if yt:
        selected_y = st.slider("Select Year", df['Year'].min(),df['Year'].max(), key='c')

        user_y = df[df['Year'] == selected_y]
        user_y.reset_index(drop= True, inplace= True)

        user_gy = user_y.groupby('States')[['Registered_users', 'App_opens']].sum()
        user_gy.reset_index(inplace= True)


        if qt:
            opt = map_user[map_user["Year"]  == selected_y]['Quarter'].unique().tolist()
            selected_q = st.radio("Select Quarter", opt, key='d')

            user_q = user_y[user_y['Quarter'] == selected_q]
            user_q.reset_index(drop= True, inplace= True)

            user_gq = user_q.groupby('States')[['Registered_users', 'App_opens']].sum()
            user_gq.reset_index(inplace= True)

            users_map(user_gq, str(selected_y) + " " + "Quarter" + " " + str(selected_q))

        else:
            users_map(user_gy, str(selected_y))


    else :
        user_tot = map_user.groupby('States')[['Registered_users', 'App_opens']].sum()
        user_tot.reset_index(inplace= True)
        users_map(user_tot, "Total")



# Function for transaction and insurance data visualization for state analysis
def trans_ins_dist(df,tit,state):

    co1,co2 = st.columns(2)

    with co1:

        chart1 = px.bar(df,x= "District_name",y= "Transaction_amount",
                    title = tit + " " + "Transaction Amount" + " " + "for" + " " + state + " "+ "District", 
                        color_discrete_sequence = px.colors.sequential.Oryel_r, height = 600, width=600, text_auto=True)
        
        chart1.update_xaxes(tickangle=90)

        st.plotly_chart(chart1)


    with co2:

        chart2 = px.bar(df,x= "District_name",y = "Transaction_count",
                    title = tit + " " + "Transaction Count" + " " + "for" + " " + state + " "+ "District", 
                    color_discrete_sequence = px.colors.sequential.Greens_r, height = 600, width=600, text_auto=True)
        
        chart2.update_xaxes(tickangle=90)

        st.plotly_chart(chart2)


# Function for transaction and insurance tab buttons for state analysis
def inp_but_trans_dist(df,state,k,p):

    yt = st.toggle("Year wise",key= k[0])
    qt = st.toggle("Quarter wise", key=k[1])
    
    if yt:
        selected_y = st.slider("Select Year", df['Year'].min(),df['Year'].max())

        state_yr = df[df['States'] == state]
        district_y = state_yr[state_yr['Year'] == selected_y]
        district_y.reset_index(drop= True, inplace= True)

        district_gy = district_y.groupby('District_name')[['Transaction_amount', 'Transaction_count']].sum()
        district_gy.reset_index(inplace= True)

        if qt:

            opt = state_yr[state_yr["Year"]  == selected_y]['Quarter'].unique().tolist()
            selected_q = st.radio("Select Quarter", opt, key =k[2])

            district_q = district_y[district_y['Quarter'] == selected_q]
            district_q.reset_index(drop= True, inplace= True)

            district_gq = district_q.groupby('District_name')[['Transaction_amount', 'Transaction_count']].sum()
            district_gq.reset_index(inplace= True)

            trans_ins_dist(district_gq, str(selected_y) + " " + "Quarter" + " " + str(selected_q),state)

        else:
            trans_ins_dist(district_gy, str(selected_y),state)

    else:

        adf= df[df['States'] == state].groupby('Year')[['Transaction_amount', 'Transaction_count']].sum()
        adf.reset_index(inplace= True)

        area1 = px.area(adf, x ='Year', y= 'Transaction_amount', title= "Transaction Amount Trend over the Years for "  + " " + state,
                        color_discrete_sequence = px.colors.sequential.Sunsetdark,text='Transaction_amount',)
        
        st.plotly_chart(area1)

        if p:
            pdf = aggregated_transaction[aggregated_transaction['States'] == state].groupby('Transaction_type')[['Transaction_amount', 'Transaction_count']].sum()
            pdf.reset_index(inplace= True)

            p1 = px.pie(pdf, names='Transaction_type', values='Transaction_amount',title='Transaction Types for' + " " + state,
                        color_discrete_sequence=px.colors.sequential.PuBuGn_r, hole= 0.5, height=500)
            
            st.plotly_chart(p1)



# Function for User data visualization for state analysis
def user_dist(df, tit, state):

    co3,co4 = st.columns(2)

    with co3:

        chart1 = px.bar(df,x= "District_name",y= "Registered_users",
                    title = tit + " " + "Registered Users" + " " + "for" + " " + state + " "+ "District", 
                        color_discrete_sequence = px.colors.sequential.Mint_r, height = 600, width=600, text_auto=True)
        
        chart1.update_xaxes(tickangle=90)

        st.plotly_chart(chart1)


    with co4:

        chart2 = px.bar(df,x= "District_name",y = "App_opens",
                    title = tit + " " + "App Opens" + " " + "for" + " " + state + " "+ "District", 
                    color_discrete_sequence = px.colors.sequential.dense_r, height = 600, width=600, text_auto=True)
        
        chart2.update_xaxes(tickangle=90)

        st.plotly_chart(chart2)

    

# Function for User tab buttons for state analysis
def inp_but_dist_user(df, sel_st):
            
    yt = st.toggle("Year wise",key= 'p')
    qt = st.toggle("Quarter wise", key='q')

    if yt:

        selected_y = st.slider("Select Year", df['Year'].min(),df['Year'].max(), key ='g')

        state_yr = df[df['States'] == sel_st]
        user_dis_y = state_yr[state_yr['Year'] == selected_y]
        user_dis_y.reset_index(drop= True, inplace= True)

        user_dis_gy = user_dis_y.groupby('District_name')[['Registered_users', 'App_opens']].sum()
        user_dis_gy.reset_index(inplace= True)

        if qt:

            opt = state_yr[state_yr["Year"]  == selected_y]['Quarter'].unique().tolist()
            selected_q = st.radio("Select Quarter", opt, key = 'r')

            user_dis_q = user_dis_y[user_dis_y['Quarter'] == selected_q]
            user_dis_q.reset_index(drop= True, inplace= True)

            user_dis_gq = user_dis_q.groupby('District_name')[['Registered_users', 'App_opens']].sum()
            user_dis_gq.reset_index(inplace= True)

            user_dist(user_dis_gq, str(selected_y) + " " + "Quarter" + " " + str(selected_q),sel_st)

        else:
            user_dist(user_dis_gy, str(selected_y),sel_st)
    
    else:

        adf= map_user[map_user['States'] == sel_st].groupby('Year')[['Registered_users', 'App_opens']].sum()
        adf.reset_index(inplace= True)

        area2 = px.area(adf, x ='Year', y= 'Registered_users', title= "Registered Users Trend over the Years for "  + " " + sel_st,
                        color_discrete_sequence = px.colors.sequential.solar_r,text='Registered_users')
        
        st.plotly_chart(area2)


        pdd = aggregated_user[aggregated_user['States'] == sel_st].groupby('Transaction_device')[['Transaction_count', 'Transaction_percentage']].sum()
        pdd.reset_index(inplace= True)

        p2 = px.pie(pdd, names='Transaction_device', values='Transaction_count',title='Types of Mobile Transaction for' + " " + sel_st,
                color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5, height=500)
        
        st.plotly_chart(p2)



    


# Basic streamilt UI funcrions
st.set_page_config(layout="wide")

st.title(":violet[Phone Pe Pulse Data Exploration and Visualization]")

option = option_menu(None,options = ["Home","Data Visualization","Top Insights"],
                       icons = ["house-door","binoculars","clipboard-data-fill"],
                       default_index=0,
                       orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#DD33FF"}})


if option == "Home":

    st.subheader(":violet[About]")

    st.image(Image.open("D:/PhonePe_Project/App_pic.jpeg"),width=500,)

    st.write("")

    st.markdown('''PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. 
                    PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. 
                    The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. 
                    It is owned by Flipkart, a subsidiary of Walmart.''')
    st.write("")
    
    st.subheader(':violet[Phonepe Pulse]')

    st.write('''The Indian digital payments story has truly captured the world's imagination. 
                From the largest towns to the remotest villages, there is a payments revolution being driven by the 
                penetration of mobile phones and data.''')

    st.write('''PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and 
                in-depth analysis based on our data put together by the PhonePe team.''')
    
    st.write(":violet[We have Used the Phone Pe Pulse data to visulaize the data with geo maps and charts to get insights from them ]")



elif option == "Data Visualization":

    selected = option_menu(None,options=["Country Analysis", "State Analysis"],
                            icons = ["globe","bar-chart-fill"],
                            default_index=0,
                            orientation="horizontal",
                            styles={"nav-link-selected": {"background-color": "#DD33FF"}})
    

    if selected == "Country Analysis":

        tab1,tab2,tab3 = st.tabs(["Transaction", "Insurance", "User"])

        with tab1 :

            inp_buttons_trans(aggregated_transaction, [1,2,3,4])
        
        with tab2:

            inp_buttons_trans(aggregated_insurance, [5,6,7,8])


        with tab3:

            inp_but_user(map_user)



    elif selected == "State Analysis":

        tab3,tab4,tab5 = st.tabs(["Transaction", "Insurance", "User"])

        with tab3:

            opt1 = map_transaction["States"].unique().tolist()

            sel_st = st.selectbox("Select any state",opt1,key = 's')

            inp_but_trans_dist(map_transaction,sel_st,['x','y','z'],1)


        with tab4:

            opt1 = map_insurance["States"].unique().tolist()

            sel_st = st.selectbox("Select any state",opt1, key = 't')

            inp_but_trans_dist(map_insurance,sel_st,['a','b','c'],0)


        with tab5:

            opt1 = aggregated_user["States"].unique().tolist()

            sel_st = st.selectbox("Select any state",opt1, key = 'u')

            inp_but_dist_user(map_user, sel_st)




elif option == "Top Insights" :
    
    choice = ["Top 10 States with highest transactions",
              "Top 10 states with highest registered users",
              "Top 10 states with lowest transactions",
              "Top 10 states with lowest registered users",
              "Top 10 Districts with highest transactions",
              "Top 10 Districts with highest registered users",
              "Top 10 Districts with lowest transactions",
              "Top 10 Districts with lowest registered users",
              "Top 10 Mobiles with highest transactions"]
    

    sel_ques = st.selectbox("Select any option", choice, index= None)


    if sel_ques == "Top 10 States with highest transactions" :

        mycursor.execute('''SELECT States, sum(Transaction_amount) Total_Transaction_Amount
                            FROM aggregated_transaction
                            GROUP BY States
                            ORDER BY Total_Transaction_Amount desc
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['States','Total Transaction Amount'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'States', y = 'Total Transaction Amount', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Burgyl_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)


    if sel_ques == "Top 10 states with highest registered users":

        mycursor.execute('''SELECT States, sum(Registered_users) Total_Registered_users
                            FROM map_user
                            GROUP BY States
                            ORDER BY Total_Registered_users desc
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['States','Total Registered Users'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'States', y = 'Total Registered Users', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Aggrnyl_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)



    if sel_ques == "Top 10 states with lowest transactions" :
    
        mycursor.execute('''SELECT States, sum(Transaction_amount) Total_Transaction_Amount
                            FROM aggregated_transaction
                            GROUP BY States
                            ORDER BY Total_Transaction_Amount 
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['States','Total Transaction Amount'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'States', y = 'Total Transaction Amount', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Darkmint, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)



    if sel_ques == "Top 10 states with lowest registered users" :

        mycursor.execute('''SELECT States, sum(Registered_users) Total_Registered_users
                            FROM map_user
                            GROUP BY States
                            ORDER BY Total_Registered_users 
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['States','Total Registered Users'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'States', y = 'Total Registered Users', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Oryel_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)




    if sel_ques == "Top 10 Districts with highest transactions" :

        mycursor.execute('''SELECT District_name, States, sum(Transaction_amount) Total_Transaction_Amount
                            FROM map_transaction
                            GROUP BY District_name,States
                            ORDER BY Total_Transaction_Amount desc
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['Districts', 'States','Total Transaction Amount'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'Districts', y = 'Total Transaction Amount', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Greens_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)



    if sel_ques == "Top 10 Districts with highest registered users" :

        mycursor.execute('''SELECT District_name, States, sum(Registered_users) Total_Registered_users
                            FROM map_user
                            GROUP BY District_name,States
                            ORDER BY Total_Registered_users desc
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['Districts','States','Total Registered Users'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'Districts', y = 'Total Registered Users', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Plasma_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)


    if sel_ques == "Top 10 Districts with lowest transactions" :

        mycursor.execute('''SELECT District_name, States, sum(Transaction_amount) Total_Transaction_Amount
                            FROM map_transaction
                            GROUP BY District_name,States
                            ORDER BY Total_Transaction_Amount 
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['Districts', 'States','Total Transaction Amount'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'Districts', y = 'Total Transaction Amount', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.ice_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)




    if sel_ques == "Top 10 Districts with lowest registered users" :

        mycursor.execute('''SELECT District_name, States, sum(Registered_users) Total_Registered_users
                            FROM map_user
                            GROUP BY District_name,States
                            ORDER BY Total_Registered_users 
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['Districts','States','Total Registered Users'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.bar(df1, x= 'Districts', y = 'Total Registered Users', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Pinkyl_r, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)



    if sel_ques == "Top 10 Mobiles with highest transactions" :

        mycursor.execute('''SELECT Transaction_device, sum(Transaction_count) Total_Transaction_count
                            FROM aggregated_user
                            GROUP BY Transaction_device
                            ORDER BY Total_Transaction_count desc
                            limit 10''')

        myresult = mycursor.fetchall()

        df1 = pd.DataFrame(myresult, columns = ['Mobile Brands','Total Transaction Count'])

        c1,c2 = st.columns(2)

        with c1:

            b1 = px.pie(df1, names= 'Mobile Brands', values = 'Total Transaction Count', title = sel_ques,
                        color_discrete_sequence = px.colors.sequential.Hot_r,hole=0.5, height = 600, width=600)
            
            b1.update_xaxes(tickangle=90)
            
            st.plotly_chart(b1)

        with c2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)
