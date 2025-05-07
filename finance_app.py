import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# File to store data
DATA_FILE = "finance_data.csv"

# Initialize file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type"])
    df.to_csv(DATA_FILE, index=False)

# Load data
df = pd.read_csv(DATA_FILE)

st.title("💰 Personal Finance Dashboard")

# Add new transaction
st.header("➕ Add a New Transaction")

with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    date = col1.date_input("Date", datetime.today())
    trans_type = col2.selectbox("Type", ["Expense", "Income"])
    category = st.selectbox("Category", ["Food", "Rent", "Salary", "Transport", "Entertainment", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted:
        new_data = pd.DataFrame([[date, category, description, amount, trans_type]],
                                columns=["Date", "Category", "Description", "Amount", "Type"])
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("Transaction added successfully!")

# Show transaction history
st.header("📄 Transaction History")
df = pd.read_csv(DATA_FILE)
st.dataframe(df)

# Summary
st.header("📊 Summary & Charts")
if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"])
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${income:.2f}")
    col2.metric("Total Expenses", f"${expenses:.2f}")
    col3.metric("Balance", f"${balance:.2f}")

    # Plot by category
    st.subheader("Expenses by Category")
    exp_by_cat = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
    st.bar_chart(exp_by_cat)

    st.subheader("Income vs Expense Over Time")
    df["Date"] = pd.to_datetime(df["Date"])
    time_summary = df.groupby(["Date", "Type"])["Amount"].sum().unstack().fillna(0)
    st.line_chart(time_summary)
else:
    st.info("No data yet. Add a transaction above to get started.")
