import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ----------- Page Setup --------------
st.set_page_config(page_title="My Store", page_icon=":bar_chart:", layout="wide")


# ----------- Page Title --------------
st.title("Bank Analysis Web Application")
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)
st.warning('The data changes based on the filters applied!', icon="⚠️")

# ----------- data Sources ------------
df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")
st.success('The connection to the Bank API was successful', icon="✅")


# -------------- Sidebar for the Web App --------------

with st.sidebar:
    # ----------- File Uploader for Data Source ----------------
    st.header(":file_folder: Upload a file")
    with st.sidebar:
        fl = st.file_uploader("", type=(["csv","xlsx","xls"]))
        if fl is not None:
            if fl.type != "text/csv" | fl.type != "xlsx" | fl.type != "xls":
                st.error('The selected file is not supported', icon="🚨")
            else:
                filename = fl.name
                st.write(filename)
                df = pd.read_csv(filename, encoding="ISO-8859-1")
        else:
            df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

    # ----------- Filters header ----------
    st.write("---")
    st.sidebar.header("Choose your filters: ")
    job = st.selectbox("Select Job Title", pd.unique(df["job"]))
    st.write("##")

    min = df["balance"].min()
    max = df['balance'].max()

    min_money, max_money = st.select_slider(
    'Select a monetary range for customer balances',
    options=sorted(df["balance"].unique()),
    value=(min, max))

    st.write("---")
    st.sidebar.header("Page Settings: ")
    color = st.color_picker('Background Color', '#00f900')
    st.write('The current color is', color)

    st.markdown(
    """
    <style>
    .reportview-container {
        background: {color};
    }
   .sidebar .sidebar-content {
        background: {color};
    }
    </style>
    """,
    unsafe_allow_html=True
    )


# ------------ Table Raw Data ---------------
st.subheader("Customers list - Raw data")
st.write(df)

# ---------- filters -------------
job_filter = df[df["job"] == job]
job_and_balance_range = df[(df["balance"] >= min_money) & (df["balance"] < max_money) & (df["job"] == job)]

# ------------- Time Series Chart --------------

st.write("##")
st.subheader("Customers filtered by age based on Job Title")
age_count = pd.value_counts(job_filter["age"])
line = pd.DataFrame(age_count, columns=["Age", "count"])
st.line_chart(line)

st.info('You can download the data from the line series with the current filters using the tools below', icon="🔥")
with st.expander("Tabular form of: Customers filtered by age based on Job Title"):
    st.write(job_filter.style.background_gradient(cmap="Blues"))
    csv = job_filter.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data= csv, file_name= "customersByAge_basedOn_jobTitle.csv", mime= "text/csv", help= 'Click here to download the data as a CSV file')

# ------------- Time Series Chart : Min & Max Balance and Job Title --------------

st.write("##")
st.subheader("Customers filtered by Account Balance based on Job Title")
balances = pd.value_counts(job_and_balance_range["balance"])
line2 = pd.DataFrame(balances, columns=["count", "Job"])
st.line_chart(line2)

st.info('You can download the data from the line series with the current filters using the tools below', icon="🔥")
with st.expander("Tabular form of: Customers filtered by Account Balance based on Job Title"):
    st.write(job_and_balance_range.style.background_gradient(cmap="Blues"))
    csv = job_and_balance_range.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data= csv, file_name= "customersBalance_basedOn_jobTitle.csv", mime= "text/csv", help= 'Click here to download the data as a CSV file')

# --------------- Bar Chart --------------
st.write("##")
st.subheader("Customers filtered by Job Title")
job_post = pd.value_counts(df["job"])
bar = pd.DataFrame(job_post, columns=["Job", "count"])
st.bar_chart(bar)

# --------------- Map --------------
# st.write("---")
# st.subheader("You can visit our offices anytime on addresses marked below")

# data = pd.DataFrame({
#     'latitude': [37.7749, 34.0522, 40.7128],
#     'longitude': [-122.4194, -118.2437, -74.0060]
# })
 
## Create a map with the data
# st.map(data)

# ------------ Footer Section -------------
st.write("##")
st.write("---")
tutorials_col, contact_form_col = st.columns((3,2))

with tutorials_col:
    st.subheader("You can use the following resources to learn how to build interactive Web Applications like this one with [Streamlit](https://streamlit.io/)")
    st.write("1. [Real-Time Live Finance/Marketing/Data Science Dashboard in Python](https://www.youtube.com/watch?v=OkodDZxsN1I)")
    st.write("2. [Streamlit Tutorial - 3 for beginners | streamlit st.line_chart , st.bar_chart , st.pyplot , st.map](https://www.youtube.com/watch?v=HB0OlnX5K_U)")
    st.write("3. [Streamlit Tutorial - 4, input widget streamlit button, download_button , checkbox , radio, selectbox](https://www.youtube.com/watch?v=K7vu6Yu6P9c)")
    st.write("4. [Streamlit Documentation](https://streamlit.io/library/components/create)")

with contact_form_col:
    st.subheader("Get In Touch With Us")
    with st.form("contact-form", clear_on_submit=True):
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        body = st.text_area("Message")
        newsletter = st.checkbox("Subscribe me to your newsletter")
        submit = st.form_submit_button("Submit")