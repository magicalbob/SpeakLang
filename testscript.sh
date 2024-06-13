pip install -r requirements.txt
./tests/speaklang_unittest.py
~/.local/bin/coverage run -m unittest tests/speaklang_unittest.py
~/.local/bin/coverage xml
rm -rf __pycache__
