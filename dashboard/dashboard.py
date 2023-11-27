import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_daily_rent(df):
    daily_rent_df = df.groupby(by="datetime").agg(
        {"total_count": "sum"}).reset_index()
    return daily_rent_df


main_df = pd.read_csv("./main_data.csv")
main_df.sort_values(by="datetime", inplace=True)
main_df.reset_index(inplace=True)

main_df['datetime'] = pd.to_datetime(main_df['datetime'])

min_date = main_df["datetime"].min()
max_date = main_df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = main_df[(main_df["datetime"] >= str(start_date)) &
                  (main_df["datetime"] <= str(end_date))]

daily_rent_df = create_daily_rent(main_df)
corr = main_df.corr(numeric_only=True)

st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Daily Rental')

col1, col2, col3 = st.columns(3)

with col1:
    total_rent = main_df.total_count.sum()
    st.metric("Total Rent", value=total_rent)

with col2:
    total_casual_rent = main_df.casual.sum()
    st.metric("Total Casual Rent", value=total_casual_rent)

with col2:
    total_registered_rent = main_df.registered.sum()
    st.metric("Total Registered Rent", value=total_registered_rent)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["datetime"],
    daily_rent_df["total_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader(
    "Faktor-faktor apa yang berpotensi mempengaruhi volume peminjaman sepeda")

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
plt.subplots_adjust(hspace=0.5)

axes = axes.flatten()

sns.barplot(data=main_df, x='season', y='total_count', ax=axes[0])
axes[0].set_title('Variation of total count by season')

sns.lineplot(data=main_df, x='month', y='total_count', ax=axes[1])
axes[1].set_title('Variation of total count by month')

sns.barplot(data=main_df, x='holiday', y='total_count', ax=axes[2])
axes[2].set_title('Variation of total count on holidays')

sns.barplot(data=main_df, x='weekday', y='total_count', ax=axes[3])
axes[3].set_title('Variation of total count on weekdays')

sns.lineplot(data=main_df, x='hour', y='total_count', ax=axes[4])
axes[4].set_title('Variation of total count by hour')

sns.barplot(data=main_df, x='weather_condition', y='total_count', ax=axes[5])
axes[5].set_title('Variation of total count by weather condition')

plt.tight_layout()

st.pyplot(fig)

fig, axes = plt.subplots(figsize=(16, 8))

sns.heatmap(corr, annot=True, annot_kws={'size': 10})
axes.set_title('Correlation Matrix')

st.pyplot(fig)

st.subheader(
    "Perbedaan karakteristik antara pengguna kasual(casual) dan pengguna terdaftar(registered)")

fig, ax = plt.subplots(figsize=(16, 8))
ax = sns.lineplot(x='weekday', y='value', hue='variable', data=pd.melt(
    main_df, id_vars=['weekday'], value_vars=['registered', 'casual']), marker='o')
ax.set_title('Variation of Average Weekly Count of Registered and Casual Users')
ax.set_xlabel('Weekday')
ax.set_ylabel('Count')
ax.legend(title='User Type')
sns.set(style="whitegrid")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax = sns.pointplot(x='hour', y='value', hue='variable', data=pd.melt(main_df, id_vars=['hour'], value_vars=[
                   'registered', 'casual']), palette={'registered': '#4c72b0', 'casual': '#dd8452'})
ax.set_title('Variation of Average Hour Count of Registered and Casual Users')
ax.set_xlabel('Hour')
ax.set_ylabel('Count')
ax.legend(title='User Type')
sns.set(style="whitegrid")
st.pyplot(fig)
