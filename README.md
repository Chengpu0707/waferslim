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

## Decision table

```
|Echo Fixture    |
|value|get value?|
|hello|hello     |
```

The corresponding code is waferslim\tests\fixtures\echo_fixture.py

## Query table

|query:Employee List|test arg            |
|name               |department |arg     |
|Alice              |Engineering|test arg|
|Bob                |Marketing  |test arg|

|query:Employee List   |
|name |department |arg |
|Alice|Engineering|None|
|Bob  |Marketing  |None|

The corresponding code is waferslim\tests\fixtures\employee_list.py


## Script table

|script:Login Fixture|admin       |secret|
|enter username      |admin              |
|enter password      |secret             |
|check               |is logged in|true  |
|enter username      |someone            |
|enter password      |secret             |
|check               |is logged in|false |

The corresponding code is waferslim\tests\fixtures\login.py


# Changes

## Python 3 compatibility fixes

**`converters.py`** — `Converter.to_string` referenced `unicode`, which does not exist in Python 3. Removed the redundant check; `str` in Python 3 is already unicode.

**`protocol.py`** — `_pack_item` had the `str`/`unicode` type checks inverted for Python 3: swapped to check `bytes` first (decoding to `str`), then `str`. Also added a `break` in `_get_message` when `recv()` returns empty bytes, preventing an infinite loop on a closed connection.

**`execution.py`** — `target_for` used direct dict access (`self.aliases[class_name][method_name]`), raising `KeyError` when FitNesse sends lifecycle method calls (e.g. `table`, `beginTable`) that are not defined on the fixture. Changed to `.get()` with a `None` fallback so unknown methods are silently ignored.

### New fixtures

**`tests/fixtures/echo_fixture.py`** — Replaced the original multi-method echo fixture with a simple Decision Table fixture: `set_value` / `get_value` pair for round-trip value testing.

**`tests/fixtures/employee_list.py`** — New Query Table fixture. Constructor accepts an optional `arg` (defaults to `None`). `query()` returns two rows (Alice/Engineering, Bob/Marketing) each exposing `name`, `department`, and `arg` columns.

**`tests/fixtures/login.py`** — New Script Table fixture. Constructor takes expected `username` and `password`. `enter_username` / `enter_password` set the values to check, and `is_logged_in` returns `True` only when both match the constructor arguments.


