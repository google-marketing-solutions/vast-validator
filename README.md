# VAST Request Validator

A command-line Python tool for validating VAST (Video Ad Serving Template) request URLs against implementation-specific rules for `web`, `app`, `ctv`, `audio`, and `doh`.

This tool helps developers and ad tech analysts ensure that VAST requests contain all required parameters and that those parameters are valid.

Please refer to the official documentation for updated parameters. The documentation supersedes this code.

Official documentation: https://support.google.com/admanager/answer/10678356

---

## Features

- Validation of required and programmatic parameters
- Type checking (`int`, `bool`, `str`, `enum`, `url`, `size`)
- Optional decoding of URL-encoded parameters
- JSON output mode for easy integration
- Quiet mode for scripting
- Implementation-specific validation

---

## Installation

```bash
git clone https://github.com/your-user/vast-validator.git
cd vast-validator
python3 -m venv venv
source venv/bin/activate
```

---

## Usage

```bash
python main.py "<VAST_REQUEST_URL>" -i <implementation_type> [options]
```

### Required Arguments

- `<VAST_REQUEST_URL>`: The full VAST request string (must be quoted to avoid shell interpretation).
- `-i, --implementation_type`: One of the following:
  - `web`
  - `app`
  - `ctv`
  - `audio`
  - `doh`

### Optional Flags

| Flag              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `-p, --programmatic` | Validate additional programmatic-specific required and recommended params |
| `-j, --json`          | Output result as a structured JSON                                        |
| `-d, --decode`        | URL-decode parameter values before validation                            |
| `-q, --quiet`         | Suppress all output except for errors                                    |

---

## Parameter Types

- `int`: Must be a valid integer (e.g. `123`)
- `bool`: Must be `0` or `1`
- `str`: Any non-empty string
- `enum`: Must match one of the allowed values
- `url`: Must be a valid URL (must include scheme like `https://`)
- `size`: Must be in the format `WIDTHxHEIGHT` (e.g. `640x480`)

---

## Implementation Types and Required Parameters

Each implementation type has its own set of rules for:

- `required`: Always expected parameters
- `programmatic_required`: Expected if `--programmatic` is passed
- `programmatic_recommended`: Helpful but not required (will trigger warnings)

The following types are supported:

- `web`
- `app`
- `ctv`
- `audio`
- `doh`

See `main.py` for a full breakdown of which parameters are expected for each type.

---

## Sample Executions

### 1. Validate a basic `web` request

```bash
python main.py "https://pubads.g.doubleclick.net/campads/ads?VAST_REQUEST" -i web -d
```

### 2. Validate a `web` programmatic request with JSON output

```bash
python main.py "https://pubads.g.doubleclick.net/campads/ads?VAST_REQUEST" -i web -p -j -d
```

### 3. Quiet mode (for shell scripting)

```bash
python main.py "https://..." -i app -p -d -q
```


## FAQ

**Q: Why do I get `command not found` errors when running the script?**
A: You must quote the VAST request URL, because it contains `&`, which the shell interprets.

```bash
# Wrong
python main.py https://...&param=value -i web

# Correct
python main.py "https://...&param=value" -i web
```
