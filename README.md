# K-Beauty AI Store

A **Streamlit-based beauty store** where users can:  
✅ Filter products by **category** & **price**  
✅ View **premium product cards** with images & details  
✅ Get **smart recommendations** for similar products  

---

## 🛠️ Tech Stack & Libraries  

- **Python 3.9+**  
- **Streamlit** → Interactive web app  
- **Pandas** → Data handling for product catalog  
- **JSON** → Product data storage (`products.json`)  
- **Pathlib** → Local image handling  
- **Custom CSS + Google Fonts** → Premium UI design  

---

## 📂 Project Structure  

kbeauty_ai_store/
├── app.py # Main Streamlit application
├── products.json # Product catalog
├── images/ # Local product images
└── README.md # Documentation


---

## ✅ Assumptions  

- Product data is stored in `products.json` in **this format**:  

```json
[
  {
    "name": "Velvet Lipstick",
    "price": "$20",
    "category": "Lips",
    "rating": 4.6,
    "description": "Matte finish lipstick with long-lasting color.",
    "image": "images/lipstick.jpg",
    "image_width": 200
  },
  {
    "name": "Hydrating Foundation",
    "price": "$35",
    "category": "Face",
    "rating": 4.8,
    "description": "Lightweight foundation with 24-hour hydration.",
    "image": "images/foundation.jpg",
    "image_width": 220
  }
]
