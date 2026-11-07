@st.cache_data
def load_data():
    for file in os.listdir("."):
        if file.endswith(".csv"):
            return pd.read_csv(file)
    return None
