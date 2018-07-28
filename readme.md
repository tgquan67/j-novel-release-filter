# Filter for J-Novel Club's releases
Run:
```
pip install -r requirements.txt
cd JNCFilter
python manage.py runserver 0.0.0.0:8000
```
Omit the `0.0.0.0:8000` part to run on localhost only, or modify it to suit your need. The server is left in debug mode.
This was tested on Python 3.6.5 on Windows 10 64-bit, other environments may require different versions of packages.  
After starting, visit `/set/` endpoint to modify the choice and go back to `/` to browse the releases.