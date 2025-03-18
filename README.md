# Final Project Group H - Backend Side

## MarketPlace "Toko Edi Ya"

### TechStack

- **Python** with **Flask** as a framework backend
- **MySQL** for database using **SQLAlchemy** as ORM
- **Flask-JWT-Extended** for authentication with JSON Web Token (JWT)
- **Bcrypt** for password hashing and security
- **Python-dotenv** for managing environment variables 

### About "Toko Edi Ya" (TEY)
"Toko Edi Ya" is a web application designed to support users in:
- **Showcasing Creativity**: A platform for eco-conscious creators to showcase their sustainable handmade goods.
- **Rediscovering Value**: Buy and sell secondhand items in great condition.
- **Supporting Sustainability**: Promoting an environmentally friendly lifestyle through mindful shopping.
- **Embracing Sustainability**: Giving pre-loved items a new home and helping the planet.

**Join the TEY community today and explore a world of unique, meaningful items!**

### Toko Edi Ya – Where Every Item Finds Its Purpose.

---

## How to Deploy - Backend Side

✈To deploy the backend side of the project, follow these steps:

1. **Clone the Repository**
   - Clone the GitHub repository from [this link](https://github.com/GentaYuki/BACKEND-FSSEGROUPH).

2. **Install Dependencies**
   - Run the following command in the terminal:
     ```
     pip install -r requirements.txt
     ```

3. **Setup Environment Variables**
   - Create file `.env` in root project
      ```env
      DB_USERNAME = your_DB_user_name
      DB_PASSWORD = your_private_key
      DB_HOST     = your_Host
      DB_PORT     = your_DB_port
      DB_NAME     = your_DB_name
      ```

4. **Initialize the Database**
   - Run the following command to initialize the database:
     ```
     flask db init
     ```

5. **Create Migrations**
   - Run the following command to create an initial migration:
     ```
     flask db migrate -m "initial migration"
     ```

6. **Upgrade the Database**
   - Run the following command to apply the migrations:
     ```
     flask db upgrade
     ```

7. **Run the API**
   - Finally, run the API using the following command:
     ```
     flask run
     ```

---

By following these steps, you will successfully deploy the backend side of the "Toko Edi Ya" project.
