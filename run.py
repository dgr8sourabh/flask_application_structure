import os
from dotenv import load_dotenv
from app import create_app


# load environment variables from .env file
load_dotenv()

"""Run the Flask applications"""
app = create_app()

if __name__ == '__main__':
    # determine if the environment is local
    is_local = os.environ.get('ENV') == 'local'

    if is_local:
        app.run(
            debug=True,
            port=int(os.environ.get('BACKEND_PORT', 5000))
        )
    else:
        app.run()
