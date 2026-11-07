@st.cache_data
def load_data():
    csv_file = "macrofungi_database_template.csv"
    if os.path.exists(csv_file):
        # المحاولة الأولى بترميز utf-8-sig والمحاولة الثانية بترميز windows-1256 العربي
        for enc in ['utf-8-sig', 'utf-8', 'cp1256', 'latin1']:
            try:
                return pd.read_csv(csv_file, encoding=enc)
            except:
                continue
    return None
