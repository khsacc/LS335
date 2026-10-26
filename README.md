# LakeShore 335 Controller

PyQt6 application for monitoring and controlling a LakeShore 335 temperature
controller over GPIB. It shows both temperature inputs, the setpoint and heater
output, and can save readings to CSV. A simulation mode is available without
hardware.

This directory is maintained in the [LS335 repository](https://github.com/khsacc/LS335)
and included in `bl18c_controller` as the `apps/LakeShore335` git submodule.

The lower controls use three panels: control parameters, heater output, and
logging. Press Enter to apply a setpoint or ramp rate. Use the +/- buttons to
change the current setpoint by the entered number of kelvin. A rate of
`0 K/min` disables the ramp; a positive rate enables it. Selecting a heater
range applies it immediately. The logging interval can be set from 1 to 3600 s;
temperature readings continue at the normal 1 s polling interval.

## Local readings endpoint

While connected, the app automatically serves
`GET http://127.0.0.1:8767/api/v1/readings` in standalone and embedded mode.
The JSON response contains `connected`, `timestamp` (Unix seconds),
`temperature_a_k`, `temperature_b_k`, `target_setpoint_k`, `ramp_enabled`,
`ramp_rate_k_per_min`, and `heater_range` (`OFF`, `LOW`, `MEDIUM`, or `HIGH`). The two
temperatures and timestamp are `null` until the first poll. The listener
stops on a normal disconnect. Each request reads the app's cache and makes no
GPIB query. The server is read-only and binds to loopback only. If port 8767
is occupied, the instrument remains connected but the endpoint is unavailable.

## Standalone use

Use Python 3.11 or newer. Install the local dependencies:

```bash
python -m pip install -r requirements.txt
python app.py
```

The same launcher works inside `bl18c_controller` from its root:

```bash
python apps/LakeShore335/app.py
```

The `apps/LakeShore335/` directory can be placed outside `bl18c_controller`;
the standalone launcher does not import its parent project. Select **Simulation**
before connecting to try the UI without an instrument. For a real connection,
install a VISA implementation and its GPIB driver (for example, NI-VISA on
Windows), then enter the instrument's GPIB resource address. The default is
`GPIB0::12::INSTR`.

The selected log directory is saved under `__localdata/` in this directory.
Closing a standalone window disconnects its instrument. Disconnecting does not
change the heater or setpoint.

## Use from bl18c_controller

Run `python main.py` or `python main.py --debug` from the parent project. The
main launcher connects to the device and passes its shared
`LakeShore335Backend` to `LakeShore335Window`. The main launcher owns that
connection; closing the LakeShore window leaves it available to other apps.
`--debug` uses the simulated backend.

After cloning the parent repository, initialise this submodule with
`git submodule update --init apps/LakeShore335`.
