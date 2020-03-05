## This project has been developed as a part of the Infieon AI Challenge. Please go through the following installation manual to get started with the app.
# Installation Manual
## For Windows:
### The project requires the user to have Python 3 installed in their systems and added to their path with name as python. To check if your system has this setting Follow these steps:
- Press Windows+R to open "Run" box.
- Type "cmd" and click ok to open Command Prompt.
- Type "python" and press "Enter"
- If the output is something like `'python' is not recognized as an internal or external command, operable program or batch file.` Please follow [these](https://phoenixnap.com/kb/how-to-install-python-3-windows) steps to install python3 and add to your path.
### Once you have python 3 installed and added to your path, follow these steps to Install the software:
- Clone the repository into the computer
- Go To Folder named "DocumentFinder"
- Double-click "setup.bat" and let it install the software. If at the end you did not find "Installation Successful", Please check again if python 3 is installed and added to Environment Variables and try again.
- Now to launch the application, double-click "launcher.bat". It should open the project for you. Wait a few seconds after it opens to let the server start properly before performing any actions.
## For Linux/MacOS
### Before installing the project. Make sure you have python 3 instlled and added to your path
- Clone the repository into th computer
- Install pip and virtualenv if not already installed using instructions provided [here](https://www.codingforentrepreneurs.com/blog/install-django-on-mac-or-linux)
- Open terminal inside the "DocumentFinder" Folder and activate the virtual environment
- Install required libraries using `pip install -r requirements.txt`
- start the server using `python manage.py runserver`
- launch the web-app by double-clicking website/index.html
