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

# دالة قراءة ملف الـ CSV
@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        try:
            return pd.read_csv(csv_file)
        except Exception:
            return None
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
            
            # استخراج أسماء الصور مباشرة من أعمدة جدول الـ CSV (البحث عن أعمدة تحتوي على image أو photo)
            image_columns = [col for col in df.columns if 'image' in col.lower() or 'photo' in col.lower() or 'img' in col.lower()]
            
            displayed_any_image = False
            
            if image_columns:
                cols = st.columns(len(image_columns) if len(image_columns) <= 3 else 3)
                for i, col_name in enumerate(image_columns):
                    img_filename = str(matched_row[col_name].values[0]).strip()
                    
                    if img_filename and img_filename.lower() != 'nan' and img_filename.lower() != 'none':
                        # البحث عن الصورة في المجلد الرئيسي أو داخل مجلد images
                        img_path = None
                        if os.path.exists(img_filename):
                            img_path = img_filename
                        elif os.path.exists(os.path.join("images", img_filename)):
                            img_path = os.path.join("images", img_filename)
                            
                        if img_path:
                            with cols[i % len(cols)]:
                                st.image(img_path, caption=f"{col_name}: {img_filename}", use_container_width=True)
                                displayed_any_image = True
                                
            if not displayed_any_image:
                st.warning("⚠️ تنبيه: لم يتم تسجيل أسماء الصور بدقة في أعمدة جدول الـ CSV لهذه العينة، أو أن ملفات الصور غير موجودة في المجلد.")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المجلد الرئيسي. تأكدي من صحة اسم الملف ورفعه.")
