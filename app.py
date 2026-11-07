import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="المستودع الرقمي لفطريات الجبل الأخضر",
    page_icon="🍄",
    layout="wide"
)

st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")
st.markdown("منصة توثيق وإدارة العينات الحقلية والمجهرية للفطريات الكبيرة.")

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
    
    search_term = st.text_input("🔍 ابحثي عن اسم الفطر أو رقم العينة (Specimen_ID):")
    
    if search_term:
        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df
        
    st.dataframe(filtered_df, use_container_width=True)
    st.info(f"إجمالي العينات المعروضة: {len(filtered_df)}")
    
    st.markdown("---")
    st.subheader("🖼️ المعرض البصري للعينات (صور الحقل والأبواغ)")
    
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
            image_cols = [c for c in df.columns if 'image' in c.lower() or 'photo' in c.lower() or 'img' in c.lower()]
            displayed = False
            
            if image_cols:
                cols = st.columns(len(image_cols) if len(image_cols) <= 3 else 3)
                for i, col_name in enumerate(image_cols):
                    img_name = str(matched_row[col_name].values[0]).strip()
                    if img_name and img_name.lower() not in ['nan', 'none', '']:
                        # التحقق من وجود الصورة في المجلد الرئيسي أو مجلد images
                        img_path = None
                        if os.path.exists(img_name):
                            img_path = img_name
                        elif os.path.exists(os.path.join("images", img_name)):
                            img_path = os.path.join("images", img_name)
                            
                        if img_path:
                            with cols[i % len(cols)]:
                                st.image(img_path, caption=f"{col_name}: {img_name}", use_container_width=True)
                                displayed = True
                                
            if not displayed:
                st.info("💡 ملاحظة: لعرض الصور، تأكدي من رفع ملفات الصور إلى المستودع وأن أسماءها مسجلة في أعمدة الصور بملف الـ CSV أو تحتوي على رقم المعرف.")
else:
    st.error("لم يتم العثور على ملف البيانات `macrofungi_database_template.csv`.")
