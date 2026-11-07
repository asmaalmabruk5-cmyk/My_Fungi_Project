import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="المستودع الرقمي لفطريات الجبل الأخضر", page_icon="🍄", layout="wide")

st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")
st.write("مرحباً بكِ في منصة توثيق وإدارة الفطريات.")

# دالة قراءة ملف الـ CSV بكل موثوقية
@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        try:
            return pd.read_csv(csv_file, encoding='utf-8')
        except:
            return pd.read_csv(csv_file, encoding='latin1')
    return None

df = load_data()

if df is not None:
    st.success("تم تحميل قاعدة البيانات بنجاح! 📊")
    
    # عرض خيارات التصفح والبحث
    search_term = st.text_input("🔍 ابحثي عن اسم الفطر أو العينة:")
    if search_term:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
        
    st.info(f"إجمالي العينات المسجلة في القاعدة: {len(df)}")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المستودع الرئيسي. تأكدي من صحة اسم الملف.")
