pip3 install -r ./requirements.txt
pip3 install -r ./requirements-dev.txt

python3 ./setup.py sdist
python3 ./setup.py bdist_wheel
twine upload dist/*