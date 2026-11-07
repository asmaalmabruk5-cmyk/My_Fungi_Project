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
            
            # جمع كل الصور المتاحة في المجلد الرئيسي أو مجلد images
            all_image_paths = []
            
            # البحث في المجلد الرئيسي
            if os.path.exists("."):
                for f in os.listdir("."):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        all_image_paths.append(f)
            
            # البحث داخل مجلد images إذا كان موجوداً
            images_dir = "images"
            if os.path.exists(images_dir) and os.path.isdir(images_dir):
                for f in os.listdir(images_dir):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        all_image_paths.append(os.path.join(images_dir, f))
            
            # تصفية الصور التي تتطابق مع معرف العينة المحدد
            matched_images = [img for img in all_image_paths if str(selected_specimen).lower() in img.lower()]
            
            if matched_images:
                st.write("الصور المرتبطة بهذه العينة:")
                cols = st.columns(len(matched_images) if len(matched_images) <= 3 else 3)
                for idx, img_path in enumerate(matched_images):
                    with cols[idx % len(cols)]:
                        st.image(img_path, caption=os.path.basename(img_path), use_container_width=True)
            else:
                st.warning(f"⚠️ تنبيه: لم يتم العثور على صور مطابقة للمعرف ({selected_specimen}) في المجلدات. تأكدي أن اسم ملف الصورة يحتوي على رقم المعرف تماماً.")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv` في المجلد الرئيسي. تأكدي من صحة اسم الملف ورفعه.")
