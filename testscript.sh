#export PYTHONPATH=.
pip install -r requirements.txt
python3 -m unittest tests.test_speaklang
~/.local/bin/coverage run -m unittest tests/test_speaklang
~/.local/bin/coverage xml
rm -rf __pycache__
