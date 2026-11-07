import streamlit as st
import pandas as pd
import os

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="المستودع الرقمي لفطريات الجبل الأخضر - ليبيا",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# عنوان التطبيق والمقدمة
st.title("🍄 المستودع الرقمي التوثيقي لفطريات الجبل الأخضر (ليبيا)")
st.markdown("""
**إعداد وتوثيق:** أ. أسماء المبروك عبد السيد  
*مركز البحوث الزراعية والحيوانية - البيضاء، ليبيا*
---
""" )

# اسم ملف الإكسل ومجلد الصور
EXCEL_FILE = "macrofungi_database_template.xlsx"
IMAGE_DIR = "images"

# التحقق من وجود ملف الإكسل
if not os.path.exists(EXCEL_FILE):
    st.error(f"❌ لم يتم العثور على ملف البيانات `{EXCEL_FILE}`! يرجى التأكد من وضعه في المجلد الرئيسي.")
    st.stop()

# قراءة البيانات
@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

df = load_data()

# شريط البحث والتصفية في القائمة الجانبية
st.sidebar.header("🔍 تصفية العينات المعشبية")
search_term = st.sidebar.text_input("بحث برقم العينة أو الاسم العلمي:", "")
family_filter = st.sidebar.multiselect(
    "تصفية حسب العائلة / المجموعة:",
    options=df["Family_Or_Group"].unique() if "Family_Or_Group" in df.columns else [],
    default=[]
)

# تصفية البيانات
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[
        filtered_df["Specimen_ID"].astype(str).str.contains(search_term, case=False) |
        filtered_df["Scientific_Name"].astype(str).str.contains(search_term, case=False) |
        filtered_df["Arabic_Name"].astype(str).str.contains(search_term, case=False)
    ]

if family_filter:
    filtered_df = filtered_df[filtered_df["Family_Or_Group"].isin(family_filter)]

st.sidebar.markdown(f"**عدد العينات المعروضة:** `{len(filtered_df)}` من أصل `{len(df)}`")

# عرض العينات
if filtered_df.empty:
    st.warning("⚠️ لا توجد عينات تطابق خيارات البحث الحالية.")
else:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"📌 **[{row['Specimen_ID']}]** - *{row['Scientific_Name']}* ({row['Arabic_Name']})", expanded=True):
            col_info, col_img = st.columns([1.2, 1])
            
            with col_info:
                st.markdown(f"### 🧪 **بيانات العينة والمعشبة**")
                st.markdown(f"* **الاسم العلمي:** *{row['Scientific_Name']}*")
                st.markdown(f"* **الاسم العربي / الشائع:** {row['Arabic_Name']}")
                st.markdown(f"* **العائلة / المجموعة:** `{row['Family_Or_Group']}`")
                st.markdown(f"* **الموقع:** {row['Location']}")
                if pd.notna(row.get('Coordinates')) and str(row.get('Coordinates')) != "N/A":
                    st.markdown(f"* **الإحداثيات الجغرافية:** `{row['Coordinates']}`")
                st.markdown(f"* **تاريخ الجمع:** `{row['Collection_Date']}`")
                st.markdown(f"* **التقييم والسمية:** `{row['Edibility_Status']}`")
                
                st.markdown("---")
                st.markdown("#### 🔬 **الصفات المورفولوجية والمجهرية**")
                st.info(f"**الصفات الظاهرية والميدانية:**

{row['Field_And_Macro_Traits']}")
                st.success(f"**الفحص المجهري والأبواغ:**

{row['Microscopic_And_Spore_Traits']}")

            with col_img:
                st.markdown("### 📸 **التوثيق الفوتوغرافي والمعشبي**")
                tab1, tab2, tab3 = st.tabs(["🖼️ العينة الميدانية", "🔍 تفاصيل الغطاء", "🔬 الأبواغ المجهرية"])
                
                # وظيفة مسبقة لعرض الصورة والتأكد من وجودها
                def show_specimen_image(img_name, caption):
                    if pd.notna(img_name):
                        img_path = os.path.join(IMAGE_DIR, str(img_name).strip())
                        if os.path.exists(img_path):
                            st.image(img_path, caption=caption, use_container_width=True)
                        else:
                            st.warning(f"📷 صورة غير متوفرة: `{img_name}` في مجلد images")
                    else:
                        st.caption("لا توجد صورة مسجلة.")

                with tab1:
                    show_specimen_image(row.get('Field_Image'), f"العينة الميدانية - {row['Specimen_ID']}")
                with tab2:
                    show_specimen_image(row.get('Cap_Detail_Image'), f"تفاصيل الغطاء والساق - {row['Specimen_ID']}")
                with tab3:
                    show_specimen_image(row.get('Spore_Microscope_Image'), f"الفحص المجهري والأبواغ - {row['Specimen_ID']}")

st.markdown("---")
st.caption("Developed for Mycological Taxonomy Research © 2026 Asma Almabrok | Agricultural Research Center")
