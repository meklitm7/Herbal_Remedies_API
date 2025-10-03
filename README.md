# 🌿 Herbal Remedies API  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-4.x-darkgreen?logo=django&logoColor=white)  
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-API-red?logo=django&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-yellow)  

---

## 📌 Project Overview  

The **Herbal Remedies API** is a backend system built with **Django** and **Django REST Framework (DRF)** that allows users to manage and organize natural herbal remedies.  
Users can add, update, delete, and view herbal entries that include medicinal uses and precautions.  

This project simulates a real-world backend application focusing on **database management, CRUD operations, and API design**.  

---

## 🚀 Features  

### 🌱 Herb Management (CRUD)  
- Create, Read, Update, and Delete herbs.  
- Each herb entry includes:  
  - Name (e.g., Ginger, Aloe Vera)  
  - Category (leaf, root, seed, flower, etc.)  
  - Description  
  - Medical Uses (e.g., “helps with digestion”)  
  - Precautions (e.g., “not recommended during pregnancy”)  
  - Created By (User who added the herb)  
- Validations for required fields.  

### 👤 User Management  
- Uses Django’s built-in **User model** (Username, Email, Password).  
- Each herb is linked to its creator.  
- In future versions:  
  - Users will register and authenticate.  
  - Users will only manage their own entries.  

### 🔎 Search & Filtering *(Planned for Capstone 4+)*  
- Search herbs by **name** or **ailment/medical use**.  
- Optional filters by category.  

### 📑 Additional Features (Future Goals)  
- Authentication & Token-based access.  
- Pagination for large datasets.  
- Sorting herbs (e.g., alphabetically or by category).  
- Deployment on **Heroku** or **PythonAnywhere**.  

---

## 🛠 Technical Stack  
- **Backend**: Django, Django REST Framework (DRF)  
- **Database**: SQLite (development), MySQL/PostgreSQL (production)  
- **Authentication**: Django Authentication (DRF Token planned)  
- **Deployment**: PythonAnywhere / Heroku  
- **Version Control**: Git + GitHub  

---

## 🔑 Authentication  
- Currently using **Django’s built-in User model**.  
- Herbs must include a `created_by` field referencing the user’s ID.  
- In the next phase (Capstone 4), users will register and login, and herbs will automatically link to the logged-in user.  

---

## ⚙️ Installation & Setup  

### Clone the Repository  
```bash
git clone https://github.com/yourusername/herbal-remedies-api.git
cd herbal-remedies-api
