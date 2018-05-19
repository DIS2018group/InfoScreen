# Info screen
How to install and run the web application

    # Install python virtualenv on Debian/Ubuntu
    $ sudo apt install python3-virtualenv
    
    # Create and enable virtualenv for Python
    $ virtualenv -p python3 env
    $ source env/bin/activate
    
    # Install dependencies
    $ pip install -r requirements.txt
    
    # Run the application
    $ python run.py
    
    # Now just visit http://127.0.0.1:8080 on your web browser

The script `listen_nfc.py` allows authentication features to be used with a compatible NFC/RFID reader with the USB ID `1DA8:1301`. If a compatible reader isn't available, a user can also be logged in and logged out manually using the command line:

    $ python -c "from users import login_user; login_user('NFC', 'TerryTest')"
    $ python -c "from users import logout_user; logout_user('NFC')"
