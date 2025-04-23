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

"""A script for validating VAST request parameters."""

import argparse
import json
import re
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
import urllib
import urllib.parse


class VastRequestValidator:
  """A class for validating VAST request strings."""

  def __init__(self) -> None:
    """Initializes the VastRequestValidator with parameter rules."""
    self.param_rules: Dict[str, Dict[str, Dict[str, Union[str, List[str]]]]] = {
        "web": {
            "required": {
                "correlator": {"type": "int"},
                "description_url": {"type": "url"},
                "env": {
                    "type": "enum",
                    "allowed_values": ["vp", "instream", "outstream"],
                },
                "gdfp_req": {"type": "int"},
                "iu": {"type": "str"},
                "output": {
                    "type": "enum",
                    "allowed_values": [
                        "vast",
                        "xml_vast2",
                        "xml_vast3",
                        "xml_vast4",
                    ],
                },
                "sz": {"type": "size"},
                "unviewed_position_start": {"type": "int"},
                "url": {"type": "url"},
                "vpmute": {"type": "bool"},
            },
            "programmatic_required": {
                "ott_placement": {"type": "int"},
                "plcmt": {"type": "int"},
                "vpa": {"type": "bool"},
            },
            "programmatic_recommended": {
                "aconp": {"type": "bool"},
                "dth": {"type": "int"},
                "givn": {"type": "str"},
                "hl": {"type": "str"},
                "omid_p": {"type": "str"},
                "vconp": {"type": "bool"},
                "vid_d": {"type": "int"},
                "vpos": {
                    "type": "enum",
                    "allowed_values": [
                        "preroll",
                        "midroll",
                        "postroll",
                        "1",
                        "2",
                        "3",
                        "0",
                    ],
                },
                "wta": {"type": "int"},
            },
        },
        "app": {
            "required": {
                "correlator": {"type": "int"},
                "description_url": {"type": "url"},
                "env": {
                    "type": "enum",
                    "allowed_values": ["vp", "instream", "outstream"],
                },
                "gdfp_req": {"type": "int"},
                "iu": {"type": "str"},
                "output": {
                    "type": "enum",
                    "allowed_values": [
                        "vast",
                        "xml_vast2",
                        "xml_vast3",
                        "xml_vast4",
                    ],
                },
                "sz": {"type": "size"},
                "unviewed_position_start": {"type": "int"},
                "url": {"type": "url"},
                "vpmute": {"type": "bool"},
            },
            "programmatic_required": {
                "idtype": {"type": "int"},
                "is_lat": {"type": "bool"},
                "ott_placement": {"type": "int"},
                "plcmt": {"type": "int"},
                "rdid": {"type": "str"},
                "vpa": {"type": "bool"},
            },
            "programmatic_recommended": {
                "aconp": {"type": "bool"},
                "an": {"type": "str"},
                "dth": {"type": "int"},
                "givn": {"type": "str"},
                "hl": {"type": "str"},
                "msid": {"type": "str"},
                "omid_p": {"type": "str"},
                "pvid": {"type": "str"},
                "sid": {"type": "str"},
                "vconp": {"type": "bool"},
                "vid_d": {"type": "int"},
                "vpos": {
                    "type": "enum",
                    "allowed_values": [
                        "preroll",
                        "midroll",
                        "postroll",
                        "1",
                        "2",
                        "3",
                        "0",
                    ],
                },
                "wta": {"type": "int"},
            },
        },
        "ctv": {
            "required": {
                "correlator": {"type": "int"},
                "env": {
                    "type": "enum",
                    "allowed_values": ["vp", "instream", "outstream"],
                },
                "gdfp_req": {"type": "int"},
                "iu": {"type": "str"},
                "output": {
                    "type": "enum",
                    "allowed_values": [
                        "vast",
                        "xml_vast2",
                        "xml_vast3",
                        "xml_vast4",
                    ],
                },
                "sz": {"type": "size"},
                "url": {"type": "url"},
            },
            "programmatic_required": {
                "idtype": {"type": "int"},
                "is_lat": {"type": "bool"},
                "ott_placement": {"type": "int"},
                "plcmt": {"type": "int"},
                "rdid": {"type": "str"},
                "vpa": {"type": "bool"},
                "vpmute": {"type": "bool"},
            },
            "programmatic_recommended": {
                "aconp": {"type": "bool"},
                "an": {"type": "str"},
                "dth": {"type": "int"},
                "givn": {"type": "str"},
                "hl": {"type": "str"},
                "msid": {"type": "str"},
                "omid_p": {"type": "str"},
                "sid": {"type": "str"},
                "vconp": {"type": "bool"},
                "vid_d": {"type": "int"},
                "vpos": {
                    "type": "enum",
                    "allowed_values": [
                        "preroll",
                        "midroll",
                        "postroll",
                        "1",
                        "2",
                        "3",
                        "0",
                    ],
                },
                "wta": {"type": "int"},
            },
        },
        "audio": {
            "required": {
                "ad_type": {"type": "str"},
                "correlator": {"type": "int"},
                "env": {
                    "type": "enum",
                    "allowed_values": ["vp", "instream", "outstream"],
                },
                "gdfp_req": {"type": "int"},
                "iu": {"type": "str"},
                "output": {
                    "type": "enum",
                    "allowed_values": [
                        "vast",
                        "xml_vast2",
                        "xml_vast3",
                        "xml_vast4",
                    ],
                },
                "url": {"type": "url"},
            },
            "programmatic_required": {
                "idtype": {"type": "int"},
                "is_lat": {"type": "bool"},
                "plcmt": {"type": "int"},
                "rdid": {"type": "str"},
                "vpa": {"type": "bool"},
                "vpmute": {"type": "bool"},
            },
            "programmatic_recommended": {
                "aconp": {"type": "bool"},
                "an": {"type": "str"},
                "dth": {"type": "int"},
                "givn": {"type": "str"},
                "hl": {"type": "str"},
                "msid": {"type": "str"},
                "omid_p": {"type": "str"},
                "sid": {"type": "str"},
                "vconp": {"type": "bool"},
                "vpos": {
                    "type": "enum",
                    "allowed_values": [
                        "preroll",
                        "midroll",
                        "postroll",
                        "1",
                        "2",
                        "3",
                        "0",
                    ],
                },
                "wta": {"type": "int"},
            },
        },
        "doh": {
            "required": {
                "correlator": {"type": "int"},
                "env": {
                    "type": "enum",
                    "allowed_values": ["vp", "instream", "outstream"],
                },
                "gdfp_req": {"type": "int"},
                "iu": {"type": "str"},
                "output": {
                    "type": "enum",
                    "allowed_values": [
                        "vast",
                        "xml_vast2",
                        "xml_vast3",
                        "xml_vast4",
                    ],
                },
                "sz": {"type": "size"},
                "url": {"type": "url"},
                "vpmute": {"type": "bool"},
            },
            "programmatic_required": {
                "idtype": {"type": "int"},
                "is_lat": {"type": "bool"},
                "plcmt": {"type": "int"},
                "rdid": {"type": "str"},
                "sid": {"type": "str"},
                "venuetype": {"type": "int"},
            },
            "programmatic_recommended": {
                "aconp": {"type": "bool"},
                "an": {"type": "str"},
                "dth": {"type": "int"},
                "givn": {"type": "str"},
                "hl": {"type": "str"},
                "msid": {"type": "str"},
                "omid_p": {"type": "str"},
            },
        },
    }

  @staticmethod
  def validate_url(url_string: str) -> bool:
    """Validates if a URL string is well-formed."""
    try:
      result = urllib.parse.urlparse(url_string)
      return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
      return False

  def validate_vast_request(
      self,
      vast_request: str,
      implementation_type: str,
      is_programmatic: bool = False,
      decode_params: bool = False,
  ) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
    """Validates a VAST request based on the implementation type."""
    present_params: Dict[str, str] = {}
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    if implementation_type not in self.param_rules:
      errors.append({
          "parameter": "implementation_type",
          "type": "invalid",
          "message": (
              f"Invalid implementation type: '{implementation_type}'. Allowed"
              f" types are: {', '.join(self.param_rules.keys())}"
          ),
      })
      return present_params, errors
    for match in re.finditer(r"([a-zA-Z0-9_]+)=([^&]*)", vast_request):
      param_name = match.group(1)
      param_value = match.group(2)
      if decode_params:
        param_value = urllib.parse.unquote(param_value)
      present_params[param_name] = param_value

    def validate_param(
        param: str, rules: Dict[str, Union[str, List[str]]], value: str
    ) -> None:
      """Validates a single parameter value based on its rules."""
      if not value:
        errors.append({
            "parameter": param,
            "type": "invalid",
            "message": "Parameter value is empty",
        })
        return
      param_type = rules["type"]
      if param_type == "int":
        try:
          int(value)
        except ValueError:
          errors.append({
              "parameter": param,
              "type": "invalid",
              "message": f"Expected integer, got '{value}'",
          })
      elif param_type == "url":
        if not VastRequestValidator.validate_url(value):
          errors.append({
              "parameter": param,
              "type": "invalid",
              "message": f"Invalid URL: '{value}'",
          })
      elif param_type == "enum":
        if value not in rules["allowed_values"]:
          errors.append({
              "parameter": param,
              "type": "invalid",
              "message": (
                  "Invalid value. Allowed values:"
                  f" {', '.join(rules['allowed_values'])}"
              ),
          })
      elif param_type == "size":
        if not re.match(r"^\d+x\d+$", value):
          errors.append({
              "parameter": param,
              "type": "invalid",
              "message": "Expected format WIDTHxHEIGHT (e.g., 640x480)",
          })
      elif param_type == "bool":
        if value not in ("0", "1"):
          errors.append({
              "parameter": param,
              "type": "invalid",
              "message": f"Expected 0 or 1, got '{value}'",
          })

    rules = self.param_rules[implementation_type]
    for param_dict, error_message, is_required in [
        (rules.get("required", {}), "Missing required parameter", True),
        (
            rules.get("programmatic_required", {}),
            "Missing required programmatic parameter",
            is_programmatic,
        ),
        (
            rules.get("programmatic_recommended", {}),
            "Recommended programmatic parameter not found",
            False,
        ),
    ]:
      if not is_required and param_dict is rules.get(
          "programmatic_required", {}
      ):
        continue
      for param, param_rules in param_dict.items():
        if param not in present_params:
          if is_required:
            errors.append({
                "parameter": param,
                "type": "missing",
                "message": error_message,
            })
        else:
          validate_param(param, param_rules, present_params[param])
    return present_params, errors + warnings


def main():
  """Main function to parse arguments and validate VAST requests."""
  parser = argparse.ArgumentParser(
      description="Validate VAST request parameters."
  )
  parser.add_argument("vast_request", help="The VAST request string.")
  parser.add_argument(
      "-i",
      "--implementation_type",
      choices=["web", "app", "ctv", "audio", "doh"],
      required=True,
      help=(
          "The implementation type of the VAST request (web, app, ctv, audio,"
          " doh)."
      ),
  )
  parser.add_argument(
      "-p",
      "--programmatic",
      action="store_true",
      help="Indicate if the request is programmatic.",
  )
  parser.add_argument(
      "-j", "--json", action="store_true", help="Output in JSON format."
  )
  parser.add_argument(
      "-d", "--decode", action="store_true", help="URL-decode parameter values."
  )
  parser.add_argument(
      "-q",
      "--quiet",
      action="store_true",
      help="Suppress output except for errors.",
  )
  args = parser.parse_args()
  validator = VastRequestValidator()
  is_programmatic = args.programmatic
  implementation_type = args.implementation_type.lower()
  present_params, issues = validator.validate_vast_request(
      args.vast_request, implementation_type, is_programmatic, args.decode
  )
  errors = [
      issue for issue in issues if issue.get("type") in ("invalid", "missing")
  ]
  warnings = [
      issue
      for issue in issues
      if issue.get("type") not in ("invalid", "missing")
  ]
  if args.json:
    output = {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "present_parameters": present_params,
    }
    print(json.dumps(output, indent=4))
  else:
    if not args.quiet:
      print("\n--- Validation Results ---")
      print(f"Implementation Type: {implementation_type}")
      print(f"Present Parameters: {', '.join(present_params) or 'None'}")
    if errors:
      print("\n--- Errors ---")
      for error in errors:
        print(f"  Parameter: {error['parameter']}")
        if "type" in error:
          print(f"    Type: {error['type']}")
        print(f"    Message: {error['message']}")
    if warnings and not args.quiet:
      print("\n--- Warnings ---")
      for warning in warnings:
        print(f"  Parameter: {warning['parameter']}")
        print(f"    Message: {warning['message']}")
    if not errors and not args.quiet:
      print("No errors found.")


if __name__ == "__main__":
  main()
