# AI Facebook Content System (AI-FCS)

AI-FCS is an automated backend platform built with **Django**, **Django REST Framework (DRF)**, and **CrewAI** designed to manage brands, campaigns, and generate AI-powered social media content and images.

---

## 🚀 Features

*   **RESTful API Backend**: Fully functional endpoints for managing Brands, Campaigns, and Content Posts.
*   **AI Agent Pipeline (CrewAI)**: Automated agents that collaborate to design context-aware content and descriptive image prompts.
*   **Custom AI Tool Integration**: Securely integrates custom tools (`GenerateImageTool`) to interface with generative AI services.
*   **PostgreSQL & Schema Isolation**: Configured for robust database management using PostgreSQL with custom schema support.

---

## 🛠️ Tech Stack

*   **Backend**: Python 3.12, Django 6.1, Django REST Framework
*   **AI Orchestration**: CrewAI
*   **Database**: PostgreSQL
*   **Environment Management**: python-decouple

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/AI-FCS.git](https://github.com/YourUsername/AI-FCS.git)
cd AI-FCS
