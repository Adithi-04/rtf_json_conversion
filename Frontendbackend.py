# test_core_logic.py

import pytest
import os
import json
from core_logic import extract_font_details, convert_rtf

def test_extract_font_details():
    rtf_content = r'{\fonttbl{\f0 Arial;}}'
    expected_fonts = {'f0': 'Arial'}
    assert extract_font_details(rtf_content) == expected_fonts

def test_convert_rtf(tmpdir):
    rtf_content = r'{\fonttbl{\f0 Arial;}}\page\header{Header}\trhdr\title{\cell} Title \cell\trrow\cell Data \cell'
    rtf_file = tmpdir.join('test.rtf')
    output_dir = tmpdir.mkdir('output')
    rtf_file.write(rtf_content)
    
    status, remarks = convert_rtf(str(rtf_file), str(output_dir))
    
    assert status == "Successful"
    assert os.path.isfile(os.path.join(str(output_dir), 'test.json'))
    
    with open(os.path.join(str(output_dir), 'test.json')) as f:
        data = json.load(f)
    
    assert 'fonts' in data
    assert 'data' in data
    assert len(data['data']) > 0
