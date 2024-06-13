pip install -r requests.txt
./tests/speaklang_unittest.py
~/.local/bin/coverage run -m unittest tests/test_speaklang.py
~/.local/bin/coverage xml
rm -rf __pycache__
