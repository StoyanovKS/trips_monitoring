# Documentation for Trips Monitoring django web application

## 1. Project overview
A Django web application for tracking trips, refueling events, and fuel-related costs for vehicles.
The project provides insights into vehicle usage, fuel consumption, and monthly aggregated statistics per vehicle.
It is suitable for personal use or as a foundation for a small car fleet.

Major project goals are summarised as follows:
- Track trips and mileage accurately;
- Monitor fuel consumption and refueling costs;
- Provide monthly summaries and aggregated statistics per vehicle;
- Improve cost awareness and expense analysis for personal or business car usage;

---

## 2. Technology stack used
- Backend: Python, Django;
- Database: PostgreSQL;
- Background Tasking: Celery and Redis;
- Deployment: Azure App Service;

---
## 3. Features overview

### 3.1. User Authentication
- User registration and login;
- Role-based behavior;

The application defines two user groups (Driver, Manager) in the Django Admin panel. Role assignment is handled **exclusively by administrators** through the Django Admin panel to prevent privilege escalation.

The application defines two user roles:

- **Driver** (default role);
- **Manager**;

Users do **not** select their role during registration.

In the current educational version:
- Drivers can access and manage **only their own cars and trips**;
- Managers have **read access** to data across users via API.;



### 3.2. Garage Management
- Add and manage vehicles;
- Track mileage per car;
- Optionality to add vehicle metadata such as car`s vin or photo;

### 3.3. Trips
- Create trips with start and end odometer values;
- Start/end dates and locations;
- Distance calculation;
- Assign predefined tags;


### 3.4. Refuels
- Register refueling;
- Track fuel type, quantity, total cost, and station;
- Linkage between refuels with a particular car;


### 3.5. Reports
- Aggregated statistics per **month** and **vehicle**;
- Reporting of aggregated data for number of trips, distance covered, fuel consumption;

The application uses Celery for asynchronous background processing of monthly statistics. Instead of calculating heavy aggregates on every request, monthly data is precomputed and stored in a dedicated model (MonthlyCarStat).

Fuel cost totals in the monthly report are normalized to EUR using a fixed exchange rate: 1 EUR = 1.95583 BGN.

If refuels are entered in mixed currencies, the report displays separate rows per currency, while the Total row is always shown in EUR.

### 3.6. Tags
The project uses **predefined Tags** for:
- Cars;
- Trips;

They must be created in advance by a **superuser (admin)** using Django Admin to ensure consistency in the categorization and normalized data. If no tags exist yet, the tags selector will be empty.

### 3.7. REST API 

The project exposes a REST API built with Django REST Framework. The API is designed as a read-only data access layer intended for external systems, dashboards, or integrations. API requests require an authenticated user.

---

## 4. Local set-up

### 4.1. Clone the repository

```bash
git clone https://github.com/StoyanovKS/trips_monitoring.git
cd trips_monitoring
```

### 4.2. Create and activate virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4.3. Install dependencies from the requirements.txt

```bash
pip install -r requirements.txt
```

### 4.4. Configuration of `.env` file

Create a `.env` file in the project root directory.

The file **shall contain**:

```env
DJANGO_SETTINGS_MODULE=config.settings.dev
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost

DB_NAME=your_database_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=disable

REDIS_URL=redis://localhost:6379/0
```

### 4.5. Postgres database setup

- Ensure PostgreSQL database is running locally;
- Create the database;
- Apply migrations: 

```bash
python manage.py migrate
```

- Create admin user:

```bash
python manage.py createsuperuser
```

### 4.6. Run the project locally

```bash
python manage.py runserver
```

### 4.7. Open on localhost

```bash
http://127.0.0.1:8000/
```

### 4.8. Tags creation


Use the already created **admin user**.

- Open Django admin panel:
  http://127.0.0.1:8000/admin/

- Navigate to:
  Logbook → Tags → Add

- Create the following tags:
  - Highway
  - Inner-city
  - Vacation
  - Business trip

Once created, users can select tags from checkboxes in the UI.

### 4.9. Automated testing


```bash
python manage.py test
```

Upon completion you have to see the following message: All automated tests pass successfully.

### 4.10. Background tasks

- Start Redis as a docker image;
- Run a worker:

```bash
celery -A config worker -l info
```

### 4.11. Production deployment

The application can be deployed on Azure App Service with a PostgreSQL database.

Production configuration is handled via Azure App Service environment settings.
Sensitive values are not stored in the repository.

Live application URL:
https://tripsmonitoring-fcbsc9g5hpbpb4fr.italynorth-01.azurewebsites.net/


#### 4.11.1. Required Azure App Settings (Secrets)

The following environment variables must be configured in Azure App Service:

- `DJANGO_SECRET_KEY`
- `DEBUG` (set to `False` in production)
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

#### 4.11.2. Database settings
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

#### 4.11.3. GitHub Actions Secrets

To enable CI/CD deployment, configure the following repository secrets:

- `AZUREAPPSERVICE_CLIENTID`
- `AZUREAPPSERVICE_TENANTID`
- `AZUREAPPSERVICE_SUBSCRIPTIONID`

#### 4.11.4. Media Storage (Azure Blob Storage)

Uploaded car photos (media files) are stored in Azure Blob Storage in production.
Create a Storage Account and a blob container (e.g. media) and configure the following App Service environment variables:

AZURE_ACCOUNT_NAME (Storage Account name)

AZURE_ACCOUNT_KEY (Access key)

AZURE_MEDIA_CONTAINER (container name, default: media)

Important:

The blob container should allow public read access (anonymous blob access), otherwise images will not render in the browser.

