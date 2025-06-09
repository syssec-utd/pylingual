"""Tests for the compress data class"""
import os
from datetime import datetime
from pathlib import Path
from cg.models import CompressionData

def test_get_run_name():
    """Test that the correct run name is returned"""
    file_path = Path('/path/to/dir')
    run_name = 'a_run'
    compression_obj = CompressionData(file_path / run_name)
    assert compression_obj.run_name == run_name

def test_get_change_date(compression_object):
    """Test to get the date time for when a file was changed"""
    file_path = compression_object.spring_path
    file_path.touch()
    change_date = compression_object.get_change_date(file_path)
    assert change_date.date() == datetime.today().date()

def test_get_nlinks_one_link(compression_object):
    """Test get_nlinks when there is one link to a file"""
    file_path = compression_object.spring_path
    file_path.touch()
    nlinks = compression_object.get_nlinks(file_path)
    assert nlinks == 1

def test_get_nlinks_two_links(compression_object):
    """Test get_nlinks two links"""
    file_path = compression_object.spring_path
    file_path.touch()
    first_link = file_path.parent / 'link-1'
    os.link(file_path, first_link)
    nlinks = compression_object.get_nlinks(file_path)
    assert nlinks == 2

def test_get_nlinks_three_links(compression_object):
    """Test get_nlinks when three links"""
    file_path = compression_object.spring_path
    file_path.touch()
    first_link = file_path.parent / 'link-1'
    os.link(file_path, first_link)
    second_link = file_path.parent / 'link-2'
    os.link(file_path, second_link)
    nlinks = compression_object.get_nlinks(file_path)
    assert nlinks == 3