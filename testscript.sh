export PYTHONPATH=.
pip install -r requirements.txt
./tests/test_speaklang.py
~/.local/bin/coverage run -m unittest tests/test_speaklang.py
~/.local/bin/coverage xml
rm -rf __pycache__
