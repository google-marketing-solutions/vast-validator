#!/usr/bin/env python
# Copyright 2025 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import json
import unittest
from unittest import mock
from main import main
from main import VastRequestValidator


class TestVastRequestValidator(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.validator = VastRequestValidator()

  def test_validate_url_valid(self):
    self.assertTrue(VastRequestValidator.validate_url("http://example.com"))
    self.assertTrue(
        VastRequestValidator.validate_url(
            "https://example.com/path?query=value"
        )
    )

  def test_validate_url_invalid(self):
    self.assertFalse(VastRequestValidator.validate_url("not a url"))
    self.assertFalse(VastRequestValidator.validate_url("example.com"))
    self.assertFalse(VastRequestValidator.validate_url("ftp://example.com"))

  def test_validate_vast_request_web_required(self):
    vast_request = "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0"
    _, errors = self.validator.validate_vast_request(
        vast_request, "web"
    )
    self.assertEqual(len(errors), 0)

  def test_validate_vast_request_web_missing_required(self):
    vast_request = "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com"
    _, errors = self.validator.validate_vast_request(
        vast_request, "web"
    )
    self.assertEqual(len(errors), 1)
    self.assertEqual(errors[0]["parameter"], "vpmute")

  def test_validate_vast_request_web_invalid_param_type(self):
    vast_request = "correlator=abc&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0"
    _, errors = self.validator.validate_vast_request(
        vast_request, "web"
    )
    self.assertEqual(len(errors), 1)
    self.assertEqual(errors[0]["parameter"], "correlator")

  def test_validate_vast_request_web_programmatic_required(self):
    vast_request = "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0&ott_placement=1&plcmt=2&vpa=1"
    _, errors = self.validator.validate_vast_request(
        vast_request, "web", is_programmatic=True
    )
    self.assertEqual(len(errors), 0)

  def test_validate_vast_request_app_required(self):
    vast_request = "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0"
    _, errors = self.validator.validate_vast_request(
        vast_request, "app"
    )
    self.assertEqual(len(errors), 0)

  def test_validate_vast_request_app_programmatic_required(self):
    vast_request = "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0&idtype=1&is_lat=0&ott_placement=1&plcmt=2&rdid=test_rdid&vpa=1"
    _, errors = self.validator.validate_vast_request(
        vast_request, "app", is_programmatic=True
    )
    self.assertEqual(len(errors), 0)

  def test_validate_vast_request_ctv_required(self):
    vast_request = "correlator=123&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&url=http://example.com"
    _, errors = self.validator.validate_vast_request(
        vast_request, "ctv"
    )
    self.assertEqual(len(errors), 0)

  def test_validate_vast_request_ctv_programmatic_required(self):
    vast_request = "correlator=123&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&url=http://example.com&idtype=1&is_lat=0&ott_placement=1&plcmt=2&rdid=test_rdid&vpa=1&vpmute=0"
    _, errors = self.validator.validate_vast_request(
        vast_request, "ctv", is_programmatic=True
    )
    self.assertEqual(len(errors), 0)

  def test_main_valid_web(self):
    with mock.patch(
        "sys.argv",
        [
            "vast_request_validator.py",
            "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0",
            "-i",
            "web",
        ],
    ):
      with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No errors found.", output)

  def test_main_invalid_web(self):
    with mock.patch(
        "sys.argv",
        [
            "vast_request_validator.py",
            "correlator=abc&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0",
            "-i",
            "web",
        ],
    ):
      with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Errors", output)
        self.assertIn("correlator", output)

  def test_main_json_output(self):
    with mock.patch(
        "sys.argv",
        [
            "vast_request_validator.py",
            "correlator=123&description_url=http://example.com&env=vp&gdfp_req=1&iu=/123/example&output=vast&sz=640x480&unviewed_position_start=1&url=http://example.com&vpmute=0",
            "-i",
            "web",
            "-j",
        ],
    ):
      with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        main()
        output = mock_stdout.getvalue()
        result = json.loads(output)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
