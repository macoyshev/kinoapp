from .api import create_app
from .db import create_bd

app = create_app()
create_bd()
