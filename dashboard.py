import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load dataset
dongsi_df = pd.read_csv("./dashboard/dongsi.csv")

datetime_columns = ["date"]
dongsi_df.sort_values(by="date", inplace=True)
dongsi_df.reset_index(inplace=True)

for column in datetime_columns:
    dongsi_df[column] = pd.to_datetime(dongsi_df[column])

# Dashboard Title
st.title('DONGSI STATION AIR QUALITY ANALYSIS')
st.subheader('This dashboard presents the results of air quality analysis at Dongsin Station from 2013 to 2017. This analysis focuses on the parameters PM2.5, PM10 and temperature.')



# dongsin_df["date"] = pd.to_datetime(dongsin_df["date"])
minimum = dongsi_df["date"].min()
maximum = dongsi_df["date"].max()

with st.sidebar:
    st.image("./data/img-example.jpg")
    st.text('Hello! this is filter')
    start_date, end_date = st.date_input(
        label='Date',
        min_value= minimum,
        max_value= maximum,
        value=[minimum, maximum]
    )

main_df = dongsi_df[(dongsi_df["date"] >= str(start_date)) & 
                (dongsi_df["date"] <= str(end_date))]

#########
# plot Air Polution PM2.5
st.header('Air Pollution Dongsin :sparkles:')
st.subheader("PM2.5 Pollution")

fig, ax = plt.subplots(figsize=(16, 8))
groupByMonth = main_df.groupby("month").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByMonth.index, groupByMonth["PM2.5"], label="PM2.5")
plt.xlabel("Month")
plt.ylabel("µg/m³(microgram/m3)")
plt.legend()
st.pyplot(fig)

##########
# Plot Air Polution PM10
st.subheader("PM10 Polution")
groupByMonth = main_df.groupby("month").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByMonth.index, groupByMonth["PM10"], label="PM10")
plt.xlabel("Month")
plt.ylabel("µg/m³(microgram/m3)")
plt.legend()
st.pyplot(fig)

##########
# Plot Air Quality Temperature Parameter
st.subheader("Temperature")
groupByYear = main_df.groupby("year").mean(numeric_only=True)


fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["TEMP"], label="TEMP")
plt.xlabel("Year")
plt.ylabel("°C")
plt.legend()
st.pyplot(fig)

############
#Plot Air Quality Based on Particle Diameter (month)
st.subheader("Air Quality Based on Particle Diameter (month)")
groupByMonths = main_df.groupby("month").mean(numeric_only=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#linechart
ax1.plot(groupByMonth.index, groupByMonth["PM2.5"], linestyle='--', marker='o', label="PM2.5")
ax1.plot(groupByMonth.index, groupByMonth["PM10"], linestyle='--', marker='o', label="PM10")
ax1.set_xlabel("Months")
ax1.set_xticklabels(month_labels)  
ax1.set_ylabel("µg/m³ (microgram/m3)")
ax1.set_title("PM2.5 & PM10 Line Chart")
ax1.legend()

#barchart
bar_width = 0.35  
index = groupByMonth.index

ax2.bar(index - bar_width/2, groupByMonth["PM2.5"], bar_width, color='skyblue', label="PM2.5")
ax2.bar(index + bar_width/2, groupByMonth["PM10"], bar_width, color='lightgreen', label="PM10")
ax2.set_xticks(index)  
ax2.set_xticklabels(month_labels)  
ax2.set_xlabel("Months")
ax2.set_ylabel("µg/m³ (microgram/m3)")
ax2.set_title("PM2.5 & PM10 Bar Chart")
ax2.legend()

plt.tight_layout()

st.pyplot(fig)

############
#Plot Correlation Matrix Between PM2.5, PM10, Temperature
st.subheader("Correlation Matrix Between PM2.5, PM10, Temperature")
correlation_matrix = dongsi_df[['PM2.5', 'PM10', 'TEMP']].corr()

# show heatmap
fig = plt.figure(figsize=(13, 9))
sns.heatmap(correlation_matrix, cmap='Oranges', annot=True)
plt.title("Correlation between PM2.5, PM10, TEMP")
st.pyplot(fig)

############
#Plot Comparison of PM2.5 Concentrations each year
st.subheader("Comparison of PM2.5 Concentrations each year")
years = dongsi_df.groupby("year").mean(numeric_only=True)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
#subplot data linechart
ax1.plot(years.index, years["PM2.5"], linestyle='--', marker='o', label="PM2.5")
ax1.set_xlabel("Year")
ax1.set_ylabel("µg/m³ (microgram/m3)")
ax1.set_title("PM2.5 Line Chart")
ax1.legend()

#subplot data barchart
ax2.bar(years.index, years["PM2.5"], color='skyblue', label="PM2.5")
ax2.set_xlabel("Year")
ax2.set_ylabel("µg/m³ (microgram/m3)")
ax2.set_title("PM2.5 Bar Chart")
ax2.legend()

plt.tight_layout()
st.pyplot(fig)

########
#conclusion
st.subheader("Conclusion")
st.write(""" - Conclusion question 1
  
    1. PM10 consistently has a higher concentration compared to PM2.5 throughout the year, indicating that larger particles are more prevalent.
    2. The lowest point for both PM2.5 and PM10 occurs in the 8th month, which suggests better air quality during this period.
    3. However, pollution levels increase significantly around the 3rd and 10th months, indicating worse air quality during these months, especially when PM10 reaches its peak.

- Conclusion question 2
    1. Pollutan concentration change as temperature changes
    2. there is positive and negative correlation

- Conclusion question 3
    
    The highest concentration of PM2.5 occurred in 2017 which was arround more than 100 µg/m³
         """)
st.caption('Copyright © Dicoding 2023-Fitri Fitriah-m123b4kx1537@bangkit.academy')