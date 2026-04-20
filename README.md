waferslim
=========


FitNesse SLIM protocol v0.3 implementation compatible with 3.11.

It is forked from https://github.com/peterdemin/waferslim, to debug Python2 code in the original, and to add .wiki examples for decision table, query table, and script table.


# Fixture Test Page Demo

The test page is at waferslim\tests\fitnesse\pages\PythonTest.wiki

## Defines

```
!define TEST_SYSTEM {slim}
!define SLIM_PORT {0}
!path Python
!define COMMAND_PATTERN {python3 -m waferslim.server --syspath %p }

|import|
|tests |
```

## Original table

```
|script|!-EchoFixture-!              |
|check |echo       |hello|hello hello|
|check |echo       |world|hello world|
|check |static_echo|hello|hello      |
|check |class_echo |hello|hello      |
```

The corresponding code is waferslim\tests\fixtures\echo_fixture.py

## Decision table

```
|Division|true                          |
|x       |y|divide?                     |
|100     |5|20.0                        |
|0       |5|0.0                         |
|100     |0|EXCEPTION:=~/divide by zero/|
```

The corresponding code is waferslim\tests\fixtures\division.py

## Query table

```
|query:Employee List|test arg            |
|name               |department |arg     |
|Alice              |Engineering|test arg|
|Bob                |Marketing  |test arg|

|query:Employee List   |
|name |department |arg |
|Alice|Engineering|None|
|Bob  |Marketing  |None|
```

The corresponding code is waferslim\tests\fixtures\employee_list.py


## Script table

```
|script:Login Fixture|admin       |secret|
|enter username      |admin              |
|enter password      |secret             |
|check               |is logged in|true  |
|enter username      |someone            |
|enter password      |secret             |
|check               |is logged in|false |
```

The corresponding code is waferslim\tests\fixtures\login.py


# Installation

Git clone this project, and install locally from the project:
```
pip install .
```


# Changes

## Python 3 compatibility fixes

**`converters.py`** — `Converter.to_string` referenced `unicode`, which does not exist in Python 3. Removed the redundant check; `str` in Python 3 is already unicode.

**`protocol.py`** — `_pack_item` had the `str`/`unicode` type checks inverted for Python 3: swapped to check `bytes` first (decoding to `str`), then `str`. Also added a `break` in `_get_message` when `recv()` returns empty bytes, preventing an infinite loop on a closed connection.

**`execution.py`** — `target_for` used direct dict access (`self.aliases[class_name][method_name]`), raising `KeyError` when FitNesse sends lifecycle method calls (e.g. `table`, `beginTable`) that are not defined on the fixture. Changed to `.get()` with a `None` fallback so unknown methods are silently ignored.

### New fixtures

**`tests/fixtures/echo_fixture.py`** — Replaced the original multi-method echo fixture with a simple Decision Table fixture: `set_value` / `get_value` pair for round-trip value testing.

**`tests/fixtures/employee_list.py`** — New Query Table fixture. Constructor accepts an optional `arg` (defaults to `None`). `query()` returns two rows (Alice/Engineering, Bob/Marketing) each exposing `name`, `department`, and `arg` columns.

**`tests/fixtures/login.py`** — New Script Table fixture. Constructor takes expected `username` and `password`. `enter_username` / `enter_password` set the values to check, and `is_logged_in` returns `True` only when both match the constructor arguments.


#	How to step in a waferslim page in VsCode?

The challenge is that FitNesse launches waferslim as a subprocess with stdin/stdout redirected, so pdb won't work. Use remote debugging via debugpy:

##	Step 1 — Add debugpy to your fixture

In the fixture file you want to debug (e.g. division.py):
```
  import debugpy
  debugpy.listen(5678)
  debugpy.wait_for_client()   # pauses until debugger attaches
```
Put it at the top of the method you want to break into, or in __init__.

##	Step 2 — Attach VS Code
In VS Code, add this to .vscode/launch.json:
```
  {
    "type": "python",
    "request": "attach",
    "name": "Attach waferslim",
    "connect": { "host": "localhost", "port": 5678 },
    "pathMappings": [{
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "."
    }]
  }
```
Press F5 → Attach waferslim. VS Code connects to port 5678, hits your breakpoint, and you can:
  - F10 — step over
  - F11 — step into
  - Shift+F11 — step out
  - F5 — continue

##	Step 3 — Run the FitNesse test

Go to http://localhost/LanguageSuite.PythonTest?test and run it. The test will hang waiting for a debugger to connect.

##	Step 4 — Remove debugpy when done

Delete the debugpy.listen / debugpy.wait_for_client() lines, otherwise the test will hang every time.
