# wordcloud_generator.py
import pandas as pd
from wordcloud import WordCloud
import ast
import matplotlib.pyplot as plt
import streamlit as st

def generate_sector_wordcloud(sector=None):
    st.title("🏘️ Word Cloud of Property Features by Sector")

    df1 = pd.read_csv('datasets/gurgaon_properties.csv')#no sector 
    df2 = pd.read_csv('datasets/gurgaon_properties_missing_value_imputation.csv')# has sector
    df = df1.merge(df2, left_index=True, right_index=True)[['features', 'sector']]

    # Dropdown to choose sector

    col1, col2 = st.columns([1, 4])  # 1: small column, 4: large column
    with col1:
        sector = st.selectbox("Choose Sector", load_sectors(df))

    if sector and sector != "All Region":
        df = df[df['sector'] == sector]

    text = get_text(df)
    # Generate word cloud
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig1 = plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad = 0)
    st.pyplot(fig1)


def get_text(df):
    main = []
    for item in df['features'].dropna().apply(ast.literal_eval):
        main.extend(item)

    text = ' '.join(main)
    return text

def load_sectors(df):
    # Drop missing and deduplicate
    sectors = df['sector'].dropna().unique()

    # Sort by numeric part after "sector "
    def sector_key(x):
        try:
            return int(x.lower().replace('sector', '').strip())
        except:
            return float('inf')  # put non-matching strings at end

    sorted_sectors = sorted(sectors, key=sector_key)

    return ["All Region"] + sorted_sectors


