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

# دالة قراءة ملف الـ CSV بالترميز الصحيح لضمان ظهور النصوص العربية بوضوح تام
@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        for enc in ['utf-8-sig', 'cp1256', 'utf-8']:
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
            
            # البحث عن أعمدة الصور في جدول الـ CSV
            image_cols = [c for c in df.columns if any(term in c.lower() for term in ['image', 'photo', 'img', 'cap', 'spore'])]
            
            displayed_images = []
            for col_name in image_cols:
                val = str(matched_row[col_name].values[0]).strip()
                if val and val.lower() not in ['nan', 'none', 'n/a', '']:
                    if val.lower().endswith(('.jpg', '.jpeg', '.png')):
                        displayed_images.append((col_name, val))
            
            if displayed_images:
                st.write("الصور المرتبطة بهذه العينة:")
                cols = st.columns(len(displayed_images) if len(displayed_images) <= 3 else 3)
                for idx, (col_type, img_filename) in enumerate(displayed_images):
                    img_path = None
                    if os.path.exists(img_filename):
                        img_path = img_filename
                    elif os.path.exists(os.path.join("images", img_filename)):
                        img_path = os.path.join("images", img_filename)
                        
                    if img_path:
                        with cols[idx % len(cols)]:
                            st.image(img_path, caption=f"نوع الصورة: {col_type}", use_container_width=True)
                    else:
                        cols[idx % len(cols)].warning(f"⚠️ الصورة `{img_filename}` مسجلة في الجدول لكن تأكدي من رفعها لمستودع قيت هاب.")
            else:
                st.warning("⚠️ لا توجد أسماء صور مسجلة في أعمدة جدول البيانات لهذه العينة.")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المستودع.")
