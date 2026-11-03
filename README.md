# Campus Services & Accessibility Finder

## Overview

Campus Services & Accessibility Finder is a location-based web application created for the Location-Based Services module.

The application focuses on the TU Dublin Grangegorman campus. It helps users explore campus buildings, services, routes and different campus areas on an interactive map.

The project demonstrates how Django, PostgreSQL/PostGIS, REST APIs, Leaflet and Docker can work together in one location-based application.

---

## Main Features

The application currently provides:

- Interactive Leaflet campus map
- OpenStreetMap base map
- Campus facilities displayed as points
- Campus routes displayed as lines
- Campus areas displayed as polygons
- Facility information shown in map popups
- Place filtering by category
- Accessibility filtering
- Nearest facility search
- Search for facilities within a radius
- Point-in-polygon search
- Route and zone intersection search
- Layer controls
- Responsive Bootstrap interface
- RESTful GeoJSON API
- Full CRUD support
- Input validation and error handling
- Docker-based local deployment
- PostgreSQL/PostGIS spatial database
- Automated API tests

---

## Technology Stack

### Backend

- Python
- Django
- GeoDjango
- Django REST Framework
- Django REST Framework GIS

### Database

- PostgreSQL
- PostGIS

### Frontend

- HTML5
- CSS
- JavaScript
- Bootstrap 5
- Leaflet JS
- OpenStreetMap

### Deployment and Development

- Docker
- Docker Compose
- pgAdmin
- Git
- GitHub

---

## Application Architecture

The application uses a simple multi-layer architecture.

```text
Browser
   |
   | HTTP
   v
Django Web Application
   |
   | REST / GeoJSON
   v
Django REST Framework
   |
   | GeoDjango
   v
PostgreSQL + PostGIS
   |
   v
Persistent Docker Volume
```

Leaflet is used in the browser to display the spatial data returned by the REST API.

The application runs using Docker Compose.

The main Docker services are:

- `web` - Django application
- `db` - PostgreSQL/PostGIS database
- `pgadmin` - database management interface

All services communicate through a custom Docker network.

---

## Database Design

The application uses three main spatial models.

### Place

A Place represents a campus building or service.

Examples include:

- Academic Hub and Library
- Central Quad
- East Quad
- Rathdown House
- Glassmanogue Gym
- Student Health Centre

Spatial type:

```text
POINT
```

Main fields include:

- name
- description
- category
- location
- opening hours
- accessibility status

---

### Route

A Route represents a walking, cycling or accessible route through the campus.

Spatial type:

```text
LINESTRING
```

Main fields include:

- name
- description
- route type
- path
- distance
- accessibility status

---

### Zone

A Zone represents an area of the campus.

Examples include:

- Main Campus
- Academic Core
- Sports Area
- South Campus

Spatial type:

```text
POLYGON
```

Main fields include:

- name
- description
- zone type
- boundary

---

## Coordinate System

All spatial data uses:

```text
EPSG:4326
```

This is the standard WGS 84 coordinate system used for latitude and longitude.

---

## Spatial Indexes

Spatial columns use PostGIS GiST indexes.

Indexes are created for:

```text
Place.location
Route.path
Zone.boundary
```

These indexes help PostgreSQL process spatial searches more efficiently.

---

## Spatial Queries

The application contains four main spatial operations.

### 1. Nearest Place Search

This query finds the closest campus facilities to a selected location.

Example:

```text
/api/places/nearest/?lat=53.3552&lng=-6.2795&limit=5
```

The application calculates the distance between the selected point and campus facilities.

Results are ordered from nearest to furthest.

---

### 2. Radius Search

This query finds facilities within a selected distance.

Example:

```text
/api/places/within-radius/?lat=53.3552&lng=-6.2795&radius=500
```

For example, a user can find all campus facilities within 500 metres.

The radius is also displayed visually on the Leaflet map.

---

### 3. Point-in-Polygon Search

This query finds which campus zone contains a selected location.

Example:

```text
/api/zones/contains-point/?lat=53.3550&lng=-6.2800
```

This uses a point and polygon spatial relationship.

---

### 4. Route and Zone Intersection

This query finds routes that cross a selected campus zone.

Example:

```text
/api/routes/intersecting-zone/?zone_id=1
```

This uses PostGIS spatial intersection between a LineString and a Polygon.

---

## REST API

The project provides RESTful API endpoints for all main spatial objects.

### Places

```text
GET    /api/places/
POST   /api/places/
GET    /api/places/{id}/
PUT    /api/places/{id}/
PATCH  /api/places/{id}/
DELETE /api/places/{id}/
```

### Routes

```text
GET    /api/routes/
POST   /api/routes/
GET    /api/routes/{id}/
PUT    /api/routes/{id}/
PATCH  /api/routes/{id}/
DELETE /api/routes/{id}/
```

### Zones

```text
GET    /api/zones/
POST   /api/zones/
GET    /api/zones/{id}/
PUT    /api/zones/{id}/
PATCH  /api/zones/{id}/
DELETE /api/zones/{id}/
```

---

## Filtering

Places can be filtered by category.

Example:

```text
/api/places/?category=academic
```

Accessible facilities can also be filtered.

Example:

```text
/api/places/?is_accessible=true
```

Routes can be filtered by route type.

Example:

```text
/api/routes/?route_type=walking
```

Zones can be filtered by zone type.

Example:

```text
/api/zones/?zone_type=campus
```

---

## Validation and Error Handling

The API checks user input before running spatial queries.

The application validates:

- latitude
- longitude
- radius values
- result limits
- required parameters
- zone IDs

For example, latitude must be between:

```text
-90 and 90
```

Longitude must be between:

```text
-180 and 180
```

Invalid requests return suitable HTTP responses such as:

```text
400 Bad Request
404 Not Found
```

This prevents invalid spatial queries from being sent to the database.

---

## Campus Data

The project originally used a small synthetic dataset during development.

The dataset was later improved to represent the TU Dublin Grangegorman campus more realistically.

The application includes buildings and facilities such as:

- Academic Hub and Library
- Central Quad
- East Quad
- Lower House
- Rathdown House
- Greenway Hub
- National Optometry Centre
- Glassmanogue Gym
- St. Laurence
- Clocktower
- Park House
- Training Restaurants

The building and facility names are based on TU Dublin campus information.

The coordinates, routes and polygon boundaries used in this academic project are approximate. They were manually positioned to represent the campus layout and demonstrate PostGIS functionality.

The application should not be used as an official navigation system.

---

## Project Structure

```text
campus_lbs/
│
├── api/
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── campus_lbs/
│   ├── settings.py
│   └── urls.py
│
├── dashboard/
│   ├── templates/
│   │   └── dashboard/
│   │       └── index.html
│   ├── urls.py
│   └── views.py
│
├── places/
│   ├── management/
│   │   └── commands/
│   │       └── populate_campus_data.py
│   ├── migrations/
│   ├── admin.py
│   └── models.py
│
├── routes/
│   ├── migrations/
│   ├── admin.py
│   └── models.py
│
├── zones/
│   ├── migrations/
│   ├── admin.py
│   └── models.py
│
├── static/
│   ├── css/
│   │   └── app.css
│   └── js/
│       └── map.js
│
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── manage.py
├── README.md
└── requirements.txt
```

---

## Environment Configuration

The application uses environment variables.

The real `.env` file is not stored in GitHub.

An example file is provided:

```text
.env.example
```

Copy it before starting the project.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then update the values inside `.env`.

Example variables include:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DATABASE_HOST
DATABASE_PORT
DJANGO_SECRET_KEY
DJANGO_DEBUG
```

Never upload real passwords or secret keys to GitHub.

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/BohdanYe/campus-lbs-assignment.git
```

Move into the project:

```bash
cd campus-lbs-assignment
```

---

### 2. Create the environment file

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and provide local development values.

---

### 3. Build Docker images

```powershell
docker compose build
```

---

### 4. Start the database

```powershell
docker compose up -d db pgadmin
```

Check the services:

```powershell
docker compose ps
```

The database should report:

```text
healthy
```

---

### 5. Apply database migrations

```powershell
docker compose run --rm web python manage.py migrate
```

---

### 6. Load campus sample data

```powershell
docker compose run --rm web python manage.py populate_campus_data --clear
```

---

### 7. Start the application

```powershell
docker compose up -d
```

---

### 8. Open the application

Main application:

```text
http://localhost:8000/
```

Django REST API:

```text
http://localhost:8000/api/places/
```

Django administration:

```text
http://localhost:8000/admin/
```

pgAdmin:

```text
http://localhost:5050/
```

---

## Running Tests

The project contains automated tests for the REST API and spatial functions.

Run:

```powershell
docker compose exec web python manage.py test
```

The current test suite checks:

- Places endpoint
- Routes endpoint
- Zones endpoint
- Nearest place search
- Radius search
- Point-in-polygon search
- Route and polygon intersection
- Invalid latitude handling
- Missing coordinate handling
- Invalid radius handling
- Missing zone handling

A successful test run should finish with:

```text
OK
```

---

## Using the Application

### View Campus Data

When the application opens, the map displays:

- campus facilities
- campus routes
- campus zones

Users can switch individual layers on or off.

---

### View Facility Information

Click a facility marker.

The popup shows information such as:

- facility name
- category
- opening hours
- accessibility
- description

---

### Filter Facilities

Use the category filter to display a selected type of facility.

For example:

```text
Academic Building
Library
Sports Facility
Health Service
Student Services
```

The accessibility option can be used to display accessible facilities only.

---

### Find Nearby Facilities

Click a location on the map.

The selected latitude and longitude are automatically added to the search form.

Click:

```text
Find Nearest Places
```

The application will show the closest facilities and their distances.

---

### Search Within a Radius

Choose a point on the map.

Enter a radius in metres.

Click:

```text
Search Within Radius
```

The application displays a search circle and highlights matching facilities.

---

### Find a Campus Zone

Choose a location on the map.

Click:

```text
Find Containing Zone
```

The application highlights all campus zones containing the selected point.

---

### Find Routes Through a Zone

Choose a campus zone.

Click:

```text
Find Routes Through Zone
```

The application highlights the routes that intersect the selected polygon.

---

## Docker Persistence

PostgreSQL data is stored in a Docker volume.

This means the data remains available after:

```powershell
docker compose down
```

and:

```powershell
docker compose up -d
```

Do not use:

```powershell
docker compose down -v
```

unless you intentionally want to remove the database volume.

---

## Security

The project follows basic security practices suitable for local academic development.

These include:

- secrets stored in `.env`
- `.env` excluded from Git
- `.env.example` uses placeholder values
- database passwords are not hard-coded
- Django secret key is loaded from environment variables
- API input is validated
- errors return suitable HTTP status codes
- Django configuration is separated from source-controlled secrets

The project is designed for local academic deployment and is not intended to be a production public service.

---

## Responsive Design

The interface uses Bootstrap 5.

It is designed to work on:

- desktop computers
- laptops
- tablets
- mobile devices

On smaller screens, the controls are displayed above the map so they remain easy to use.

---

## Known Limitations

This project has several limitations.

- Campus coordinates are approximate.
- Campus polygons are simplified.
- Routes are manually created and do not represent official navigation routes.
- Opening hours may change and are not updated automatically.
- The project does not provide live indoor navigation.
- The application is intended for academic demonstration.
- OpenStreetMap tiles require an internet connection.

---

## Future Improvements

Possible improvements include:

- official GIS building footprints
- real accessibility route data
- live campus opening hours
- indoor navigation
- user geolocation
- route planning between two campus buildings
- real-time service information
- searchable building codes
- authentication for editing spatial information
- more detailed accessibility information
- official campus transport data

---

## Testing and Development Process

The application was developed in several stages.

### Part 1

The first stage created:

- Docker environment
- PostgreSQL/PostGIS database
- Django project
- Point model
- LineString model
- Polygon model
- migrations
- spatial indexes

### Part 2

The second stage added:

- GeoJSON serializers
- REST API
- CRUD operations
- sample spatial data
- nearest search
- radius search
- containment search
- intersection search
- validation
- automated tests

### Part 3

The final stage added:

- responsive Bootstrap interface
- Leaflet map
- OpenStreetMap
- map layers
- popups
- filters
- interactive spatial searches
- visual search results
- improved Grangegorman campus data

---

## Author

**Bohdan Yeriemienko**

BSc Computer Science  
Technological University Dublin

Location-Based Services Assignment 1