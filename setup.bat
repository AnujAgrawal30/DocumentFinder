python get-pip.py || goto :error
python -m pip install --user virtualenv || goto :error
python -m venv documentenv || goto :error
Call .\documentenv\Scripts\activate || goto :error
python -m pip install -r requirements.txt || goto :error
echo "Installation Successful" && goto :end
:error
echo "Installation Unsuccessful"
:end
cmd \k