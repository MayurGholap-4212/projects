# Task 3 – File Listener and Database Upload

## 📄 Overview

This module continuously monitors a folder (`uploads/`) for any new file and uploads its content into a local **SQLite** database. It dynamically handles different file types and structures.

---

## 📦 Supported File Types

- `.csv` → Loaded using `pandas.read_csv()`
- `.xls` / `.xlsx` → Loaded using `pandas.read_excel()`
- `.json` → Loaded using `pandas.read_json()`

> ❌ Other file types (e.g., `.pdf`, `.txt`, `.png`) are skipped automatically.

---

## 🗃️ Database

- Engine: **SQLite3**
- File: `database.db` (auto-created)
- Tables: One per file, using filename as the table name
- Table schema: Auto-generated based on file columns

---

## 🛠️ How to Run

**clone repo**

* git clone
* cd Task3_File_Listener_Upload

**Install dependencies**:

* pip install -r requirements.txt

 **Run the script** :

* python listener.py

**Drop files** into the `uploads/` directory:

* Each file triggers upload automatically
* Data is inserted into a uniquely named table

---

## ✅ Features

* 🚀 Real-time file monitoring with `watchdog`
* 🧠 Dynamic schema creation per file
* 🧾 Multi-format support: CSV, Excel, JSON
* 📂 Uses safe filenames as table names
* ⚠️ Error-handling for unsupported/broken files
* 🔄 Runs continuously until stopped

---

## 📂 Folder Structure

Task3_File_Listener_Upload/
├── uploads/              # Drop your files here
├── listener.py           # Main script
├── database.db           # SQLite DB
├── README.md             # This file

## 📝 Notes

* You can view or query the database using **DB Browser for SQLite** or with `pandas.read_sql()` in Python.
* Only valid and supported files are uploaded.

```python

```
