# Black-Scholes-Option-Pricer
Web-based dashboard built with Dash and QuantLib to price European call and put options using the Black–Scholes–Merton model. It provides option valuation, adjustable parameters, and interactive heatmaps that visualize price sensitivity to volatility and spot price. Designed for quantitative finance learners and traders to explore option dynamics.

## 🚀 Features
- Real-time computation of **Call** and **Put** option prices  
- Interactive **heatmaps** showing sensitivity to volatility and spot  
- Adjustable inputs for **S, K, r, σ, T**  
- Built with **Python**, **Dash**, **Plotly**, and **QuantLib**

---

## 📁 Project Structure
Black-Scholes-Option-Pricer/
├── assets/  
│ ├── style.css  
│ └── preview.png  
├── app.py  
├── utils.py  
├── environment.yml  
└── README.md  
  
---  
  
## ⚙️ Installation  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/Black-Scholes-Option-Pricer.git
cd Black-Scholes-Option-Pricer
```
  
2️⃣ Create Environment
  
Using Conda:
```bash
conda env create -f environment.yml
conda activate blackScholesPricer
```

3️⃣ Run the App
```python
python app.py
```  
Open your browser at: 
http://127.0.0.1:8050
  
📸 Example Screenshot
![App Preview](assets/preview.png)  
    
📦 Dependencies
-Python ≥ 3.9  
-Dash  
-Plotly  
QuantLib  
-Pandas  
-NumPy    
  
📜 License  
  
This project is licensed under the MIT License.  
You are free to use, modify, and distribute it with attribution.
    
👤 Author  
  
Anjaneeya B  
GitHub: @AnjaneeyaB  
  
“In investing, what is comfortable is rarely profitable.” — Robert Arnott


