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

        /* Overall App Background */
        .stApp {
            background: linear-gradient(180deg, #fff8fb, #fff5f9);
            font-family: 'Poppins', sans-serif;
        }

        /* Hero Section Styling */
        .hero-section {
            background: linear-gradient(135deg, #d81b60, #880e4f);
            padding: 40px 20px;
            text-align: center;
            border-radius: 12px;
            margin-bottom: 30px;
        }

        .hero-section h1 {
            font-family: 'Playfair Display', serif;
            font-size: 44px;
            color: #fff;
            font-weight: 700;
            margin-bottom: 12px;
        }

        /* Remove Streamlit hover pin icon */
        .css-15zrgzn { display: none !important; }

        .hero-section p {
            font-size: 18px;
            color: #fce4ec;
            max-width: 650px;
            margin: auto;
        }

        /* Trolley Icon */
        .trolley-icon {
            font-size: 60px;
            display: block;
            margin: 0 auto 15px auto;
        }

        /* Featured Section Title */
        .featured-title {
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #c2185b;
            margin: 30px 0 20px 0;
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
        .css-q8sbsg p {
            word-break: break-word;
            margin-bottom: 0px;
           font-size: 14px;
        
        }
        .css-8ojfln {
           display: table-cell;
           
        }
        .st-c7 {
           padding-right: 0.5rem;
           
        }
        .product-desc {
            font-size: 15px;
            color: #444;
            line-height: 1.5;
        }

        /* Recommendation Section Header */
        .rec-header {
            
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            margin: 30px 0 15px 0;
        }
    .css-nahz7x p {
            word-break: break-word;
            
        }
    .st-e5 {
            background-color: rgb(0 0 0 / 80%);
        }
        hr {
            border: none;
            height: 1px;
            background: #f3c4d3;
            margin: 20px 0;
        }
        
        </style>
    """, unsafe_allow_html=True)

# ========================
# Load Product Catalog
# ========================
def load_products(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("❌ `products.json` not found!")
        return pd.DataFrame()

# ========================
# Show Products with Local Images & Adjustable Sizes
# ========================
def show_product_cards(df):
    for _, row in df.iterrows():
        img_path = Path(row.get("image", ""))
        img_width = int(row.get("image_width", 200)) if pd.notna(row.get("image_width")) else 200

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

# ========================
# Recommendation Logic
# ========================
def get_recommendations(df, selected_product):
    if selected_product not in df["name"].values:
        return pd.DataFrame()
    category = df.loc[df["name"] == selected_product, "category"].values[0]
    return df[(df["category"] == category) & (df["name"] != selected_product)]

# ========================
# Streamlit UI
# ========================
def main():
    st.set_page_config(page_title="K-Beauty AI Store", page_icon="💄", layout="wide")
    local_css()

    # === Hero Section ===
    st.markdown("""
        <div class="hero-section">
            <div class="trolley-icon">🛍️</div>
            <h1>K-Beauty AI Store</h1>
            <p>Discover curated makeup essentials with smart recommendations powered by AI.<br>Simple. Elegant. Tailored for your beauty journey.</p>
        </div>
    """, unsafe_allow_html=True)

    # ✅ Load product catalog
    df = load_products("products.json")
    if df.empty:
        st.stop()

    # ✅ Convert price safely (remove $)
    df["price_num"] = pd.to_numeric(df["price"].str.replace("$", "", regex=False), errors="coerce")

    # === Catalog Section ===
    st.markdown('<div class="featured-title">Featured Makeup Collection</div>', unsafe_allow_html=True)

    # ✅ Dynamic category list
    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.selectbox("Filter by Category", categories)

    # ✅ Dynamic min & max price
    min_price = int(df["price_num"].min())
    max_price = int(df["price_num"].max())
    price_filter = st.slider("Filter by Price (max)", min_price, max_price, max_price)

    # ✅ Apply filters
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]

    filtered_df = filtered_df[filtered_df["price_num"] <= price_filter]

    # ✅ Show products or empty message
    if filtered_df.empty:
        st.warning(f"No products found under ${price_filter}. Try changing the filters.")
    else:
        show_product_cards(filtered_df)

    # === Recommendation Section ===
    st.markdown("---")
    st.markdown('<div class="featured-title"> Find Similar Products</div>', unsafe_allow_html=True)

    product_list = ["-- Select a product --"] + df["name"].tolist()
    selected_product = st.selectbox("Choose a product you like:", product_list, index=0)

    if selected_product != "-- Select a product --":
        st.markdown(f"<div class='rec-header'>Similar to <b>{selected_product}</b></div>", unsafe_allow_html=True)
        recommendations = get_recommendations(df, selected_product)
        if not recommendations.empty:
            show_product_cards(recommendations)
        else:
            st.markdown("""
                <div style="background: #ffe4ec; color: #880e4f; padding: 15px;
                            border-radius: 12px; text-align: center; font-size: 16px; font-weight: 500;
                            border: 1px solid #f5b7c5; max-width: 500px; margin: 15px auto;">
                 No other products available in this category.<br>Try exploring another one!
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; font-size:14px; color:#6a1b9a;'>© 2025 K-Beauty Labs | Built by <b>Komal Sakhidad</b></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
