# CarCraft: Automotive Inventory & Dealership Suite

**CarCraft** is an enterprise-grade full-stack automotive dealership web suite built with **Python 3**, **Django 5.x**, **MySQL 8+**, and **Bootstrap 5** with custom automotive showroom & precision workshop styling.

---

## 🏎️ Core Modules & Architecture

The application is structured into three cohesive Django apps under a centralized dealership command center:

```
HCL_Project/
├── carcraft/                  # Project configuration, settings & root URLs
├── inventory/                 # Vehicle Inventory & Showroom Management
│   ├── management/commands/   # Demo seeding script (seed_carcraft.py)
│   ├── models.py              # Vehicle & VehicleImage models
│   ├── views.py               # Inventory filtering, CRUD & quick status change
│   └── forms.py               # Vehicle forms & validation
├── store/                     # Parts & Accessories E-Commerce
│   ├── cart.py                # Session-based shopping cart engine
│   ├── models.py              # Category, Part, Order & OrderItem
│   ├── views.py               # Catalog, instant cart, atomic checkout & invoice
│   └── forms.py               # Checkout and catalog forms
├── service/                   # Service Appointment Scheduling & Bay Board
│   ├── models.py              # ServiceBay & Appointment
│   ├── views.py               # Live Bay Board matrix, booking & conflict engine
│   └── forms.py               # Appointment booking & capacity validator
├── static/                    # Custom CSS, typography & interactive JS
│   ├── css/carcraft.css       # Showroom & workshop automotive theme
│   └── js/carcraft.js         # Dynamic cart sidebar, live bay checker, gallery
├── templates/                 # Responsive HTML templates with Bootstrap 5
│   ├── base.html
│   ├── home.html
│   ├── inventory/
│   ├── store/
│   └── service/
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── manage.py
```

### 1. 🚙 Vehicle Inventory (`inventory`)
- **Vehicle Model**: VIN (17-char unique index), year, make, model, trim, body type (Sedan, SUV, Truck, Coupe, EV, Convertible, Wagon), status (`available`, `pending`, `sold`), mileage, price, powertrain (Gasoline, Electric, Hybrid, Diesel), transmission, horsepower, and high-res imagery.
- **Showroom Catalog**: Full-text search by Make/Model/VIN/Trim, filter by Body Type and Status, and sort by Price/Mileage/Year.
- **VIN-Plate Visual Identity**: Metallic stamped header strip with monospace VIN tag and instant copy tool.
- **Quick Status Actions**: 1-click AJAX / POST toggle between `Available`, `Pending`, and `Sold` without leaving the listing.
- **Full Spec Sheet & Photo Gallery**: Interactive thumbnail switcher and 1-click shortcut to schedule service for any inventory vehicle.

### 2. ⚙️ Parts & Accessories E-Commerce (`store`)
- **Parts Catalog**: Categorized performance catalog (Braking Systems, Titanium Exhausts, Forged Wheels & Suspension, Intakes & ECU Tunes, Carbon Aero, EV Charging).
- **Session-Based Cart**: Fast session cart supporting real-time add, quantity adjustments, tax calculations, free shipping thresholds, and a sticky drawer.
- **Atomic Checkout Flow**: Validates item availability in a database transaction (`transaction.atomic()`), creates `Order` + `OrderItem` records, and automatically decrements stock.
- **Order Tracking & Invoicing**: Formatted printable invoice receipts and search by order number or customer email.

### 3. 🔧 Service Appointment Scheduling (`service`)
- **Service Bay Board Matrix**: Live timeline view displaying active workshop bays (e.g. Dyno Lab, Laser Alignment, Heavy Mechanical, High-Voltage EV Bay) across 6 daily time slots (08:00 AM to 05:30 PM).
- **Automated Bay Allocation & Conflict Engine**: Automatically assigns the next free lift bay for a selected date and slot. Prevents double-booking and alerts when bay capacity is reached.
- **Workshop Job Tickets**: Color-coded tickets with technician remarks, lift observation logs, and stage transitions (`Scheduled` → `In Progress / On Lift` → `Completed / Ready for Pickup`).

---

## 🎨 UI/UX Design Direction

- **Showroom & Workshop Aesthetic**: Deep carbon/obsidian base (`#090c12`, `#151c2a`), gunmetal card surfaces (`#192233`), and **Apex Amber** (`#f59e0b`) & **Electric Cyan** (`#06b6d4`) accents.
- **Typography**: Paired Google Fonts (`Chakra Petch` for technical headings, `Plus Jakarta Sans` for body typography, and `JetBrains Mono` for VINs, SKUs, and bay slots).
- **Accessible & Responsive**: Keyboard focus outlines (`:focus-visible`), responsive layouts down to mobile viewports, custom forms, switch toggles, and modals.

---

## 🚀 Setup & Installation Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- MySQL 8.0+ (or Docker for running MySQL 8)

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone <repository_url>
cd HCL_Project

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database (MySQL 8)

#### Option A: Quick MySQL via Docker (Recommended)
```bash
docker run -d \
  --name carcraft-mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=carcraftroot \
  -e MYSQL_DATABASE=carcraft \
  -e MYSQL_USER=carcraft_user \
  -e MYSQL_PASSWORD=carcraftpass \
  mysql:8.0
```

#### Option B: Native MySQL Server
Log into your MySQL terminal:
```sql
CREATE DATABASE carcraft CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'carcraft_user'@'%' IDENTIFIED BY 'carcraftpass';
GRANT ALL PRIVILEGES ON carcraft.* TO 'carcraft_user'@'%';
GRANT ALL PRIVILEGES ON test_carcraft.* TO 'carcraft_user'@'%';
FLUSH PRIVILEGES;
```

### Step 4: Environment Variables (`.env`)
Create a `.env` file in the project root (defaults are provided in `.env.example`):
```ini
SECRET_KEY=carcraft-production-grade-key-9948271649281
DEBUG=True
ALLOWED_HOSTS=*

# MySQL Database Settings
DB_NAME=carcraft
DB_USER=carcraft_user
DB_PASSWORD=carcraftpass
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Seed Realistic Demo Data
Populate the database with 10+ vehicles, 12+ performance parts, 4 service bays, and scheduled appointments across today and upcoming days:
```bash
python manage.py seed_carcraft
```
> **Default Admin Credentials**: Username: `admin` | Password: `admin123`

### Step 7: Run Automated Test Suite
```bash
python manage.py test
```

### Step 8: Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```
Open your browser and navigate to:
- **Dealership Command Center**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Vehicle Inventory**: [http://127.0.0.1:8000/inventory/](http://127.0.0.1:8000/inventory/)
- **Parts Store**: [http://127.0.0.1:8000/store/](http://127.0.0.1:8000/store/)
- **Workshop Bay Board**: [http://127.0.0.1:8000/service/](http://127.0.0.1:8000/service/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Testing Verification & MySQL Confirmation
All test cases run directly against the live MySQL 8 database instance:
- `inventory.tests.VehicleModelTests`: Tests vehicle properties, filtering, search, and AJAX status mutations.
- `store.tests.StoreAndCartTests`: Tests session cart additions, tax/shipping logic, checkout transaction, and inventory stock decrements.
- `service.tests.ServiceAppointmentTests`: Tests automated bay assignment, conflict checking when bay capacity is reached, and the bay board calendar.
