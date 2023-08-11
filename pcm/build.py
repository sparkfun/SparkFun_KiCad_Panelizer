
import os
from os import path
import shutil
import pathlib
import json
import sys

src_path = path.join(path.dirname(__file__),'..','SparkFunKiCadPanelizer')
version_path = path.join(src_path, 'resource', '_version.py')

metadata_template = path.join(path.dirname(__file__),'metadata_template.json')
resources_path = path.join(path.dirname(__file__),'resources')

build_path = path.join('build')

# Delete build and recreate
try:
    shutil.rmtree(build_path)
except FileNotFoundError:
    pass
os.mkdir(build_path)
os.mkdir(path.join(build_path,'plugin'))
os.chdir(build_path)

# Copy plugin
shutil.copytree(src_path, path.join('plugin','plugins'))

# Clean out any __pycache__ or .pyc files (https://stackoverflow.com/a/41386937)
[p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]
[p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]

# Don't include test_dialog.py. It isn't needed. It's a developer thing.
[p.unlink() for p in pathlib.Path('.').rglob('test_dialog.py')]

# Copy icon
shutil.copytree(resources_path, path.join('plugin','resources'))

# Copy metadata
metadata = path.join('plugin','metadata.json')
shutil.copy(metadata_template, metadata)

# Load up json script
with open(metadata) as f:
    md = json.load(f)

# Get version from resource/_version.py
# https://stackoverflow.com/a/7071358
import re
verstrline = open(version_path, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    verstr = "1.0.0"

# Update download URL
md['versions'][0].update({
    'version': verstr,
    'download_url': 'https://github.com/sparkfun/SparkFun_KiCad_Panelizer/releases/download/v{0}/SparkFunKiCadPanelizer-{0}-pcm.zip'.format(verstr)
})

# Update metadata.json
with open(metadata, 'w') as of:
    json.dump(md, of, indent=2)

# Zip all files
zip_file = 'SparkFunKiCadPanelizer-{0}-pcm.zip'.format(md['versions'][0]['version'])
shutil.make_archive(pathlib.Path(zip_file).stem, 'zip', 'plugin')

# Rename the plugin directory so we can upload it as an artifact - and avoid the double-zip
shutil.move('plugin', 'SparkFunKiCadPanelizer-{0}-pcm'.format(md['versions'][0]['version']))
