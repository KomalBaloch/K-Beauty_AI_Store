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
        /* Import elegant Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@300;400;500&display=swap');

        /* Overall App Background */
        .stApp {
            background: linear-gradient(180deg, #fff8fb, #fff5f9);
            font-family: 'Poppins', sans-serif;
        }

        /* Titles (Luxury Style) */
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            text-align: center;
            color: #c2185b; /* soft rose color */
            font-weight: 600;
            letter-spacing: 1px;
        }
        h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #880e4f;
            letter-spacing: 0.5px;
        }

        /* Product Card Styling */
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

        /* Recommendation Section Header */
        .rec-header {
            color: #ad1457;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            margin: 30px 0 15px 0;
        }

        /* Divider line */
        hr {
            border: none;
            height: 1px;
            background: #f3c4d3;
            margin: 20px 0;
        }

        /* Sidebar text */
        .css-1d391kg, .css-1v3fvcr {
            font-family: 'Poppins', sans-serif;
        }

        /* ✅ Disable pointer hover + link cursor on all headings & images */
        img, .stImage, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            pointer-events: none !important;
            cursor: default !important;
        }

        /* ✅ Prevent image dragging */
        img {
            -webkit-user-drag: none;
            user-drag: none;
        }

        /* ✅ Center align Featured Makeup Collection heading */
        .featured-title {
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #c2185b;
            margin: 30px 0 20px 0;
        }

        /* ✅ Custom Dropdown (Selectbox) Styling */
        div[data-baseweb="select"] > div {
            background-color: #ffeaf3 !important; /* soft pink background */
            border-radius: 10px;
            border: 1px solid #f5b7c5 !important;
            color: #880e4f !important;
            font-weight: 500;
        }
        div[data-baseweb="select"] svg {
            fill: #c2185b; /* dropdown arrow color */
        }

        /* ✅ Dropdown options list background */
        ul[role="listbox"] {
            background-color: #fff6fa !important;  /* soft blush background */
            border: 1px solid #f5b7c5 !important;
            border-radius: 8px !important;
        }

        /* ✅ Each option text color */
        li[role="option"] {
            background-color: #fff6fa !important;
            color: #880e4f !important;
            font-weight: 500;
            transition: all 0.2s ease-in-out;
        }

        /* ✅ Hover effect for dropdown options */
        li[role="option"]:hover {
            background-color: #fde3ec !important;  /* pale rose hover */
            color: #c2185b !important;
        }

        /* ✅ Highlighted selected option */
        li[aria-selected="true"] {
            background-color: #fbdce8 !important;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

# ========================
# Load Product Catalog
# ========================
def load_products(file_path: str):
    """Load product catalog from JSON file into a DataFrame."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# ========================
# Show Products with Local Images & Adjustable Sizes
# ========================
def show_product_cards(df):
    for _, row in df.iterrows():
        img_path = Path(row["image"])

        # ✅ If image_width is missing, use default 200
        img_width = int(row["image_width"]) if "image_width" in row and pd.notna(row["image_width"]) else 200

        col1, col2 = st.columns([1, 2])

        # ✅ LEFT: Product Image
        with col1:
            if img_path.exists():
                st.image(str(img_path), width=img_width)
            else:
                st.warning(f"⚠️ Image not found: {img_path}")

        # ✅ RIGHT: Product Details
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

        # ✅ Soft divider between products
        st.markdown("<hr>", unsafe_allow_html=True)

# ========================
# Recommendation Logic
# ========================
def get_recommendations(df, selected_product):
    """Get similar products based on category."""
    category = df.loc[df["name"] == selected_product, "category"].values[0]
    return df[(df["category"] == category) & (df["name"] != selected_product)]

# ========================
# Streamlit UI
# ========================
def main():
    st.set_page_config(page_title="K-Beauty AI Store", page_icon="💄", layout="wide")
    local_css()  # Apply premium styles
    
    # === Sidebar (Minimal Elegant Info) ===
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1058/1058984.png", width=90)
        st.markdown("### K-Beauty AI Store")
        st.write("*Your personalized beauty product guide.*")
        st.write("Built by **Komal**")
        st.write("Prices in **USD**")
        st.markdown("---")
        st.caption("Select a product → Get AI-powered recommendations")

    # === Hero Section ===
    st.markdown("""
        <div style="text-align:center; padding:25px 10px;">
            <h1>K-Beauty AI Store</h1>
            <p style="font-size:18px; color:#6d6d6d; max-width:600px; margin:auto;">
                Discover curated makeup essentials with smart recommendations powered by AI. 
                Simple. Elegant. Tailored for your beauty journey.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ✅ Load product catalog
    df = load_products("products.json")
    
    # === Catalog Section ===
    st.markdown('<div class="featured-title">✨ Featured Makeup Collection</div>', unsafe_allow_html=True)
    show_product_cards(df)

    # === Selection for AI Recommendations ===
    st.markdown("---")
    st.markdown('<div class="featured-title">🔍 Find Similar Products</div>', unsafe_allow_html=True)
    
    selected_product = st.selectbox("Choose a product you like:", df["name"].tolist())
    
    if selected_product:
        st.markdown(f"<div class='rec-header'>Similar to <b>{selected_product}</b></div>", unsafe_allow_html=True)
        recommendations = get_recommendations(df, selected_product)
        
        if not recommendations.empty:
            show_product_cards(recommendations)
        else:
            # ✅ Custom styled visible info box
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
