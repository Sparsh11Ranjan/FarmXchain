# FarmXchain


**FarmXchain** is a backend-powered agricultural marketplace platform aimed at transforming how farmers and buyers connect. Focused on building a robust and scalable server-side system, the platform enables features like farmer registration, profile management, product listings, and buyer interactions. The backend ensures secure authentication, efficient data handling, and smooth API integration to support seamless user experiences. By strengthening the core infrastructure, FarmConnect supports a smarter, more connected agricultural ecosystem that empowers rural communities and streamlines marketplace interactions.

## Features

- **Secure Authentication:** Clerk-based signup and login (email/password, social logins)
- **Farmer Management:** Register, view, edit, and delete farmer profiles
- **Product Marketplace:** List, browse, and purchase agricultural products
- **Farming Types:** Manage and categorize farming types
- **Audit Logging:** Automatic tracking of key actions (insert, update, delete)
- **Responsive UI:** Modern, mobile-friendly interface with Shadcn UI and Tailwind CSS

---

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-CORS
- **Database:** MySQL
- **Authentication:** Clerk

---

## Project Structure

```

FarmXchain/
├── backend/       # Flask API (REST endpoints)
├── database/      # SQL scripts, migrations
└── README.md
```

---
## Database Schema

**Main Tables:**
- `register`: Farmer details
- `farming`: Farming types
- `addagroproducts`: Product listings
- `trig`: Audit logs

> **Note:** No `user` table is needed; Clerk handles user authentication.

**ERD Overview:**
```
register (rid PK) -- farming (fid PK)
register (farmername) --< addagroproducts (username)
```
## 👩‍💻 Author

Developed with ❤️ by **Sparsh Ranjan**  
📫 Connect with me on [LinkedIn](https://www.linkedin.com/in/sparsh-ranjan-b57514289?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---
---
