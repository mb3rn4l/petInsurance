# Pet Insurance App

This project is divided into two main layers:
1. **Backend:** Built with Django and Django REST Framework (DRF), responsible for managing business logic, claims, pets, and authentication.
2. **Frontend:** Built with Vue 3 and Vite, which consumes the API services.

---

## Recommended Method: Docker Compose

The easiest and most resilient way to raise both environments in an integrated manner is by using Docker Compose. All dependencies, environment configurations, Python and Node.js packages will be installed and orchestrated automatically.

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) installed and running.

### Execution Instructions
1. Open a terminal in the root of the project (where the `docker-compose.yml` file is located).
2. Run the following command to build all images and hook up the services:
   ```bash
   docker-compose up --build
   ```
3. Once the containers are up, the project will be active in your browsers:
   - **🖥️ Frontend App:** http://localhost:5173
   - **⚙️ Backend API Base:** http://localhost:8000/api/
   - **📖 Swagger UI (Interactive Doc):** http://localhost:8000/api/docs/

*To stop the execution safely in the future, press `Ctrl + C` in your terminal or run `docker-compose down`.*

---

## Manual Execution (Independent Local Development)

If you prefer to work separately or do not have Docker installed, run the services manually in different command windows.

### 1. Start the Backend (Django)

**Prerequisites:** Python 3.10+ installed.

1. Open your terminal and go to the backend route:
   ```bash
   cd backend
   ```
2. Create a virtual environment to isolate the libraries:
   ```bash
   python -m venv venv
   ```
3. Activate your virtual environment:
   - **On Windows:** `.\venv\Scripts\activate`
   - **On macOS/Linux:** `source venv/bin/activate`
4. Install all dependencies of the Django and testing ecosystem:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the migrations to initialize the base database structure (SQLite):
   ```bash
   python manage.py migrate
   ```
6. Start the primary server of the application:
   ```bash
   python manage.py runserver
   ```
   *The server should be listening for local requests through port `8000`.*

👉 **Run Unit Tests**  
Within this same backend virtual environment, you can automate and audit the code by simply writing:  
```bash
pytest
```
*This will look for the TDD logic programmed in `models`, `serializers`, and `views`, validating success and error cases.*

---

---

## 🗄️ Database Management (Migrations)

If you make changes to the data models or need to initialize the database from scratch, use the following commands depending on your environment:

### A. If you use Docker Compose (Recommended)
Run these commands in a separate terminal while the containers are active:

*   **Apply pending migrations:**
    ```bash
    docker-compose exec backend python manage.py migrate
    ```
*   **Create new migrations (after changes in models.py):**
    ```bash
    docker-compose exec backend python manage.py makemigrations
    ```

### B.If you use Manual Execution (venv)
Make sure you are in the `backend` folder and with the virtual environment enabled:

*   **Apply migrations:**
    ```bash
    python manage.py migrate
    ```
*   **Create new migrations:**
    ```bash
    python manage.py makemigrations
    ```

---

### 2. Start the Frontend (Vue 3 + Vite)

**Prerequisites:** Node.js v18+ installed.

1. Open a **new window/tab** in your terminal and go to the frontend system route:
   ```bash
   cd frontend
   ```
2. Download the local JS modules:
   ```bash
   npm install
   ```
3. Initialize the hot development cycle:
   ```bash
   npm run dev
   ```
   *The environment will give you a route that usually starts interactively at `http://localhost:5173`.*

---

## API Documentation (Swagger UI)

The main engine is natively enriched with OpenAPI 3 under the `drf-spectacular` library. You can experiment with all the routes and perform direct tests to the API from the comfortable generated graphical interface, without needing to connect using third-party systems or *Postman*.

As soon as you are running the backend, visualize all your integrations by connecting the browser to: `http://localhost:8000/api/docs/`
