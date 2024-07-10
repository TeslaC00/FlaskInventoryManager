# Note: set env variables outside of code
from app import create_app

if __name__ == '__main__':
    myapp = create_app()
    myapp.run(host='0.0.0.0')
