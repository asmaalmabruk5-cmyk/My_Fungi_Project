import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة وواجهة العرض
st.set_page_config(page_title="المستودع الرقمي لفطريات الجبل الأخضر", page_icon="🍄", layout="wide")

st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")
st.markdown("منصة توثيق وإدارة العينات الحقلية والمجهرية للفطريات الكبيرة.")

# دالة قراءة ملف الـ CSV مع دعم الترميز العربي المتعدد
@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        for enc in ['utf-8-sig', 'utf-8', 'cp1256', 'latin1']:
            try:
                return pd.read_csv(csv_file, encoding=enc)
            except:
                continue
    return None

df = load_data()

if df is not None:
    st.success("تم تحميل قاعدة البيانات بنجاح! 📊")
    
    # مربع البحث السريع
    search_term = st.text_input("🔍 ابحثي عن اسم الفطر أو رقم العينة (Specimen_ID):")
    
    if search_term:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df
        
    # عرض الجدول كاملاً ومنسقاً
    st.dataframe(filtered_df, use_container_width=True)
    st.info(f"إجمالي العينات المعروضة: {len(filtered_df)}")
    
    # قسم استعراض الصور المرتكز على العينات
    st.markdown("---")
    st.subheader("🖼️ المعرض البصري للعينات (صور الحقل والابواغ)")
    
    if "Specimens_ID" in df.columns or "Specimen_ID" in df.columns:
        id_col = "Specimen_ID" if "Specimen_ID" in df.columns else "Specimens_ID"
        selected_specimen = st.selectbox("اختر رقم العينة لعرض صورها المجهرية والحقلية:", df[id_col].tolist())
        
        if selected_specimen:
            # البحث عن بادئة اسم الصورة المرتبطة بالعينة
            matched_row = df[df[id_col] == selected_specimen]
            st.write(matched_row)
            
            # محاولة البحث عن الصور المطابقة في المجلد
            files_in_dir = os.listdir(".")
            # استخراج اسم ملف مصغر أو البحث بالصور المتاحة
            col1, col2, col3 = st.columns(3)
            
            # عرض الصور التي تتطابق مع الاسم
            found_images = [f for f in files_in_dir if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # عرض توضيحي لطريقة جلب الصور
            st.write("الصور المتاحة في المستودع لهذه العينة:")
            for img in found_images:
                if any(part.lower() in img.lower() for part in str(selected_specimen).split("-")):
                    st.image(img, caption=img, width=300)

else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المستودع. تأقدي من رفعه في المجلد الرئيسي.")
