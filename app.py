import streamlit as st
import pandas as pd
import cleaning
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
cleaning.df['year'] = cleaning.df['date'].dt.year
cleaning.df['month'] = cleaning.df['date'].dt.month


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the invester
    last5_df = cleaning.df[cleaning.df['investors'].str.contains('investor')].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investor
        big_series = cleaning.df[cleaning.df['investors'].str.contains(investor)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('biggest investment')
        #st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)
    with col2:
        verical_series = cleaning.df[cleaning.df['investors'].str.contains(investor)].groupby('vertical')[
            'amount'].sum()
        st.subheader('sectors invested in')
        #st.dataframe(verical_series)
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series, labels=verical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)
    col3, col4 = st.columns(2)
    with col3:
        round_series = cleaning.df[cleaning.df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('rounds investment in ')
        #st.dataframe(round_series)
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        city_series = cleaning.df[cleaning.df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('cities invested in ')
        #st.dataframe(city_series)
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index)

        st.pyplot(fig3)


    year_series = cleaning.df[cleaning.df['investors'].str.contains(investor)].groupby('year')[
        'amount'].sum()
    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)

    st.pyplot(fig4)


def load_overall_analysis():
  st.title('Overall Analysis')
  # total invested amount
  total = round(cleaning.df['amount'].sum())
  # total amount infused in a startup
  max_funding = cleaning.df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
  # avg funding in startups
  avg_funding = cleaning.df.groupby('startup')['amount'].sum().mean()
  # total funded startups
  num_startup = cleaning.df['startup'].nunique()
  #
  cleaning.df['month'] = cleaning.df['date'].dt.month
  col1,col2,col3,col4 = st.columns(4)
  with col1:
      st.metric('Total', str(total) + "Cr")
  with col2:
      st.metric('Max', str(max_funding) + "Cr")
  with col3:
      st.metric('Avg', str(round(avg_funding)) + "Cr")
  with col4:
      st.metric('Funded startups', num_startup )

  st.header('MoM graph')
  selected_option = st.selectbox('Select Type',['Total','Count'])
  if selected_option == 'Total':
   temp_df = cleaning.df.groupby(['year','month'])['amount'].sum().reset_index()
  else:
      temp_df = cleaning.df.groupby(['year','month'])['amount'].count().reset_index()
  temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

  fig6, ax6 = plt.subplots()
  ax6.plot(temp_df['x_axis'], temp_df['amount'])

  st.pyplot(fig6)



st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select startup', sorted(cleaning.df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    selected_investor = st.sidebar.selectbox('Select Investor',
                                             sorted(set(cleaning.df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        st.title('Investor Analysis')
        load_investor_details(selected_investor)

# kaade se data ko preprocess karo and then clean and then use in analysis
