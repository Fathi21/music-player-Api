# Django Backend API for Music Player App

This is the backend API for the Music Player App built with Django and Django REST Framework. It provides endpoints for user authentication, song management, playlists, likes, and search functionality.

## Features

- User registration, login, and JWT authentication  
- CRUD operations for songs, playlists, and likes  
- Support for CORS to enable frontend-backend communication  
- Image handling for album covers or song thumbnails  
- RESTful API design for easy integration with frontend  

## Tech Stack & Dependencies

- Python 3.x  
- Django 5.2.3  
- Django REST Framework 3.16.0  
- djangorestframework-simplejwt for JWT authentication  
- django-cors-headers to manage Cross-Origin Resource Sharing  
- django-colorfield for color fields in models (e.g., playlist colors)  
- Pillow for image processing  
- PyJWT for JSON Web Token handling  
- Additional tools: asgiref, packaging, sqlparse, pip-tools, setuptools, wheel  

## Getting Started

### Prerequisites

- Python 3.8 or later  
- pip package manager  

### Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/Fathi21/music-player-Api.git
   cd music-player-Api
