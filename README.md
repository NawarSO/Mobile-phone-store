# Mobile-phone-store
Welcome to our simple project.
In this project you can find system analysis for mobiles store website including the SRS
# To install the libraries 
you can find a file named 'requirements.txt' it include the libraries you need to run the project.
You can install them using the command :
pip install -r requirements.txt
# To run the project:
At first you need to migrate the data base using the commands:
python manage.py makemigrations
python manage.py migrate
Now you can run the server using the command :
python manage.py runserver
the server now will run on http://localhost:8000/
# Api documentation 
you can find api documentation on http://localhost:8000/swagger/
you will find a list with all the crud operations and endpoints that you can access to.

# The AI service 
The AI service here is not complete if yoy use it it will give you result but it from model trained on 15 rows dataset but you can 
put you data set for the model and fit it then it suppose to give right result .
You will find unit tests in the file tests.
To Run the test use the command:
python manage.py test api.tests


