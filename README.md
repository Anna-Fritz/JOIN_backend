# JOIN Backend

## 📌 Project Description

JOIN Backend is a RESTful API service designed for the **JOIN Kanban Board** task management application. It provides endpoints for user authentication, task management, and data handling, ensuring smooth communication between the frontend and backend components.

---

## 🛠 Installation & Setup

### System Requirements

- **Python:** 3.13.1
- **Django:** 5.1.6
- **Django REST Framework:** 3.15.2

### Dependencies (from `requirements.txt`)

```
asgiref==3.8.1
Django==5.1.6
django-cors-headers==4.7.0
djangorestframework==3.15.2
djangorestframework_simplejwt==5.5.0
PyJWT==2.9.0
sqlparse==0.5.3
tzdata==2025.1
```

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository-url.git
   cd join-backend
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

5. Start the development server:
   ```sh
   python manage.py runserver
   ```

---

## 🌐 API Documentation

### Endpoints

- **User Management:**
  - `GET, POST /user/` → Retrieve all users or create a new user.
  - `GET /user/{id}/` → Retrieve a specific user.

- **Task Management:**
  - `GET, POST /task/` → Retrieve all tasks or create a new task.
  - `GET /task/{id}/` → Retrieve details of a specific task.

- **Subtask Management:**
  - `GET, POST /task/{id}/subtask/` → Retrieve or create subtasks for a task.
  - `GET /task/{task_id}/subtask/{id}/` → Retrieve details of a specific subtask.

- **Summary:**
  - `GET /summary/` → Retrieve an overview of tasks and subtasks.

- **Priority Management:**
  - `GET /prio/` → Retrieve a list of priorities.

- **Category Management:**
  - `GET /category/` → Retrieve a list of categories.

- **User Profiles:**
  - `GET, POST /profiles/` → Retrieve all user profiles or create a new one.
  - `GET /profiles/{id}/` → Retrieve details of a specific user profile.

- **Authentication:**
  - `POST /registration/` → Register a new user.
  - `POST /login/` → Log in and receive authentication tokens.
  - `POST /login/refresh/` → Refresh the authentication token.
  - `POST /logout/` → Log out the current user.

### Authentication
- Uses **JWT (JSON Web Tokens)** for authentication.
- **Access Token** and **Refresh Token** implementation for secure session management.

---

## 📂 Database & Migrations

- **Database Technology:** SQLite (default, can be switched to PostgreSQL or MySQL if needed).
- **Run Migrations:**
  ```sh
  python manage.py migrate
  ```

---

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

- **Share:** You may copy and redistribute the material in any format or medium.
- **Adapt:** You may remix, transform, and build upon the material.
- **Non-Commercial:** You may not use the material for commercial purposes.

For full details, see the [official license documentation](https://creativecommons.org/licenses/by-nc/4.0/).

---

## 👩‍💻 Author

Developed and maintained by [Anna](https://github.com/Anna-Fritz).

For questions, feedback, or contributions, feel free to open an issue or submit a pull request on GitHub.
