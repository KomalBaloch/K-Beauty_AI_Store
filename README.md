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
``` 

---
## ✅ Blockchain Integration (Future Scope)

In the future, this project can be enhanced with **Blockchain** to ensure transparency and authenticity in the beauty product supply chain.

✅ **How it will work:**
- Each product batch can have a **unique blockchain hash** stored on a public ledger.
- Users can scan a **QR code** on the product page to verify authenticity.
- Blockchain will record:
  - Manufacturing details
  - Expiration dates
  - Authentic seller details

✅ **Possible Tech Stack for Blockchain:**
- **Ethereum / Polygon** → Smart contracts for product verification
- **IPFS** → Decentralized storage for product certificates
- **Web3.py** → Blockchain interaction in Python
- **Metamask Wallet** → For secure authentication

This will make the store **tamper-proof** and **build customer trust** by ensuring every product is verified on-chain.



