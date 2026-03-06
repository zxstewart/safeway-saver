# Safeway Saver

A Flask web app that helps users save money by:
- Scraping current Safeway grocery deals (https://www.safeway.com/weeklyad)
- Matching those deals to the user's weekly shopping list
- Recommending sale items they've purchased in the past

This project uses **PostgreSQL** for persistent user history and is deployed on **Render**.

---

## Features

- Input weekly grocery list
- Find out which list items are on sale
- Get suggestions for sale items that have been bought before
- Uses PostgreSQL to remember shopping habits

---

## Tech Stack

- Python 3
- Flask
- BeautifulSoup (placeholder scraper)
- PostgreSQL (via psycopg2)/SQLite locally
- HTML/CSS (frontend)

---

## Running the App

The app detects its environment automatically:

| Environment | Database | How it's triggered |
|---|---|---|
| Local | SQLite (auto-created as `safeway.db`) | `DATABASE_URL` is not set |
| Render | PostgreSQL | Render injects `DATABASE_URL` at runtime |

No code changes are needed when switching between environments.

### Running locally

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/safeway-saver.git
   cd safeway-saver
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows
   # or
   source venv/bin/activate        # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install flask python-dotenv beautifulsoup4 requests pandas
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser

SQLite creates `safeway.db` automatically on first run. No database setup required.

---

## Deployment (Render)

The `render.yaml` blueprint provisions a free web service and a free PostgreSQL database automatically.

1. Push the repo to GitHub
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo — Render detects `render.yaml` and configures everything
4. Click **Deploy**

Render injects `DATABASE_URL` into the app automatically. Tables are created on first boot.

> **Note:** Render's free PostgreSQL databases expire after 90 days. To avoid this, see the Supabase migration instructions below.

---

## Migrating the Database to Supabase (optional, permanent free tier)

Supabase offers a free PostgreSQL database with no expiry (500MB limit). No code changes are needed — only the connection string has to be swapped.

### Steps

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **New project** and fill in a name and password (save the password)
3. Once the project is ready, go to **Project Settings > Database**
4. Under **Connection string**, select the **URI** tab and copy the string — it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
5. In your Render dashboard, go to your web service > **Environment**
6. Add (or update) the environment variable:
   - Key: `DATABASE_URL`
   - Value: the connection string from step 4
7. Trigger a new deploy — the app will connect to Supabase and recreate its tables on boot

### Disconnecting the Render database

Once Supabase is working, you can delete the Render PostgreSQL instance from the Render dashboard to stay within free tier limits. Also remove the `databases:` block from `render.yaml` and the `fromDatabase` entry under `envVars`, since `DATABASE_URL` is now set manually.
