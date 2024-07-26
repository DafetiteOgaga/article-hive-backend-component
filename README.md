# Article Hive

Welcome to **Article Hive**, a dynamic platform where users can read articles and explore author profiles, while authors can create and manage their own content. Built with a robust architecture leveraging modern web technologies, Article Hive aims to provide a seamless experience for both readers and writers.

**Click [Article Hive](https://dafetite.pythonanywhere.com) to visit the Web Application live**

**Click [here](https://dafetite.pythonanywhere.com) to read about Article Hive**

## Features

#### Get Email Notifications for:
- **Membership Registration**
- **First Post**
- **Comment on Article**
- **Reply to Comments**
- **Password Change Successful**
- **Password Reset**
- **Password Reset Successful**

#### For Readers
- **Explore Articles**: Access a diverse collection of articles on various topics.
- **Author Profiles**: Learn more about the authors behind the articles.

#### For Authors
- **Create and Publish**: Write and publish articles with a user-friendly editor.
- **Manage Profile**: Build and update your author profile.
- **Engage with Readers**: Interact with your audience through comments and discussions.

## Architecture

#### Languages and Frameworks/Libraries
- **Python**: The core language used for backend development.
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **HTML**: For structuring the web pages.
- **CSS**: For styling the web pages.
- **Bash**: Automates updating, reconfiguring the server with code changes and setting environmental variables to mask credentials.
- **JavaScript**: For adding interactions and document object manipulations.
- **SQL**: Used to create authorized user profile, create database and assign neccessary permissions.
- **Request Library**: For automating the email notifications.
- **Pillow**: Used to resize and reshape profile photos before being saved to database.

#### Databases
- **MySQL**: Used for production database management.
- **SQLite**: Used for local development and testing.
- **Redis**: For caching views querysets, objects, template statics, etc.

#### Email Server
- **Brevo (Http)**: Used for sending emails, such as account verification and password reset links.

## Installation

#### Prerequisites
- Python 3.x
- Django 3.x or higher
- MySQL and SQLite

#### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DafetiteOgaga/article-hive-backend-component.git
    ```
     ```bash
   cd article-hive
   ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv env
    ```
    On Windows, use `env\Scripts\activate` to activate env.
    <br>
    On Linux/MacOS, use `source env/bin/activate` to activate env
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the database:**

* For SQLite (default): No additional setup needed.
* For MySQL:
  - Install MySQL and create a database.
  - Update DATABASES setting in settings.py with your MySQL credentials.
  - Apply migrations:

  ```bash
  python manage.py migrate
  ```

4. **Create a superuser:**

  ```bash
  python manage.py createsuperuser
  ```

5. **Run the development server:**

  ```bash
  python manage.py runserver
  ```

6. **Access the application:**
    Open your web browser and go to http://127.0.0.1:8000.

Configuration
Email Settings
To configure email settings for Brevo (SMTP), add the following to your settings.py:


## **Contributing**
We welcome contributions! Please fork the repository and submit pull requests for any enhancements, bug fixes, or new features.

**Fork the repository.**
- Create a new branch: git checkout -b feature/YourFeature.
- Commit your changes: git commit -m 'Add some feature'.
- Push to the branch: git push origin feature/YourFeature.
- Submit a pull request.


## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

## **Contact**
For any questions or feedback, please contact me at ogagadafetite@gmail.com.

Thank you for visiting Article Hive! We hope you enjoy reading and contributing to our platform.


### article-hive-backend-component and README.md were auto created using createRepo command in [*Custom Commands*](https://github.com/DafetiteOgaga/custom_commands)
		




###### *We Rise by Lifting Others.*
