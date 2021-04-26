import os
from flaskr import create_app

# Run Tests
os.system('source env/bin/activate ; python3 test_flaskr_routes.py')


app = create_app('config.DevConfig')

