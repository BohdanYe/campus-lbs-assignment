# Campus Services & Accessibility Finder

## Overview

Campus Services & Accessibility Finder is a location-based services application developed for the Location-Based Services module.

The application helps users explore campus facilities, walking routes, and different campus zones using an interactive spatial web application.

## Current Features

- PostgreSQL with PostGIS
- Django web application
- Docker Compose deployment
- Spatial Point data for campus facilities
- Spatial LineString data for routes
- Spatial Polygon data for zones
- Spatial GiST indexes
- Django administration interface

## Planned Features

- CRUD REST API
- Nearest facility search
- Radius search
- Point-in-polygon search
- Route and zone intersection search
- Interactive Leaflet map
- Responsive Bootstrap interface

## Technology Stack

- Python
- Django
- Django REST Framework
- GeoDjango
- PostgreSQL
- PostGIS
- Leaflet
- Bootstrap 5
- Docker
- Docker Compose
- pgAdmin

## Spatial Data Model

### Place
Geometry: Point

Represents campus facilities such as libraries, cafes, study areas, printers, and bicycle parking.

### Route
Geometry: LineString

Represents walking, cycling, and accessible routes.

### Zone
Geometry: Polygon

Represents campus boundaries, pedestrian areas, study areas, accessible zones, and green spaces.

## Development Status

Part 1 completed:

- Docker environment
- PostGIS database
- Django project
- Spatial models
- Database migrations
- Spatial indexes

## REST API

The application provides RESTful CRUD endpoints for all spatial entities.

### Places

- `GET /api/places/`
- `POST /api/places/`
- `GET /api/places/{id}/`
- `PUT /api/places/{id}/`
- `PATCH /api/places/{id}/`
- `DELETE /api/places/{id}/`

### Routes

- `GET /api/routes/`
- `POST /api/routes/`
- `GET /api/routes/{id}/`
- `PUT /api/routes/{id}/`
- `PATCH /api/routes/{id}/`
- `DELETE /api/routes/{id}/`

### Zones

- `GET /api/zones/`
- `POST /api/zones/`
- `GET /api/zones/{id}/`
- `PUT /api/zones/{id}/`
- `PATCH /api/zones/{id}/`
- `DELETE /api/zones/{id}/`

## Spatial Queries

### 1. Nearest Place Search

Finds the closest campus facilities to a supplied point.

Example:

```text
/api/places/nearest/?lat=53.3552&lng=-6.2795&limit=5

### 2. Radius Search
Finds campus facilities within a specified radius.

Example:
/api/places/within-radius/?lat=53.3552&lng=-6.2795&radius=500

### 3. Point-in-Polygon Search
Determines which campus zones contain a selected location.

Example:
/api/zones/contains-point/?lat=53.3550&lng=-6.2800

### 4. Spatial Intersection
Finds routes that intersect a selected campus zone.

Example:
/api/routes/intersecting-zone/?zone_id=1