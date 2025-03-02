# :earth_africa: Globetrotter Challenge
An ultimate travel guessing game featuring cryptic clues and friend challenges.

Link: https://globetrotter-1786.up.railway.app/
## :rocket: Features
- 100+ destinations with clues/facts
- Real-time scoring system
- Friend challenge system with shareable links
- Responsive Bootstrap UI
- SQLite database with ORM
- FastAPI backend
## :gear: Tech Stack
**Backend:** 
`Python` `FastAPI` `SQLAlchemy` `Pydantic`

**Frontend:** 
`Bootstrap 5` `Vanilla JS` `HTML5`

**Database:** 
`SQLite`

**Deployment:**
`Railway`
## :hammer_and_wrench: Setup
1. Clone repo:
```bash
git clone https://github.com/Aman3786/globetrotter.git
cd globetrotter
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run server:
```bash
uvicorn main:app --reload
```
## :books: Documentation
**Endpoints** 

`GET /` - Game UI 

`GET /api/game` - Get new question 

`POST /api/verify/{id}` - Submit answer 

`POST /api/challenges` - Create challenge
## :round_pushpin: Design Choices
- **SQLite**: Simplified setup for rapid development
- **FastApi**: Python Web Framework for Rapid API Development and also provided OpenAPI Swagger documentation 
- **ORM**: SQLAlchemy for database abstraction
- **Stateless**: Session management via client-side JS
- **Bootstrap 5**: Quick UI development with responsive design
---
:closed_lock_with_key: **Note:** Dataset stored exclusively in backend database







