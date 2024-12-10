# RBAC System with FastAPI

This project is a Role-Based Access Control (RBAC) system implemented using FastAPI. It allows managing users, roles, and permissions and integrates with MySQL and Redis for data persistence and logging.


#### **Project Url**: https://rbac-project-ykdb.onrender.com
---

## **Features**
- Role and Permission Management
- API Key-based Authentication
- Access Control Validation
- Audit Logging
- Background task to move logs from Redis to MySQL at regular intervals

---

## **Prerequisites**
Before setting up the project, ensure you have the following installed and running:

1. **MySQL Database**
   - Install MySQL: [MySQL Installation Guide](https://dev.mysql.com/doc/refman/9.0/en/installing.html)
   - Create a database for the project.

2. **Redis**
   - Install Redis: [Redis Installation Guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
   - Ensure the Redis server is running.

3. **Python 3.10 or above**
   - Install Python: [Python Installation Guide](https://www.python.org/downloads/)

---

## **Setup Instructions**

### Step 1: Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Set Up a Virtual Environment

#### On Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup .env
```bash
cp .env.example .env
# Edit as required
```

### Step 5: Run the app
```bash
# For development
fastapi dev

# For prod
uvicorn main:app
```

### Step 6: Create users and permissions
- By default, the roles table will be populated with predefined roles.
- Create users and permissions as required.

---

## **Documentation**

- Swagger UI: http://127.0.0.1:8000/docs
- Postman Collection: https://www.postman.com/security-pilot-16480615/projects/documentation/khm371k/rbac-project

---

## **Notes**

- The API uses API key for auth on endpoints that require validation (All endpoints in access validation collection and the endpoint to assign permission to a role).
- We can improve various aspects of the project such as salting and hashing API keys or using JWT for auth, caching frequently used values in redis