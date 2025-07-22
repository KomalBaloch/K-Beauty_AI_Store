import streamlit as st
import pandas as pd
import json
from pathlib import Path

def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@300;400;500&display=swap');

        .stApp {
            background: linear-gradient(180deg, #fff8fb, #fff5f9);
            font-family: 'Poppins', sans-serif;
        }

        /* Titles styling */
        h1, h2, h3 {
            font-family: 'Playfair Display', serif !important;
            color: #c2185b;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        /* Product Card */
        .product-card {
            background: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
        .product-title {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #c2185b;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .product-meta {
            font-size: 14px;
            color: #6d6d6d;
            margin-bottom: 10px;
        }
        .product-desc {
            font-size: 15px;
            color: #444;
            line-height: 1.5;
        }

        .rec-header {
            color: #ad1457;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            margin: 30px 0 15px 0;
        }

        hr {
            border: none;
            height: 1px;
            background: #f3c4d3;
            margin: 20px 0;
        }

        /* ===== 🔥 KEY FIX ===== */
        /* Disable pointer + hover link icon for images & section headings */
        img, .stImage, .stMarkdown h2, .stMarkdown h3 {
            pointer-events: none !important;
            cursor: default !important;
        }

        /* Also disable dragging images */
        img {
            -webkit-user-drag: none;
            user-drag: none;
        }
        </style>
    """, unsafe_allow_html=True)

def load_products(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def show_product_cards(df):
    for _, row in df.iterrows():
        img_path = Path(row["image"])
        img_width = int(row["image_width"]) if "image_width" in row and pd.notna(row["image_width"]) else 200

        col1, col2 = st.columns([1, 2])
        with col1:
            if img_path.exists():
                st.image(str(img_path), width=img_width)
            else:
                st.warning(f"⚠️ Image not found: {img_path}")
        with col2:
            st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{row['name']} – {row['price']}</div>
                <div class="product-meta">
                    <b>Category:</b> {row['category']} | ⭐ {row['rating']} / 5
                </div>
                <div class="product-desc">{row['description']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

def get_recommendations(df, selected_product):
    category = df.loc[df["name"] == selected_product, "category"].values[0]
    return df[(df["category"] == category) & (df["name"] != selected_product)]

def main():
    st.set_page_config(page_title="K-Beauty AI Store", page_icon="💄", layout="wide")
    local_css()

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1058/1058984.png", width=90)
        st.markdown("### K-Beauty AI Store")
        st.write("*Your personalized beauty product guide.*")
        st.write("Built by **Komal**")
        st.write("Prices in **USD**")
        st.markdown("---")
        st.caption("Select a product → Get AI-powered recommendations")

    st.markdown("""
        <div style="text-align:center; padding:25px 10px;">
            <h1>K-Beauty AI Store</h1>
            <p style="font-size:18px; color:#6d6d6d; max-width:600px; margin:auto;">
                Discover curated makeup essentials with smart recommendations powered by AI. 
                Simple. Elegant. Tailored for your beauty journey.
            </p>
        </div>
    """, unsafe_allow_html=True)

    df = load_products("products.json")

    st.markdown("## ✨ Featured Makeup Collection")
    show_product_cards(df)

    st.markdown("---")
    st.markdown("## 🔍 Find Similar Products")
    selected_product = st.selectbox("Choose a product you like:", df["name"].tolist())
    
    if selected_product:
        st.markdown(f"<div class='rec-header'>Similar to <b>{selected_product}</b></div>", unsafe_allow_html=True)
        recommendations = get_recommendations(df, selected_product)
        if not recommendations.empty:
            show_product_cards(recommendations)
        else:
            st.markdown("""
                <div style="
                    background: #ffe4ec; 
                    color: #880e4f; 
                    padding: 15px; 
                    border-radius: 12px; 
                    text-align: center; 
                    font-size: 16px; 
                    font-weight: 500;
                    border: 1px solid #f5b7c5;
                    max-width: 500px;
                    margin: 15px auto;
                ">
                💡 No other products available in this category.<br>Try exploring another one!
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2025 K-Beauty Labs | Created by Komal for AI Developer Test")

if __name__ == "__main__":
    main()
