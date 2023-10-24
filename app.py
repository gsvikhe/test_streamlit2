
import streamlit as st
from calculator import Calculator

st.title("Work Hours Calculator")



weekly_limit = st.slider("Weekly Limit", 48, 54, step=1)
daily_limit = st.slider("Daily Limit", 9, 13, step=1)

if st.button("Calculate"):
    calculator = Calculator()
    calculator.weekly_regular_limit = weekly_limit
    calculator.daily_spread_over_limit = daily_limit
    data = calculator.calculate()
    st.write(data)  # Display data
