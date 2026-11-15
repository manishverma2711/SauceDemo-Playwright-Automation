New-Item -ItemType Directory -Force -Path reports | Out-Null
New-Item -ItemType Directory -Force -Path test-results | Out-Null

python -m pytest tests -n auto --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
