# Step 1: Set Up a Virtual Environment
pip install virtualenv
virtualenv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Step 2: Install Dependencies
pip install -r requirements.txt

# Step 3: Apply Migrations
python manage.py migrate

# Step 4: Create a Superuser (Optional)
python manage.py createsuperuser

# Step 5: Collect Static Files (if needed)
python manage.py collectstatic

# Step 6: Run the Development Server
python manage.py runserver

# Step 7: Access the Project
# Open your web browser and navigate to http://127.0.0.1:8000/
# For admin panel, go to http://127.0.0.1:8000/admin/
