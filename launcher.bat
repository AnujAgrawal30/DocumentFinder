Call .\documentenv\Scripts\activate.bat || goto :error
start "" "website\index.html"
python manage.py runserver
:error
echo "There was some error launching the web-page. Please ensure you have installed the project properly."
cmd \k