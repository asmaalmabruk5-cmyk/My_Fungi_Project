import streamlit as st
import pandas as pd
import os

# إعدادات صفحة التطبيق
st.set_page_config(
    page_title="المستودع الرقمي لفطريات الجبل الأخضر",
    page_icon="🍄",
    layout="wide"
)

st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")
st.markdown("منصة توثيق وإدارة العينات الحقلية والمجهرية للفطريات الكبيرة.")

# دالة قراءة ملف الـ CSV مع دعم تجربة ترميزات متعددة لتجنب مشاكل الحروف العربية
@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        for enc in ['utf-8-sig', 'cp1256', 'utf-8', 'latin1']:
            try:
                df = pd.read_csv(csv_file, encoding=enc)
                return df
            except Exception:
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
        
    # عرض جدول البيانات
    st.dataframe(filtered_df, use_container_width=True)
    st.info(f"إجمالي العينات المعروضة: {len(filtered_df)}")
    
    # قسم المعرض البصري والصور المرتبطة
    st.markdown("---")
    st.subheader("🖼️ المعرض البصري للعينات (صور الحقل والأبواغ)")
    
    # التعرف على اسم عمود المعرف ديناميكياً
    id_col = None
    for col in df.columns:
        if 'specimen' in col.lower() or 'id' in col.lower():
            id_col = col
            break
            
    if id_col and not df.empty:
        selected_specimen = st.selectbox("اختر رقم العينة لعرض تفاصيلها وصورها المجهرية:", df[id_col].tolist())
        
        if selected_specimen:
            matched_row = df[df[id_col] == selected_specimen]
            st.write("تفاصيل العينة المحددة:")
            st.dataframe(matched_row, use_container_width=True)
            
            # البحث عن الصور المطابقة في المجلد
            files_in_dir = os.listdir(".")
            image_files = [f for f in files_in_dir if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # مطابقة أجزاء اسم العينة مع أسماء الصور
            matched_images = [img for img in image_files if str(selected_specimen).lower() in img.lower()]
            
            if matched_images:
                st.write("الصور المرتبطة بهذه العينة:")
                cols = st.columns(len(matched_images) if len(matched_images) <= 3 else 3)
                for idx, img_name in enumerate(matched_images):
                    with cols[idx % len(cols)]:
                        st.image(img_name, caption=img_name, use_container_width=True)
            else:
                st.warning("لا توجد صور مطابقة لهذا المعرف في المجلد حالياً.")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المجلد الرئيسي. تأكدي من صحة اسم الملف ورفعه.")
