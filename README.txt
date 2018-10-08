webshop
=======


Dependencies:
    json serialisation - https://github.com/Pylons/pyramid-cookiecutter-alchemy
    
Insominia API client can be used to make queries. Configuration file is here: https://github.com/aSemy/webshop/blob/master/webshop_insomnia.json

Getting Started
---------------

- Change directory into your newly created project.

    cd webshop

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_webshop_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
    
Endpoints 
---------

/components
view components

/orders
view orders

/orders/create
Arguments: 
    - client id (to record which client has made this order)
    - component ids (an array of valid component ids)
    - preferred delivery time (optional. in format yearMonthDay_HourMinute)
    
E.g.
{
	"client_id" : 2,
	"component_ids" : [1],
	"preferred_delivery_yyyyMMdd_HHmm" : "20190201_0000"
}

