# Product-Tracking-System

## Overview

Product-Tracking-System is a web application designed for Product Line Managers (PLM) and regional merchandisers in the APAC region to manage and track regional footwear products. The platform enables collaborative management of product attributes, manual input of key details, and order tracking, ensuring data integrity and streamlined workflows.

## Features

- **Dashboard:** Centralized dashboard for PLMs, designers, developers, and stakeholders to manage products.
- **Product Management:** Create and edit articles (e.g., shoes, t-shirts) with attributes such as age group, gender, cut type, sole type, article group, retail price, factory cost, target cost, and gross margin.
- **Manual Input:** PLMs can manually input specific details like factory costs.
- **Order Tracking:** Regional merchandisers can input and track orders for their products.
- **Role-Based Access:** Secure access for different user roles.

## System Architecture

- **Frontend:** React (`client/`)
- **Backend API:** Flask (`server/`)
- **Dashboard:** Dash (`dash/`)
- **Database:** MySQL
- **API:** RESTful endpoints for data operations

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm
- MySQL server

### Database Setup

1. Ensure MySQL is running and create a database named `product_tracking_db`.
2. Update the database credentials in `server/server.py` if needed.
3. The database tables and seed data are automatically created when running the backend.

### Backend Setup (Flask API)

```bash
cd server
pip install flask flask-cors mysql-connector-python
python server.py
```

### Frontend Setup (React)

```bash
cd client
npm install
npm start
```

### Dashboard Setup (Dash)

```bash
cd dash
pip install dash dash-bootstrap-components pandas requests
python app.py
```

## API Endpoints

- `/get_shoe`, `/add_shoe`, `/update_shoe/<id>`, `/delete_shoe/<id>`
- `/get_clothing`, `/add_clothing`, `/update_clothing/<id>`, `/delete_clothing/<id>`
- `/get_accessory`, `/add_accessory`, `/update_accessory/<id>`, `/delete_accessory/<id>`
- `/get_merchandisers`, `/add_merchandiser`, `/update_merchandiser/<id>`, `/delete_merchandiser/<id>`
- `/get_orders`, `/add_order`, `/update_order/<id>`, `/delete_order/<id>`
- `/get_shoe_sale`, `/get_clothing_sale`, `/get_accessory_sale`

## Usage

1. Start the backend server (`server/server.py`).
2. Start the frontend React app (`client/`).
3. Optionally, start the Dash dashboard (`dash/app.py`).
4. Access the React app at `http://localhost:3000`.

## License

[MIT](LICENSE)