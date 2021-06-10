rd dist /s /q
rd build /s /q
rd plotx.egg-info /s /q
conda run python setup.py sdist bdist_wheel
TIMEOUT 3
pause