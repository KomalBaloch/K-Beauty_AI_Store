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
        .css-15zrgzn {
            display: none !important;
        }
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
        .css-8ojfln {
            font-weight: 500 !important;
            color: rgba(250, 250, 250, 0.6) !important;
        }

        /* Hover effect for dropdown list items */
        .css-8ojfln:hover {
            background-color: #f8bbd0 !important; /* slightly darker pink on hover */
            color: #6a1b9a !important;            /* purple hover text */
        }
                
        /* Divider line */
        hr {
            border: none;
            height: 1px;
            background: #f3c4d3;
            margin: 20px 0;
        }
        /* Force selectbox dropdown to open downward */
        div[data-baseweb="popover"] {
            top: 15px !important;            /* Reset top */
            bottom: auto !important;         /* Reset bottom */
            left: 50% !important;            /* Move horizontally to center */
            transform: translate(-50%, 100%) !important; /* Center + push downward */
            margin: 0 auto !important;       /* Extra centering */
}


        /* Dropdown container */
        div[data-baseweb="select"] > div {
            background-color: #f8e1f1;
            border-radius: 10px;
            border: 1px solid #e1a4c6 ;
            color: #6a1b9a ; /* purple text */
            font-weight: 500;
        }
        /* Dropdown arrow */
        div[data-baseweb="select"] svg {
            fill: #8e24aa;
        }
        ul[role="listbox"] li:hover {
            background: #f8bbd0 !important;  /* darker hover pink */
            color: #6a1b9a !important;       /* purple hover text */
        }
        </style>
    """, unsafe_allow_html=True)

# ========================
# Save & Restore Scroll Position
# ========================
def save_scroll_js():
    st.markdown("""
        <script>
        // Save scroll position before refresh
        window.addEventListener("beforeunload", function () {
            localStorage.setItem("scrollPosition", window.scrollY);
        });

        // Restore scroll position after refresh
        window.addEventListener("load", function () {
            let scrollY = localStorage.getItem("scrollPosition");
            if (scrollY !== null) {
                window.scrollTo(0, parseInt(scrollY));
            }
        });
        </script>
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
    local_css()
    save_scroll_js()  # ✅ Enable scroll memory

    # === Hero Section ===
    st.markdown("""
        <div class="hero-section">
            <div class="trolley-icon">🛍️</div>
            <h1>K-Beauty AI Store</h1>
            <p>
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

    # === Recommendation Section ===
    st.markdown("---")
    st.markdown('<div class="featured-title">🔍 Find Similar Products</div>', unsafe_allow_html=True)

    # ✅ Dropdown with a dummy option for old Streamlit
    product_list = ["-- Select a product --"] + df["name"].tolist()
    selected_product = st.selectbox(
        "Choose a product you like:",
        product_list,
        index=0  # always default to dummy option
    )

    # ✅ Show recommendations ONLY if user selects a valid product
    if selected_product != "-- Select a product --":
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
    st.markdown(
        "<p style='text-align:center; font-size:14px; color:#6a1b9a;'>© 2025 K-Beauty Labs | Built by <b>Komal</b></p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
