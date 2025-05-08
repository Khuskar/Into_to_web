# 🐾 Resume Builder — Flask + SQLite

A lightweight web app that lets anyone build a résumé in minutes, preview it, and store the result as JSON in an SQLite database.


---


## Features

* **Responsive front-end** in vanilla HTML/CSS/JS—no external JS frameworks.
* **Save Résumé** → `POST /save` → stored as JSON (Create).
* **Dashboard** lists all saved résumés with View (JSON) and Delete buttons (Read + Delete).
* **Print-ready CV** via browser print dialog (`@media print` styles in `main.css`).
* Clean **Flask** backend with the built-in `sqlite3` module (no ORM required).
* Zero external services—runs completely offline.

---

## Tech Stack

| Layer     | Technology / Library                           | Why |
|-----------|------------------------------------------------|-----|
| Backend   | **Flask 3**                                    | Minimal routing, Jinja2 templating |
| Database  | **SQLite 3**                                   | Serverless, bundled with Python |
| Front-end | **HTML / CSS / JS / JQuery**                   | Matches course requirements |
| Styling   | Custom CSS + a few Bootstrap 5 utilities (CDN) | Fast responsive layout |


---

## Setup & Run (locally)

```bash
git clone --single-branch -b ResumeBuilder https://github.com/Khuskar/Into_to_web.git
cd resume-builder

# 1) create & activate virtualenv
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 2) install deps
pip install -r requirements.txt

# 3) launch development server
python app.py
# open http://127.0.0.1:5000/ in your browser


