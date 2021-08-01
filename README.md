## CovXray
Detect COVID-19 using X-ray scans.

## How to setup?
1. Clone the repo into your system and open the project folder in your code editor application.
2. Create a new `virtualenv`.
3. Activate the newly create virtual environment.
4. Open a new terminal window and `cd` to *covxray* directory.
5. Install the requirements using `pip install -r req*.txt` command.
6. In *covxray* directory create new 'media' directory.
7. Within the 'media' directory create new 'images' directory.
8. Make migrations using `python manage.py makemigrations` command.
9. Migrate database using `python manage.py migrate` command.
10. Run server using `python manage.py runserver` command.