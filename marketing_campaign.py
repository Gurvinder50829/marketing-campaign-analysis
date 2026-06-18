import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from plotly.subplots import make_subplots
import plotly.graph_objects as go
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gurvinder@SQL2026",
        database="marketing_campany"
    )
    df = pd.read_sql("SELECT * FROM marketing_Data",conn)
    print(df.info())
    conn.close()
    df.columns = df.columns.str.strip()
    product_cols = [
        "MntWines",
        "MntFruits",
        "MntMeatProducts",
        "MntFishProducts",
        "MntSweetProducts",
        "MntGoldProds"
    ]
    df["Total_Sales"] = df[product_cols].sum(axis=1)
    current_year = datetime.now().year
    df["Age"] = (current_year- df["Year_Birth"])
    return df
df = load_data()
st.title("📊 Marketing Campaign Dashboard")
st.subheader(
    "Customer Insights & Campaign Performance Analysis"
)
st.sidebar.markdown("# 📊 Marketing Dashboard")
st.sidebar.markdown(
    "## AI Powered Insights System"
)
page = st.sidebar.radio(
    "🧭 Navigation",
    [
        "📊 Key Performance Indicators (KPIs)",
        "📌 Customer Overview",
        "🛒 Product Consumption Insights",
        "🛍️ Purchase Channel Analytics",
        "📱 Digital Engagement Analytics",
        "📢 Marketing Campaign Performance",
        "💰 Customer Value & Profitability Analytics",
        "🤖 Predictive Analytics"
    ]
)
# then making the plot of the "📊 Key Performance Indicators (KPIs)":
if page=="📊 Key Performance Indicators (KPIs)":
    with st.container(border=True):
        st.subheader("📊 Key Performance Indicators (KPIs)")
    with st.container(border=True):
        st.markdown("## 👤 Age Analysis")
    m1,m2=st.columns(2)
    m3,m4=st.columns(2)
    max_age = df["Age"].max()
    min_age = df["Age"].min()
    m1.metric("🔺 Max Age", max_age)
    m2.metric("🔻 Min Age", min_age)
# older customer and the new customer
    m3.metric("🧓Oldest Customer",f"{df["Age"].max()}.yrs")
    m4.metric("🧒Newest Customer",f"{df["Age"].min()}.yrs")
# the show the  max and min income 
    with st.container(border=True):
        st.markdown("## 💰 Income Analysis")
    m5,m6=st.columns(2)
    m7,m8=st.columns(2)
    Max_Income =df["Income"].max()
    Min_Income =df["Income"].min()
    m5.metric("🔺Max Income",Max_Income)
    m6.metric("🔻Min Income",Min_Income)
# maximum education having maximum count
    with st.container(border=True):
        st.markdown("## 🎓 Education Analysis")
    m9,m10=st.columns(2)
    m11,m12=st.columns(2)
    edu_income = df.groupby("Education")["Income"].mean().reset_index()
    top_edu = edu_income.loc[edu_income["Income"].idxmax()]
    low_edu = edu_income.loc[edu_income["Income"].idxmin()]
# avg income
    m7.metric("💸 Avg Income", f"{low_edu['Income']:,.0f}")
    m8.metric("💰 Avg Income", f"{top_edu['Income']:,.0f}")
    m11.metric("🏆 Highest Income Edu", top_edu["Education"])    
    m12.metric("📉 Lowest Income Edu", low_edu["Education"])

if page == "📌 Customer Overview":
    st.subheader("📌 Customer Overview Dashboard")
# Customer Overview Container
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Customers", df["ID"].nunique())
    col2.metric("💰 Total Income", df["Income"].sum())
    col3.metric("⚠️ Total Complaints", df["Complain"].sum())
    col4.metric("📈 Total Sales", df["Total_Sales"].sum())
    # then making the plot in the customer overview dashboard
    st.subheader("📌 Customer Overview Dashboard Visualizations")
    col1,col2,col3 = st.columns(3)
    col4,col5,col6 =st.columns(3)

    with col1:
        fig1 =go.Figure()
        fig1.add_trace(go.Histogram(x=df["Age"],nbinsx=40,marker=dict(
               color="#00BFFF",line=dict(color="black",width=1))))
        fig1.update_traces(marker_line_color="black",marker_line_width=1)
        fig1.update_layout(title="Age Distribution",height=300)
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",  
            margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 =go.Figure()
        fig2.add_trace(go.Histogram(x=df["Income"],nbinsx=40,marker =dict(
            color="#39FF14",line=dict(color="black",width=1))))     
        fig2.update_traces(marker_line_color="black",marker_line_width=1)
        fig2.update_layout(title="📊 Income Distribution",height=300,template="plotly_white")              
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 =px.bar(df,x="Education",title="Education_Distributions",color="Education")
        fig3.update_layout(height=300)
        st.plotly_chart(fig3,use_container_width=True)
# making column wish plot format
    with st.container(border=True):
        with col4:
            fig4 =px.bar(df,x="Marital_Status",title="Marital Status",template="plotly_white")
            fig4.update_layout(height=300)
            st.plotly_chart(fig4,use_container_width=True)
    # income vs Edcations
        with col5:
            edu_income = df.groupby("Education")["Income"].mean().reset_index()
            fig5 = px.bar(edu_income,x="Education",y="Income",color="Education",height=250)
            fig5.update_layout(height=300)
            st.plotly_chart(fig5, use_container_width=True)
# income By Martial status
        with col6:
            fig6=px.bar(df,x="Education",y="Marital_Status",title="Education Distribution by Income",template="plotly_white")
            fig6.update_layout(height=300)            
            st.plotly_chart(fig6,use_container_width=True)
# kidhome
    col7,col8,col9=st.columns(3)
    with st.container(border=True):
        with col7:
            fig7 =px.histogram(df,x="Kidhome",title="Kidhome Distributions",nbins=30,color_discrete_sequence=["grey"])
            fig7.update_layout(height=300)
            st.plotly_chart(fig7,use_container_width=True)
# teenhome
        with col8:
            fig8 =px.histogram(df,x ="Teenhome",nbins=30,title="Teenhome Distributions",color_discrete_sequence=['Brown'])
            fig8.update_layout(height=300)
            st.plotly_chart(fig8,use_container_width=True)
# age vs income
        with col9:
            fig = px.scatter(df,x="Age",y="Income",size="Total_Sales",hover_data=["Marital_Status", "Kidhome", "Teenhome"],title="📊 Customer Age vs Income (Segmentation Insight)",template="plotly_white")
            fig.update_layout(height=300,title_font_size=18,xaxis_title="Age of Customer",yaxis_title="Annual Income",legend_title="Education Level")
            st.plotly_chart(fig, use_container_width=True)

# /then the second plot 
elif page == "🛒 Product Consumption Insights":
    st.markdown("### 🥧 Product Contribution Analysis ")
    st.subheader("📌 Key Metrics")
    # then analysics the data of the Product Consumption Insights
    product_cols = ["MntWines", "MntFruits", "MntMeatProducts",
                "MntFishProducts", "MntSweetProducts","MntGoldProds"]
    Sales =df[product_cols].sum().reset_index()
    Sales.columns =["Product","Sales"]
    print("\nSales Distribution By Product\n",Sales)
    Total_Product_Sales =Sales["Sales"].sum()
    print("\nTotal Product Sales\n",Total_Product_Sales)
    # then find the mntwines using age 
    MntWines_consumption =df[["ID","MntWines"]]
    # highest sales product
    Top_product =Sales.loc[Sales["Sales"].idxmax()]
    Low_product =Sales.loc[Sales["Sales"].idxmin()]

    # then making the metics of the product consumption insights
    st.markdown("### 🥧 Product Contribution Analysis Visulatizations ")
    col1,col2,col3 =st.columns(3)
    col4,col5= st.columns(2)
    col1.metric("💰 Total Product Sales",f"{Total_Product_Sales:.0f}")
    col2.metric("🏆 Highest Sale",f"{Top_product["Sales"]:.0f}")
    col3.metric("📉 Lowest Sale",f"{Low_product["Sales"]:.0f}")
    col4.metric("📈Highest Saling Product",Top_product["Product"])
    col5.metric("📉Lowest Saling Product",Low_product["Product"])
# then making the plot of the visulization the data
    st.markdown("### 🥧 Product Contribution Analysis Visulatizations ")
    col1,col2,col3 =st.columns(3)
    with col1:
        with st.container(border=True):
            fig1 =px.bar(Sales,x="Product",y="Sales",color="Product",title="Total Product Sales Distributions",color_discrete_sequence=["pink"])
            fig1.update_layout(height=400)
            st.plotly_chart(fig1,use_container_width=True)
    with col2:
        with st.container(border=True):
            wine_edu = df.groupby("Education")["MntWines"].mean().reset_index()
            fig2 = px.bar(wine_edu,x="Education",y="MntWines",color="Education",title="Average Wine Consumption by Education",color_discrete_sequence=["blue"])
            fig2.update_layout(height=400)
            fig2.update_layout(xaxis_tickangle=90)
            fig2.update_layout(xaxis=dict(tickfont=dict(size=12)))            
            st.plotly_chart(fig2, use_container_width=True)

    with col3:
        with st.container(border=True):
            fruit_con =df.groupby("Education")["MntFruits"].mean().reset_index()
            fig3 =px.bar(fruit_con,x="Education",y="MntFruits",color="Education",title="Fruit Concumptions by Education",color_discrete_sequence=["brown"])
            fig3.update_layout(height=400)
            fig3.update_layout(xaxis_tickangle=90)      
            fig2.update_layout(xaxis=dict(tickfont=dict(size=12)))            
            st.plotly_chart(fig3,use_container_width=True)
        # then making the mit consumptions
    col4,col5,col6 =st.columns(3)
    with col4:
        with st.container(border=True):
            fruit_con =df.groupby("Education")["MntMeatProducts"].mean().reset_index()
            fig4 =px.bar(fruit_con,x="Education",y="MntMeatProducts",color="Education",title="Meat Concumptions by Education",color_discrete_sequence=["#8A2BE2"])
            fig4.update_layout(height=400)
            fig4.update_layout(xaxis_tickangle=90)      
            fig4.update_layout(xaxis=dict(tickfont=dict(size=12)))            
            st.plotly_chart(fig4,use_container_width=True)
    with col5:
        with st.container(border=True):
            fish_con =df.groupby("Marital_Status")["MntFishProducts"].mean().reset_index()
            fig5 =px.bar(fish_con,x="Marital_Status",y="MntFishProducts",color="Marital_Status",title="Fish Concumptions by Education",color_discrete_sequence=["#8D7F9B"])
            fig5.update_layout(height=400)
            fig5.update_layout(xaxis_tickangle=90)      
            fig5.update_layout(xaxis=dict(tickfont=dict(size=12)))            
            st.plotly_chart(fig5,use_container_width=True)
    with col6:
        with st.container(border=True):
            sweet_equ =df.groupby("Education")["MntSweetProducts"].mean().reset_index()
            fig6 =px.bar(sweet_equ,x="Education",y="MntSweetProducts",color="Education",title="Sweet Concumptions by Education",color_discrete_sequence=["#6FCF92"])
            fig6.update_layout(height=400)
            fig6.update_layout(xaxis_tickangle=90)      
            fig6.update_layout(xaxis=dict(tickfont=dict(size=12)))            
            st.plotly_chart(fig6,use_container_width=True)
    col7,col8,col9=st.columns(3)
    with col7:
        with st.container(border=True):
            gold_edi =df.groupby("Education")["MntGoldProds"].mean().reset_index()
            fig7 =px.bar(gold_edi,x="Education",y="MntGoldProds",color="Education",title="Sweet Consumption by Education",color_discrete_sequence=["#405EC3"]) 
            fig7.update_layout(height=400)
            fig7.update_layout(xaxis_tickangle=90)      
            fig7.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig7,use_container_width=True)
# product correlations
    with col8:
        with st.container(border=True):
            product_con =df[product_cols].corr()
            fig8 =px.imshow(product_con,text_auto=True,title="Total Product Cosumstion Relations")
            fig8.update_layout(height=400)
            fig8.update_layout(xaxis_tickangle=90)      
            fig8.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig8,use_container_width=True)
# total product spending distributions
    with col9:
        with st.container(border=True):
            df["Total_Product_spend"] = (df["MntWines"]+df["MntFruits"]+df["MntMeatProducts"]+df["MntFishProducts"]+df["MntSweetProducts"]+df["MntGoldProds"])
            fig9 =px.histogram(df["Total_Product_spend"],title="Total Product Spend")
            fig9.update_layout(height=400)
            fig9.update_layout(xaxis_tickangle=90)      
            fig9.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig9,use_container_width=True)
# then making the plot of the income vs channel revenue
Purchase_Channel =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
Channel_income =pd.DataFrame({
    "Purchase_Channel":Purchase_Channel,
    "Total_Purchase":[df[cols].sum() for cols in Purchase_Channel]
})
print(Channel_income)
# CHANNEL SHARES
Purchase_Channel =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
Channel_Shares =pd.DataFrame({
    "Purchase_Channel":Purchase_Channel,
    "Total_Purchase":[df[cols].sum() for cols in Purchase_Channel]
})
print(Channel_Shares)
# //revenue by Purchase Channel
Purchase_Channel_revenue  =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
Revenue_Channel =pd.DataFrame({
    "Purchase_Channel":Purchase_Channel_revenue,
    "Revenue":[df[cols].sum() for cols in Purchase_Channel_revenue]
})
# then the Subplot Purchase channel Visualization the data 
if page =="🛍️ Purchase Channel Analytics":
    st.markdown("## 🛒 Customer Purchase Behavior Across Sales Channels ")
    st.subheader("📌 Key Metrics")
    Purchase_Channel =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
    # then making the metrics of the data
    col1,col2,col3,col4,col5=st.columns(5)
    st.markdown("## 🛒 Customer Purchase Behavior Across Sales Channels Visualizations")
    co1,co2,co3 =st.columns(3)
    co4,co5,co6 =st.columns(3)
    co7,co8,co9 =st.columns(3)
    # then making the matrics 
    with st.container(border=True):
        col1.metric("🏷️ Deal Purchase Product",df["NumDealsPurchases"].sum())
    with st.container(border=True):
        col2.metric("🌐 Web Purchase Product",df["NumWebPurchases"].sum())
    with st.container(border=True):
        col3.metric("📖 Catalog Purchase Product",df["NumCatalogPurchases"].sum())
    with st.container(border=True):
        col4.metric("🏪 Store Purchase Product",df["NumStorePurchases"].sum())
    with st.container(border=True):
        col5.metric("👥 Web Visits Month Purchase Product",df["NumWebVisitsMonth"].sum())
# then making the store purchase product visualization 
    # then visulaization the plot of the subplots
    with st.container(border= True):
        with co1:
            fig1 =px.histogram(df,x="NumStorePurchases",nbins=30,title="Store Distribution Product",color_discrete_sequence=["pink"])
            fig1.update_layout(height=400)
            fig1.update_traces(marker_line_color="black",marker_line_width=1)
            fig1.update_layout(xaxis_tickangle=90)      
            fig1.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig1,use_container_width=True)
        with co2:
            fig2 =px.histogram(df,x="NumWebPurchases",nbins=30,title="Web Purchase Distributions",color_discrete_sequence=["Red"])
            fig2.update_layout(height=400)
            fig2.update_traces(marker_line_color="black",marker_line_width=1)
            fig2.update_layout(xaxis_tickangle=90)      
            fig2.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig2,use_container_width=True)
        with co3:
            fig3 =px.histogram(df,x="NumCatalogPurchases",nbins=30,title="Catlog Purchase Distributions",color_discrete_sequence= ["brown"])
            fig3.update_layout(height=400)
            fig3.update_traces(marker_line_color="black",marker_line_width=1)
            fig3.update_layout(xaxis_tickangle=90)      
            fig3.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig3,use_container_width=True)
    # second columns
    with st.container(border=True):
        with co4:
            fig4 =px.histogram(df,x="NumDealsPurchases",nbins=30,title="Deals Purchase Distributions",color_discrete_sequence= ["green"])
            fig4.update_layout(height=400)
            fig4.update_traces(marker_line_color="black",marker_line_width=1)
            fig4.update_layout(xaxis_tickangle=90)      
            fig4.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig4,use_container_width=True)
        with co5:
            fig5 =px.histogram(df,x="NumWebVisitsMonth",nbins=30,title="Web Visit Distributions",color_discrete_sequence= ["purple"])
            fig5.update_layout(height=400)
            fig5.update_traces(marker_line_color="black",marker_line_width=1)
            fig5.update_layout(xaxis_tickangle=90)      
            fig5.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig5,use_container_width=True)
        # income vs purchase
        with co6:
            fig6 =px.bar(Channel_income,x="Purchase_Channel",y="Total_Purchase",title="Purchase Channel VS Income",color_discrete_sequence=["blue"])
            fig6.update_layout(height=400)
            fig6.update_layout(xaxis_tickangle=90)      
            fig6.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig6,use_container_width=True)
        # income vs total purchase channel
        with co7:
            fig7 =px.bar(Channel_income,x="Purchase_Channel",y="Total_Purchase",title="Purchase Channel Shares",color_discrete_sequence=["orange"])
            fig7.update_layout(height=400)
            fig7.update_layout(xaxis_tickangle=90)      
            fig7.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig7,use_container_width=True)
        # Purchase Channel Revenue
        with co8:
            fig8 =px.bar(Revenue_Channel,x="Purchase_Channel",y="Revenue",title="Channel Revenue",color_discrete_sequence=["yellow"])
            fig8.update_layout(height=400)
            fig8.update_layout(xaxis_tickangle=90)
            st.plotly_chart(fig8,use_container_width=True)
        # purchase channel heatmap
        # channel corelations heatmap
        Purchase_Channel =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
        corr=df[Purchase_Channel].corr()
        with co9:
            fig9 =px.imshow(corr,text_auto=". 2f",aspect="auto",title="Channel Corelation heatmap")
            fig9.update_layout(xaxis_title="Channel",yaxis_title="Channel")
            st.plotly_chart(fig9,use_container_width=True)
# then making the plot of the"📱 Digital Engagement Analytics",
if page =="📱 Digital Engagement Analytics":
    st.markdown("## 📱 Digital Engagement Analytics ")
    st.subheader("📌 Key Metrics")
    # website visit distributions
    mt1,mt2,mt3,mt4,mt5=st.columns(5)
    # then visulization the plot of the digital Engagement analysics 
    st.markdown("## 📱 Digital Engagement Analytics Visualizations")
    col1,col2,col3 =st.columns(3)
    col4,col5,col6 =st.columns(3)
    col7,col8,col9 =st.columns(3)
    mt1.metric("💰 Total Income",df["Income"].sum())
    mt2.metric("👀 Total Web_Visit Month",df["NumWebVisitsMonth"].sum())
    mt3.metric("🛒 Aerage Web Purchase",round(df["NumWebPurchases"].mean(),2))
    mt4.metric("🌐 Total Wwb Purchase",df["NumWebPurchases"].sum())
    mt5.metric("📈 Convertion Rate",round(df["NumWebPurchases"].sum() /df["NumWebVisitsMonth"].sum() *100,2))
    # number of visit distributions 
    with col1:
        fig1 =px.histogram(df,x="NumWebVisitsMonth",nbins=30,title="Web Visting Distributions",color_discrete_sequence=["#63FAC3"])
        fig1.update_layout(height=400)
        fig1.update_layout(xaxis_tickangle=90)      
        fig1.update_layout(xaxis=dict(tickfont=dict(size=12)))
        fig1.update_traces(marker_line_color="black",marker_line_width=1)
        st.plotly_chart(fig1,use_container_width=True)
    with col2:
        fig2=px.bar(df,x="NumWebVisitsMonth",y="Age",title="Web Visiting Distribution by Age",color="Age")
        fig2.update_layout(height=400)
        fig2.update_layout(xaxis_tickangle=90)      
        fig2.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig2,use_container_width=True)
    with col3:
        fig3=px.bar(df,x="NumWebVisitsMonth",y="Income",title="Web Visiting Distribution by Income",color_discrete_sequence=["#FADC63"])
        fig3.update_layout(height=400)
        fig3.update_layout(xaxis_tickangle=90)      
        fig3.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig3,use_container_width=True)
    with col4:
        fig4 =px.bar(df,x="NumWebVisitsMonth",y="NumWebPurchases",color_discrete_sequence=["#2D3AEE"]  )
        fig4.update_layout(height=400)
        fig4.update_layout(xaxis_tickangle=90)      
        fig4.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig4,use_container_width=True)
    # web visit trends
    Web_Visit =df["NumWebVisitsMonth"].value_counts().sort_index().reset_index()
    Web_Visit.columns =["Web Visit","Customer Count"]
    with col5:
        fig5 =px.line(Web_Visit,x="Web Visit",y="Customer Count",title="Web Visit Trend",markers=True)
        fig5.update_layout(template ="plotly_dark",height=400)
        st.plotly_chart(fig5,use_container_width=True)\
    # web activity Trend
    Web_Visits =df["NumWebVisitsMonth"].value_counts().sort_index().reset_index()
    Web_Visits.columns=["Visit","Customer"]
    with col6:
        fig6 =px.line(Web_Visits,x='Visit',y="Customer",title="Web Activity Trend",markers=True,color_discrete_sequence=["#EE2D9A"])
        fig6.update_layout(height=400)
        st.plotly_chart(fig6,use_container_width=True)
    # engagement columns 
    Engegment_Col =["NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
    corr =df[Engegment_Col].corr()
    with col7:
        fig7 =px.imshow(corr,text_auto=True,aspect="auto",title="Customer Engagement Heatmap",color_continuous_scale="Blues")
        fig7.update_layout(height=400)
        st.plotly_chart(fig7,use_container_width=True)
        # then engagement vs responce 
    Engegement_Responce =df.groupby("Response")["NumWebVisitsMonth"].mean().reset_index()
    Engegement_Responce["Response"] =Engegement_Responce["Response"].map({
        0:"Not Execpted",1:"Excepted"})
    with col8:
            fig8 =px.bar(Engegement_Responce,x="NumWebVisitsMonth",y="Response",title="Engagement Responce",color_discrete_sequence=["#5C2243","#0B1B4A"])
            fig8.update_layout(height=400)
            fig8.update_layout(xaxis_tickangle=90)      
            fig8.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig8,use_container_width=True)
    # engagement by Education
    Engagement_Education =df.groupby("Education")["NumWebVisitsMonth"].mean().reset_index()
    # Engagement_Education_["Response"] =Engagement_Education["Response"].map({
    #     0:"Not Excepted",1:"Excepted"})
    with col9:
        fig9=px.bar(Engagement_Education,x="Education",y="NumWebVisitsMonth",title="Engagement By Education",color_discrete_sequence=["#BAB5B8","#12E8AB"])
        fig9.update_layout(height=400)
        fig9.update_layout(xaxis_tickangle=90)      
        fig9.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig9,use_container_width=True)
# then making the plot of the Marketing compaign performance

if page=="📢 Marketing Campaign Performance":
    with st.container(border=True):
        st.markdown("## 📢 Marketing Campaign Performance")
    with st.container(border=True):
        st.subheader("📌 Key Metrics")
    m1,m2,m3,m4 =st.columns(4)
    m5,m6,m7,m8 =st.columns(4)
    # then given the plot column positions
    st.markdown("## 📢 Marketing Campaign Performance Visualizations")
    with st.container(border=True):
        c1,c2,c3 =st.columns(3)
    with st.container(border=True):
        c4,c5,c6=st.columns(3)
    with st.container(border=True):
        c7,c8,c9=st.columns(3)

    # then create the matrics
    m1.metric("🎯 Total Compaign Responce",df["Response"].sum())
    m2.metric("📢 Compaign 3 Accepted",df["AcceptedCmp3"].sum())
    m3.metric("📢 Compaign 2 Accepted",df["AcceptedCmp2"].sum())
    m4.metric("📢 Compaign 1 Accepted",df["AcceptedCmp1"].sum())
    m5.metric("📢 Compaign 4 Accepted",df["AcceptedCmp4"].sum())
    m6.metric("📢 Compaign 5 Accepted",df["AcceptedCmp5"].sum())
    m7.metric("💬  Complain Count",df["Complain"].sum())
    m8.metric("📈 Overall Responce Rate",f"{(df["Response"].mean()*100):.2f}%")
    # then visualization the plot of the Marketing Compaign Performance
    # then create the column using for the plot
    with c1:
        compaign_Data ={
                        "Compaign_col" :["Com1","Comp2","Comp3","Comp4","Comp5"],
            "Accptance_Campaign" :[df["AcceptedCmp3"].sum(),df["AcceptedCmp2"].sum(),df["AcceptedCmp1"].sum(),df["AcceptedCmp4"].sum(),df["AcceptedCmp5"].sum()]    
            }
        fig1 =px.bar(compaign_Data,x="Compaign_col",y="Accptance_Campaign",title="Comapign Accptance Comparisions",color ="Accptance_Campaign")
        fig1.update_layout(height=400)
        fig1.update_layout(xaxis_tickangle=90)      
        fig1.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig1,use_container_width=True)
        # compaign Success
        Compaign_Success =pd.DataFrame({
            "Status":["Successfull","Unsuccessfull"],
            "Count":[
            df["Response"].sum(),
            len(df)-df["Response"].sum()]
        })
        print(Compaign_Success)
    # then making the plot of the Responce Success
    with c2:
        fig2 =px.bar(Compaign_Success,x="Status",y="Count",title="Compaign Success Rate",color ="Count")               
        fig2.update_layout(height=400)
        fig2.update_layout(xaxis_tickangle=90)      
        fig2.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig2,use_container_width=True)
    # compaign Contributions
    with c3:
        compaign_Donut ={
        "Compaign_col" :["Com1","Comp2","Comp3","Comp4","Comp5"],
        "Accptance_Campaign" :[df["AcceptedCmp3"].sum(),df["AcceptedCmp2"].sum(),df["AcceptedCmp1"].sum(),df["AcceptedCmp4"].sum(),df["AcceptedCmp5"].sum()]}
        fig3 =px.pie(compaign_Donut,names="Compaign_col",values="Accptance_Campaign",hole=0.5,title="Compaign Contributions")
        fig3.update_traces(textposition="inside",textinfo="percent+label")
        fig3.update_layout(height=400)
        st.plotly_chart(fig3,use_container_width=True)
    with c4:
        fig4 =px.histogram(df,x="Response",nbins=30,title="Response Distributions",color="Response")
        fig4.update_layout(height=400)
        fig4.update_layout(xaxis_tickangle=90)      
        fig4.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig4,use_container_width=True)
    # responce Vs Income
    Responce_Income =pd.DataFrame({
        "Response":df["Response"],
        "Income":df["Income"]
    })
    with c5:
        fig5 =px.bar(Responce_Income,x="Response",y="Income",title="Responce Distribution by Income",color_discrete_sequence=["#C4857A"])
        fig5.update_layout(height=400)
        fig5.update_layout(xaxis_tickangle=90)      
        fig5.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig5,use_container_width=True)
    # Age Responce
    Age_Response =pd.DataFrame({
        "Age":df["Age"],
        "Response":df["Response"]
    })
    with c6:
        fig6 =px.bar(Age_Response,x="Age",y="Response",title="Responce Distribution by Age",color_discrete_sequence=["#465080"])
        fig6.update_layout(height=400)
        fig6.update_layout(xaxis_tickangle=90)      
        fig6.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig6,use_container_width=True)
    # Compaign corelations Heatmap
    Accptance_Campaign =["AcceptedCmp3","AcceptedCmp2","AcceptedCmp1","AcceptedCmp4","AcceptedCmp5"]    
    corr =df[Accptance_Campaign].corr()
    with c7:
        fig7=px.imshow(corr,text_auto=True,title="Compaign Acceptance Heatmap")
        fig7.update_layout(height=400)
        fig7.update_layout(xaxis_tickangle=90)      
        fig7.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig7,use_container_width=True)
    # responce Rate Vs Education 
    Education_ResponseRate =df.groupby("Education")["Response"].mean().reset_index()
    Education_ResponseRate["Response"] =(Education_ResponseRate["Response"] * 100)
    with c8:
        fig8 =px.bar(Education_ResponseRate,x="Education",y="Response",title="Response Rate Vs Education",color="Education")
        fig8.update_layout(height=400)
        fig8.update_layout(xaxis_tickangle=90)      
        fig8.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig8,use_container_width=True)
    # marital status vs response
    MaritalStatus_ResponseRate =df.groupby("Marital_Status")["Response"].mean().reset_index()
    MaritalStatus_ResponseRate["Response"] =(MaritalStatus_ResponseRate["Response"] * 100)
    with c9:
        fig9 =px.bar(MaritalStatus_ResponseRate,x="Marital_Status",y="Response",title="Response Rate Vs Marital_Status",color="Marital_Status")
        fig9.update_layout(height=400)
        fig9.update_layout(xaxis_tickangle=90)      
        fig9.update_layout(xaxis=dict(tickfont=dict(size=14)))
        st.plotly_chart(fig9,use_container_width=True)


# then making the customer values and the Probability Analysics 
if page== "💰 Customer Value & Profitability Analytics":
    # Analyaics the data And find the CLV(Customer Values and the probabititly anaysics)
    df["CLV"] = (df["MntWines"]+df["MntFruits"] +df["MntMeatProducts"]+df["MntFishProducts"]+df["MntSweetProducts"]+df["MntGoldProds"])
    # analysics the income and spending
    Income_Spending=pd.DataFrame({
                "Income":df["Income"],
                "Spending":df["CLV"].sum()
                })
    with st.container(border=True):
        st.markdown("## 💰 Customer Value & Profitability Analytics")
    with st.container(border=True):
        st.subheader("📌 Key Metrics")
    mc1,mc2,mc3,mc4 =st.columns(4)
    mc5,mc6,mc7 =st.columns(3)
    # then making the plot and Visualization the data of the customer Values and the Probability and Analytics Visualizations
    st.markdown("## 💰 Customer Value & Profitability Analytics Visualizations")
    with st.container(border=True):
        p1,p2,p3=st.columns(3)
    with st.container(border=True):
        p4,p5,p6=st.columns(3)
    with st.container(border=True):
        p7,p8,p9=st.columns(3)
    # then making the matrics 
    mc1.metric("💰 Average CLV",f"₹{df["CLV"].mean():,.0f}")
    mc2.metric("🏆 Max CLV",f"₹{df["CLV"].max():,.0f}")
    mc3.metric("📉 Lowest CLV",f"₹{df["CLV"].min():,.0f}")
    mc4.metric("👥 Total Customer",f"{df["ID"].nunique():,.0f}")
    mc5.metric("📊 Median CLV",f"₹{df["CLV"].median():,.0f}")
    mc6.metric("💵 TotaL Customer Values",f"₹{df["CLV"].sum():,.0f}")
    mc7.metric("📈 CLV Std Dev",f"₹{df["CLV"].std():,.0f}")
    # customer Values & Probability Analyaics
    with p1:
        fig1 =px.histogram(df["CLV"],nbins=30,color_discrete_sequence=["purple"],title="Customer Values & Probability Analysics")
        fig1.update_layout(height=400)
        fig1.update_traces(marker_line_color="black",marker_line_width=1)
        fig1.update_layout(xaxis_tickangle=90)      
        fig1.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig1,use_container_width=True)
    # Income VS Spending
    with p2:
        fig2 = px.scatter(Income_Spending,x="Income",y="Spending",title="💰 Income vs Customer Spending",render_mode="webgl",color="Spending")  
        fig2.update_layout(height=400,template="plotly_white")
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar": False})
    # Revenue vs Educations
    with p3:
        fig3 =px.bar(df,x="Education",y="Z_Revenue",title="Education By Revenue",color="Education")
        fig3.update_layout(height=400)
        fig3.update_layout(xaxis_tickangle=90)      
        fig3.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig3,use_container_width=True)
    # Revenue by Marital_Status
    with p4:
        fig4 =px.bar(df,x="Marital_Status",y="Z_Revenue",title="Marital_Status By Revenue",color="Marital_Status")
        fig4.update_layout(height=400)
        fig4.update_layout(xaxis_tickangle=90)      
        fig4.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig4,use_container_width=True)
    # profitabily by Segement
    with p5:
        df["Revenue"] =(df["MntWines"]+df["MntFishProducts"]+df["MntFruits"]+df["MntGoldProds"]+df["MntMeatProducts"]+df["MntSweetProducts"])
        Profitabilty =df.groupby("Education")["Revenue"].sum().reset_index().sort_values("Revenue",ascending=False)
        fig5 =px.bar(Profitabilty,x="Education",y="Revenue",title="Profitabilty By Segement",color="Education")
        fig5.update_layout(height=400)
        fig5.update_layout(xaxis_tickangle=90)      
        fig5.update_layout(xaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig5,use_container_width=True)
        # Top customer
        with p6:
            Top_Customer = df.nlargest(10,"Revenue")
            fig6 =px.bar(Top_Customer,x="ID",y="Revenue",title="Top Customer",color_discrete_sequence=["pink"])
            fig6.update_layout(height=400)
            fig6.update_layout(xaxis_tickangle=90)      
            fig6.update_layout(xaxis=dict(tickfont=dict(size=12)))
            st.plotly_chart(fig6,use_container_width=True)
        # Spending Trends
        with p7:
        # then Analysics the Dt_customer and the Spending
            df["Spending"] =(df["MntWines"]+df["MntFishProducts"]+df["MntFruits"]+df["MntGoldProds"]+df["MntMeatProducts"]+df["MntSweetProducts"])
            df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"],dayfirst=True)                
            Spending_Trend =(
            df.groupby(df["Dt_Customer"].dt.to_period("M"))["Spending"].sum().reset_index()                )
            Spending_Trend["Dt_Customer"] =Spending_Trend["Dt_Customer"].astype(str)
            fig7 =px.line(Spending_Trend,x="Dt_Customer",y="Spending",title="Spending Trend",markers=True)
            fig7.update_layout(height=400,xaxis_title="Month",yaxis_title="Total Spending")
            st.plotly_chart(fig7,use_container_width=True)
        # CLV heatmap
        with p8:
            numeric_cols = ["CLV","Income","Spending","NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth"]
            clv_heatmap = df[numeric_cols].corr()
            fig8 = px.imshow(clv_heatmap,text_auto=".2f",title="🔥 CLV Correlation Heatmap",aspect="auto")
            fig8.update_layout(height=500)
            st.plotly_chart(fig8, use_container_width=True)
        # then Profit Distributions
        with p9:
            df["Revenue"] =(df["MntWines"]+df["MntFishProducts"]+df["MntFruits"]+df["MntGoldProds"]+df["MntMeatProducts"]+df["MntSweetProducts"])
            df["Profit"] =df["Revenue"]-df["Z_CostContact"] 
            print(df["Profit"].sum())
            fig9 =px.histogram(df,nbins=30,x="Profit",title="Profit Distributions")
            fig9.update_layout(height=400,xaxis_title="Profit",yaxis_title="Number of Customer")
            st.plotly_chart(fig9,use_container_width=True)
# then prediction the data 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import r2_score ,mean_absolute_error,mean_squared_error,accuracy_score
df = df.drop_duplicates()
if page=="🤖 Predictive Analytics":
    st.title("Prediction Analysics")
    df["Revenue"] =(df["MntFishProducts"]+df["MntFruits"]+df["MntGoldProds"]+df["MntMeatProducts"]+df["MntSweetProducts"]+df["MntWines"])
    Feactures =[
        "Income","Kidhome","Teenhome","Teenhome","NumDealsPurchases","NumWebPurchases","NumCatalogPurchases","NumCatalogPurchases","NumStorePurchases","NumWebVisitsMonth","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","AcceptedCmp1","AcceptedCmp2"]
        # then given the feactures
    X=df[Feactures]
    y=df["Revenue"]
    # then test train and split the data
    X_train,X_test,y_train,y_test =train_test_split(X,y,test_size=0.2,random_state=42)

    # then model import 
    model_Rf =RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=2,
        min_samples_split=5,
        random_state=42
        )
    model_Rf.fit(X_train,y_train)
    # model_predict
    y_prew_rf =model_Rf.predict(X_test)
    # then check the accuracy of the model
    train_r2= model_Rf.score(X_train,y_train)
    test_r2= model_Rf.score(X_test,y_test)
    print("Train Score",train_r2)
    print("Test Score",test_r2)
    # then check the MSE and MAE
    print("Mean Squared Error",mean_squared_error(y_test,y_prew_rf))
    print("Mean Absolute Error",mean_absolute_error(y_test,y_prew_rf))

    # then check the comparisions
    comparision = pd.DataFrame({
        "Actual": y_test.values,
        "Predictions":y_prew_rf
    })
    print(comparision.head(10))
    # then Visualization the Revenue
    with st.container(border=True):
        pr1,pr2 =st.columns(2)
    with st.container(border=True):
        pr3,pr4 =st.columns(2)
        with pr1:
            fig1 =go.Figure()
            fig1.add_trace(
                go.Scatter(x=comparision.index,y=comparision["Actual"],mode="markers",name="Actual_Revenue",marker=dict(color="red"))
                )
            fig1.add_trace(
                go.Scatter(x=comparision.index,y=comparision["Predictions"],mode="markers",name="Prediction_Revenue",marker=dict(color="blue")))
            fig1.add_shape(
                type="line",
                x0=comparision["Actual"].min(),
                y0=comparision["Actual"].min(),
                x1=comparision["Actual"].max(),
                y1=comparision["Actual"].max()            
            )
            fig1.update_layout(height=400,
                               title={"text":"Revenue Predictions into Future",
                                    "x":0.5,
                                    "xanchor":"center"},xaxis_title="Future Period",yaxis_title="Predicted Revenue")
            st.plotly_chart(fig1,use_container_width=True)
    Product_Columns = ["MntWines", "MntFruits", "MntMeatProducts",
                "MntFishProducts", "MntSweetProducts","MntGoldProds"]
    # then predict the profit
    df["Profit"] =df["Revenue"]-df["Z_CostContact"]
    Feacture_profit =["Revenue","Z_CostContact"]
    # then predict the profit
    from sklearn.linear_model import LinearRegression
        # import the features
    X=df[Feacture_profit]
    y=df["Profit"]
    # import the train test and split
    X_trainpr,X_testpr,y_trainpr,y_testpr =train_test_split(X,y,test_size=0.2,random_state=42)
    # then import the model Profit
    Model_Pro =LinearRegression()
    Model_Pro.fit(X_trainpr,y_trainpr)
    # then prediction the Profit Model
    Y_pred_Pro =Model_Pro.predict(X_testpr)
    # then check the Score or the Accuracy
    Train_Pro =Model_Pro.score(X_trainpr,y_trainpr)
    Test_Pro =Model_Pro.score(X_testpr,y_testpr)
    # then visualization the Profit form the data
    Profit_Comparision =pd.DataFrame({
        "Actual Profit":y_testpr.values,
        "Predicted Profit":Y_pred_Pro
    })    
    with pr2:
        fig2=go.Figure() 
        fig2.add_trace(
                go.Scatter(x=Profit_Comparision.index,y=Profit_Comparision["Actual Profit"],name="Actual Profit",mode="markers",marker=dict(color="green"))
            )
        fig2.add_trace(
                go.Scatter(x=Profit_Comparision.index,y=Profit_Comparision["Predicted Profit"],name="Predicted Profit",mode="markers",marker=dict(color="purple"))
            )
        fig2.update_layout(height=400,
                               title={"text":"Profit Predictions into Future",
                                    "x":0.5,
                                    "xanchor":"center"},xaxis_title="Future Period",yaxis_title="Predicted Profit")            
        st.plotly_chart(fig2,use_container_width=True)
    # then predict the High Saling Product
    # import the sklearn Model for the Predict the high saling Product 
    product_cols = ["MntWines", "MntFruits", "MntMeatProducts",
                "MntFishProducts", "MntSweetProducts","MntGoldProds"]
    X=df.drop(columns=product_cols,errors="ignore")
    X = pd.get_dummies(X, drop_first=True)
    Product_Sales ={}
    for Product in product_cols:
        y=df[Product]

        # test train and split the data
        X_train_pro,X_test_pro,y_train_pro,y_test_pro =train_test_split(X,y,test_size=0.2,random_state=42)
        # model train
        Model_Product =RandomForestRegressor(n_estimators=100,random_state=42)
        Model_Product.fit(X_train_pro,y_train_pro)
        # predict the model
        Predicted_Product =Model_Product.predict(X)
        # then stored the values in product sales
        Product_Sales[Product] =Predicted_Product.mean()

        # then mKing the dataframe of the product 
    Predicted_df=pd.DataFrame({
            "Product":Product_Sales.keys(),
            "Predicted_Sales":Product_Sales.values()
    })
        # then check the high saling product 
    Hightest_product =Predicted_df.loc[Predicted_df["Predicted_Sales"].idxmax()]
    st.success(f"🏆 Future Highest Selling Product: "
                   f"{Hightest_product['Product']}"
                   f"(Predicted_Sales: {Hightest_product["Predicted_Sales"]:.2f})")
        # find the lowest sales predict
    Lowest_Product =Predicted_df.loc[Predicted_df["Predicted_Sales"].idxmin()]
    st.error(f"📉 Future Lowest Selling Product::"
                 f"{Lowest_Product['Product']}"
                 f"(Predicted_Sales: {Lowest_Product["Predicted_Sales"]:.2f})")
        # prediction the Product High Saling and Lowest Saling Product
    with pr3:
        fig3 =px.bar(Predicted_df.sort_values("Predicted_Sales",ascending=False),
                    x="Product",y="Predicted_Sales",color="Predicted_Sales",title="Future Predicted Product Sales")
        fig3.update_layout(height=400,xaxis_title="Product",yaxis_title="Predicted_Sales")
        st.plotly_chart(fig3,use_container_width=True)
