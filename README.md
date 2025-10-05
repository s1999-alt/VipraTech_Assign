# VipraTech Django Assignment

A simple Django + Stripe application for purchasing fixed products and viewing paid orders.

---

## Features
- 3 fixed products shown on the homepage.
- Stripe Checkout integration (Test Mode).
- Prevents double submissions using Stripe session IDs.
- Authenticated users can purchase and view their own orders.
- Bootstrap UI.

---

## Assumptions
- Single-page flow for simplicity (all products and orders visible on one page).
- Using **Stripe Checkout** instead of Payment Intents for simplicity and reliability.
- Users must be logged in to buy products.

---

## Flow Chosen
**Stripe Checkout** was chosen because it:
- Handles payment UI, success/cancel redirects automatically.
- Reduces chances of duplicate charges.
- Simpler to integrate.

---

## Avoiding Double Charge / Inconsistent State
- Order is created **before redirecting** to Stripe with a unique `payment_id` (Session ID).
- After payment success, we retrieve the session from Stripe and update that specific order.
- If the session is invalid or reused, the order will not be marked as paid.
- This ensures idempotency and prevents double-charging.

---

## ⚙️ Setup and Run Steps

1. **Clone the repo**
   ```bash
   git clone https://github.com/s1999-alt/VipraTech_Assign.git
   cd vipratech_assignment


2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate  # Windows
```

3. **Install dependencies**   
```bash
pip install -r requirements.txt
``` 

4. **Add environment variables**

- Create a .env file using .env.example.
- Add your Stripe test keys.
- Add your secret keys etc..


5. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate  
```  

6. **Create a superuser (Admin)**
```bash
python manage.py createsuperuser 
```  

7. **Run server**
```bash
python manage.py runserver
```  

### Server runs at:
```bash
http://127.0.0.1:8000/
``` 


### Notes on Code Quality

- Used clear separation of concerns (models, views, templates).

- Environment variables handled using python-decouple.

- Used Django authentication for secure access to “My Orders”.

- Applied Bootstrap for responsive UI.


### AI Tool Used: ChatGPT (OpenAI GPT-5)

**Assisted in:**
- Structuring Django + Stripe checkout flow.
- Designing the index.html and base.html layout.
- Creating README and .env.example structure.

- All code was reviewed, tested, and understood manually before submission.


### Time Spent

**⏱ Total Time Spent:** ~10 hours


### Improvements

- In the current setup, payment status is verified immediately after checkout using stripe.checkout.Session.retrieve().
While this works for synchronous payments, it may miss delayed or asynchronous events (e.g., UPI or bank transfers) or cases where the user closes the tab before redirection.

**Proposed Improvement — Use Stripe Webhooks** 

**Why Webhooks?**

- Webhooks automatically notify the backend when an event occurs (e.g., checkout.session.  completed).

- Reliable even if frontend fails or user closes browser.

- Prevents data mismatches or double charge cases.



