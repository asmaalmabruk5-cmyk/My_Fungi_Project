import streamlit as st
import pandas as pd
import os

st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")

# دالة لقراءة ملف الـ CSV تلقائياً
@st.cache_data
def load_data():
    for file in os.listdir("."):
        if file.endswith(".csv"):
            return pd.read_csv(file)
    return None

df = load_data()

if df is not None:
    st.success("تم تحميل قاعدة البيانات بنجاح! 📊")
    st.dataframe(df) # لعرض جدول البيانات كاملاً
else:
    st.warning("الرجاء التأكد من رفع ملف الـ CSV في المستودع الرئيسي.")
