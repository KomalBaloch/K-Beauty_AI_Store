import streamlit as st
import pandas as pd
import json

# Load Product Catalog
def load_products(file_path: str):
    """Load product catalog from JSON file into a DataFrame."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Recommendation Logic
def get_recommendations(df, selected_product):
    """Get similar products based on category."""
    category = df.loc[df["name"] == selected_product, "category"].values[0]
    return df[(df["category"] == category) & (df["name"] != selected_product)]

# Streamlit UI
def main():
    st.set_page_config(page_title="K-Beauty AI Store", page_icon="💄", layout="centered")
    
    st.title("💄 K-Beauty AI Store")
    st.write("Welcome to **K-Beauty AI-powered Makeup Store**! Explore our products and get smart recommendations instantly. ✨")
    
    # Load product catalog
    df = load_products("products.json")
    
    # Display catalog
    st.subheader("📦 Makeup Product Catalog")
    st.dataframe(df, use_container_width=True)
    
    # Product selection
    selected_product = st.selectbox("💡 Select a product to see similar recommendations:", df["name"].tolist())
    
    if selected_product:
        st.success(f"✅ You selected: **{selected_product}**")
        recommendations = get_recommendations(df, selected_product)
        
        st.subheader("🤖 AI Recommendations for You")
        if not recommendations.empty:
            st.table(recommendations)
        else:
            st.info("No similar products found.")
    
    st.markdown("---")
    st.caption("💻 Built by **K-Beauty Labs (Komal)** | AI Developer Test Project")

if __name__ == "__main__":
    main()
