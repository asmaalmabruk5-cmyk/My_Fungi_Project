import os
import pandas as pd
import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="المستودع الرقمي لفطريات الجبل الأخضر",
    page_icon="🍄",
    layout="wide"
)

# عنوان التطبيق
st.title("🍄 المستودع الرقمي لفطريات الجبل الأخضر")
st.markdown("---")

# دالة لقراءة قاعدة البيانات من الإكسل أو CSV
@st.cache_data
def load_data():
    # البحث عن ملف البيانات سواء كان xlsx أو csv
    for file in os.listdir("."):
        if file.endswith(".xlsx"):
            return pd.read_excel(file)
        elif file.endswith(".csv"):
            return pd.read_csv(file)
    return None

df = load_data()

if df is None:
    st.error("لم يتم العثور على ملف قاعدة البيانات (الإكسل أو CSV) في المجلد الرئيسي!")
else:
    # القائمة الجانبية لاختيار الفطر
    st.sidebar.header("🔍 البحث والتصفية")
    species_list = df['Scientific_Name'].dropna().unique()
    selected_species = st.sidebar.selectbox("اختر الفطر:", species_list)
    
    # تصفية البيانات الخاصة بالفطر المختار
    row = df[df['Scientific_Name'] == selected_species].iloc[0]
    
    # عرض البيانات والتفاصيل في العمود الأيسر، والصور في العمود الأيمن
    col_info, col_img = st.columns([1, 1])
    
    with col_info:
        st.subheader(f"🌱 {row.get('Scientific_Name', 'اسم غير معروف')}")
        if 'Arabic_Name' in row and pd.notna(row['Arabic_Name']):
            st.markdown(f"**الاسم العربي / المحلي:** {row['Arabic_Name']}")
        
        st.markdown(f"**الموقع والجغرافيا:** `{row.get('Coordinates', 'غير محدد')}`")
        st.markdown(f"**تاريخ الجمع:** `{row.get('Collection_Date', 'غير محدد')}`")
        st.markdown(f"**التقييم والسمية:** `{row.get('Edibility_Status', 'غير محدد')}`")
        
        st.markdown("---")
        st.markdown("#### 🔬 الصفات المورفولوجية والمجهرية")
        
        # الأسطر المصححة بالكامل لتفادي خطأ f-string
        field_traits = row.get('Field_And_Macro_Traits', 'لا توجد بيانات')
        micro_traits = row.get('Microscopic_And_Spore_Traits', 'لا توجد بيانات')
        
        st.info(f"**الصفات الظاهرية والميدانية:** {field_traits}")
        st.success(f"**الفحص المجهري والأبواغ:** {micro_traits}")
        
    with col_img:
        st.markdown("#### 📷 التوثيق الفوتوغرافي والمجهري")
        
        # إنشاء التبويبات الثلاث للصور
        tab1, tab2, tab3 = st.tabs(["🖼️ العينة الميدانية", "🔍 تفاصيل الغطاء", "🔬 الأبواغ المجهرية"])
        
        # تحديد أسماء الصور القياسية بناءً على الاسم العلمي
        base_name = str(row.get('Image_Base_Name', '')).strip()
        if not base_name:
            base_name = str(row.get('Scientific_Name', '')).strip().lower().replace(' ', '_')
            
        field_img_path = os.path.join("images", f"{base_name}_field.jpg")
        cap_img_path = os.path.join("images", f"{base_name}_cap.jpg")
        spores_img_path = os.path.join("images", f"{base_name}_spores.jpg")
        
        with tab1:
            if os.path.exists(field_img_path):
                st.image(field_img_path, caption="الصورة الميدانية الحقلية", use_column_width=True)
            else:
                st.warning("الصورة الميدانية غير متوفرة حالياً.")
                
        with tab2:
            if os.path.exists(cap_img_path):
                st.image(cap_img_path, caption="تفاصيل الثمرة / الغطاء", use_column_width=True)
            else:
                st.warning("صورة الغطاء غير متوفرة حالياً.")
                
        with tab3:
            if os.path.exists(spores_img_path):
                st.image(spores_img_path, caption="الفحص المجهري للأبواغ", use_column_width=True)
            else:
                st.warning("صورة الأبواغ المجهرية غير متوفرة حالياً.")
