import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ========================
# Custom CSS for Premium Beauty Look
# ========================
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@300;400;500&display=swap');

        /* App Background */
        .stApp {
            background: linear-gradient(180deg, #fff8fb, #fff5f9);
            font-family: 'Poppins', sans-serif;
        }

        /* Headings */
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            text-align: center;
            color: #c2185b;
            font-weight: 600;
            letter-spacing: 1px;
        }
        h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #880e4f;
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

        /* Recommendation Section */
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

        /* Disable pointer hover */
        img, .stImage, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            pointer-events: none !important;
            cursor: default !important;
        }
        img { -webkit-user-drag: none; user-drag: none; }

        /* Center align Featured Makeup Collection heading */
        .featured-title {
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #c2185b;
            margin: 30px 0 20px 0;
        }

        /* Custom Dropdown */
        div[data-baseweb="select"] > div {
            background-color: #f7e9ff !important;
            border-radius: 10px;
            border: 1px solid #e2b4ff !important;
            color: #5c2a68 !important;
            font-weight: 500;
        }
        div[data-baseweb="select"] svg {
            fill: #8e24aa;
        }

        /* ✅ FULL DARK PINK SIDEBAR */
        [data-testid="stSidebar"] {
            background: #c2185b !important; /* Dark pink full sidebar */
            color: white !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* Keep footer pinned */
            height: 100vh; /* Full height */
        }

        /* Sidebar Title */
        .sidebar-title {
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            margin-top: 15px;
        }

        /* Sidebar Content Wrapper to push footer */
        .sidebar-content {
            flex-grow: 1;
        }

        /* Sidebar Footer (ALWAYS at bottom) */
        .sidebar-footer {
            text-align: center;
            font-size: 14px;
            color: #ffe6f0;
            padding: 15px 5px;
            margin-top: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# ========================
# Load Product Catalog
# ========================
def load_products(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# ========================
# Show Products
# ========================
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
                <div class="product-meta"><b>Category:</b> {row['category']} | ⭐ {row['rating']} / 5</div>
                <div class="product-desc">{row['description']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

# ========================
# Recommendation Logic
# ========================
def get_recommendations(df, selected_product):
    category = df.loc[df["name"] == selected_product, "category"].values[0]
    return df[(df["category"] == category) & (df["name"] != selected_product)]

# ========================
# MAIN UI
# ========================
def main():
    st.set_page_config(page_title="K-Beauty AI Store", page_icon="💄", layout="wide")
    local_css()

    # ✅ DARK PINK SIDEBAR with footer STICKY at absolute bottom
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-content" style="text-align:center;">
                <img src="https://cdn-icons-png.flaticon.com/512/891/891462.png" width="70" style="margin-bottom:10px;" />
                <div class="sidebar-title">K-Beauty AI Store</div>
            </div>
            <div class="sidebar-footer">
                Built by Komal
            </div>
        """, unsafe_allow_html=True)

    # HERO SECTION
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

    # FEATURED COLLECTION
    st.markdown('<div class="featured-title">✨ Featured Makeup Collection</div>', unsafe_allow_html=True)
    show_product_cards(df)

    # RECOMMENDATION SECTION
    st.markdown("---")
    st.markdown('<div class="featured-title">🔍 Find Similar Products</div>', unsafe_allow_html=True)

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
                    margin: 15px auto;">
                💡 No other products available in this category.<br>Try exploring another one!
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2025 K-Beauty Labs | Created by Komal for AI Developer Test")

if __name__ == "__main__":
    main()
