# Artisan module and dependency map

Full method-level calls and source hashes: `function-dependency-map.json`.

| Module | Lines | Functions | Direct Qt imports | Internal imports |
|---|---:|---:|---|---|
| `src/artisanlib/__init__.py` | 9 | 0 | None |  |
| `src/artisanlib/acaia.py` | 1536 | 114 | PyQt6.QtCore | artisanlib.async_comm, artisanlib.atypes, artisanlib.ble_port, artisanlib.scale, artisanlib.util |
| `src/artisanlib/aillio_r1.py` | 719 | 28 | None |  |
| `src/artisanlib/aillio_r2.py` | 976 | 37 | None |  |
| `src/artisanlib/alarms.py` | 1184 | 31 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/async_comm.py` | 600 | 33 | None | artisanlib.atypes |
| `src/artisanlib/atypes.py` | 595 | 0 | PyQt6.QtCore | plus.stock |
| `src/artisanlib/autosave.py` | 229 | 8 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main |
| `src/artisanlib/axis.py` | 997 | 30 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/background.py` | 1164 | 35 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/batches.py` | 151 | 4 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main |
| `src/artisanlib/ble_port.py` | 589 | 40 | PyQt6.QtCore | artisanlib.async_comm |
| `src/artisanlib/bluedot.py` | 110 | 8 | None | artisanlib.ble_port |
| `src/artisanlib/button_style.py` | 459 | 0 | None | artisanlib.util |
| `src/artisanlib/calculator.py` | 343 | 12 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/canvas.py` | 19562 | 342 | PyQt6, PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib, artisanlib.atypes, artisanlib.bluedot, artisanlib.button_style, artisanlib.colors, artisanlib.comm, artisanlib.designer, artisanlib.device_registry, artisanlib.dialogs, artisanlib.events, artisanlib.hottop, artisanlib.ikawa, artisanlib.kaleido, artisanlib.main, artisanlib.mugma, artisanlib.orbiter, artisanlib.phidgets, artisanlib.roasthubs, artisanlib.santoker, artisanlib.santoker_r, artisanlib.time, artisanlib.util, plus.blend, plus.queue, plus.stock, plus.sync, plus.util |
| `src/artisanlib/colors.py` | 974 | 18 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/colortrack.py` | 230 | 13 | PyQt6.QtCore | artisanlib.async_comm, artisanlib.atypes, artisanlib.ble_port, artisanlib.filters |
| `src/artisanlib/comm.py` | 7581 | 376 | PyQt6, PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.aillio_r1, artisanlib.aillio_r2, artisanlib.atypes, artisanlib.colortrack, artisanlib.lebrew, artisanlib.main, artisanlib.util |
| `src/artisanlib/command_utility.py` | 68 | 1 | None | artisanlib |
| `src/artisanlib/comparator.py` | 2199 | 83 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.qcheckcombobox, artisanlib.suppress_errors, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/cropster.py` | 1380 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/cup_profile.py` | 413 | 18 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.widgets |
| `src/artisanlib/curves.py` | 2725 | 99 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.canvas, artisanlib.dialogs, artisanlib.main, artisanlib.qrcode, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/designer.py` | 760 | 12 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/device_registry.py` | 479 | 8 | None | artisanlib.util |
| `src/artisanlib/devices.py` | 5122 | 107 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.device_registry, artisanlib.dialogs, artisanlib.main, artisanlib.qrcode, artisanlib.roasthubs, artisanlib.scale, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/dialogs.py` | 857 | 44 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/events.py` | 4023 | 120 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/events_editor_style.py` | 158 | 0 | None | artisanlib.util |
| `src/artisanlib/filters.py` | 279 | 13 | None |  |
| `src/artisanlib/giesen.py` | 185 | 1 | None | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/hibean.py` | 192 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/hottop.py` | 237 | 13 | None | artisanlib.async_comm, artisanlib.atypes |
| `src/artisanlib/ikawa.py` | 645 | 3 | PyQt6.QtCore | artisanlib.atypes, artisanlib.ble_port, artisanlib.util |
| `src/artisanlib/kaleido.py` | 926 | 40 | None | artisanlib.async_comm, artisanlib.atypes, artisanlib.util |
| `src/artisanlib/large_lcds.py` | 963 | 69 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/lebrew.py` | 227 | 26 | None | artisanlib.async_comm, artisanlib.ble_port |
| `src/artisanlib/logs.py` | 159 | 11 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib, artisanlib.dialogs, artisanlib.main, artisanlib.widgets |
| `src/artisanlib/loring.py` | 284 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/main.py` | 28236 | 682 | PyQt6, PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtNetwork, PyQt6.QtPrintSupport, PyQt6.QtWidgets | artisanlib, artisanlib.alarms, artisanlib.atypes, artisanlib.autosave, artisanlib.axis, artisanlib.background, artisanlib.batches, artisanlib.bluedot, artisanlib.button_style, artisanlib.calculator, artisanlib.canvas, artisanlib.comm, artisanlib.comparator, artisanlib.cropster, artisanlib.cup_profile, artisanlib.curves, artisanlib.device_registry, artisanlib.devices, artisanlib.dialogs, artisanlib.events, artisanlib.events_editor_style, artisanlib.giesen, artisanlib.hibean, artisanlib.hottop, artisanlib.ikawa, artisanlib.kaleido, artisanlib.large_lcds, artisanlib.lebrew, artisanlib.logs, artisanlib.loring, artisanlib.modbusport, artisanlib.mqttport, artisanlib.mugma, artisanlib.notifications, artisanlib.orbiter, artisanlib.petroncini, artisanlib.phases, artisanlib.phases_canvas, artisanlib.pid_control, artisanlib.pid_dialogs, artisanlib.platformdlg, artisanlib.ports, artisanlib.qtsingleapplication, artisanlib.roast_properties, artisanlib.roasthubs, artisanlib.roastlog, artisanlib.roest, artisanlib.rubasse, artisanlib.s7port, artisanlib.sampling, artisanlib.santoker, artisanlib.santoker_r, artisanlib.scale, artisanlib.simulator, artisanlib.slider_style, artisanlib.statistics, artisanlib.stronghold, artisanlib.suppress_errors, artisanlib.transposer, artisanlib.util, artisanlib.weblcds, artisanlib.wheels, artisanlib.widgets, artisanlib.wsport, plus.blend, plus.config, plus.connection, plus.controller, plus.notifications, plus.queue, plus.register, plus.schedule, plus.stock, plus.sync, plus.util |
| `src/artisanlib/modbusport.py` | 1125 | 48 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.async_comm, artisanlib.main, artisanlib.util |
| `src/artisanlib/mqttport.py` | 317 | 14 | PyQt6.QtWidgets | artisanlib.main, artisanlib.util |
| `src/artisanlib/mugma.py` | 120 | 10 | None | artisanlib.async_comm |
| `src/artisanlib/notifications.py` | 398 | 33 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.qtsingleapplication, artisanlib.util, plus.config, plus.connection, plus.util |
| `src/artisanlib/orbiter.py` | 769 | 30 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.async_comm, artisanlib.atypes, artisanlib.main, artisanlib.util |
| `src/artisanlib/petroncini.py` | 212 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/phases.py` | 374 | 18 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main |
| `src/artisanlib/phases_canvas.py` | 368 | 9 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.main, artisanlib.suppress_errors, artisanlib.util |
| `src/artisanlib/phidgets.py` | 291 | 12 | PyQt6.QtCore |  |
| `src/artisanlib/pid.py` | 837 | 56 | PyQt6.QtCore | artisanlib.filters, artisanlib.suppress_errors |
| `src/artisanlib/pid_control.py` | 2035 | 59 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.button_style, artisanlib.main, artisanlib.util |
| `src/artisanlib/pid_dialogs.py` | 4833 | 148 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/platformdlg.py` | 125 | 1 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib, artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/ports.py` | 2043 | 27 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.comm, artisanlib.device_registry, artisanlib.dialogs, artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/qcheckcombobox.py` | 450 | 22 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets |  |
| `src/artisanlib/qrcode.py` | 79 | 7 | PyQt6.QtCore, PyQt6.QtGui |  |
| `src/artisanlib/qtsingleapplication.py` | 173 | 10 | PyQt6.QtCore, PyQt6.QtNetwork, PyQt6.QtWidgets | artisanlib.main |
| `src/artisanlib/roast_properties.py` | 5982 | 232 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.table_style, artisanlib.util, artisanlib.widgets, plus.blend, plus.config, plus.controller, plus.queue, plus.stock, plus.util |
| `src/artisanlib/roasthubs.py` | 310 | 10 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib, artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/roastlog.py` | 271 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/roastpath.py` | 346 | 1 | PyQt6.QtCore | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/roest.py` | 597 | 8 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/rubasse.py` | 272 | 1 | None | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/s7client.py` | 35 | 2 | None |  |
| `src/artisanlib/s7port.py` | 764 | 21 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.main, artisanlib.s7client, artisanlib.util |
| `src/artisanlib/sampling.py` | 145 | 5 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.widgets |
| `src/artisanlib/santoker.py` | 431 | 26 | None | artisanlib.async_comm, artisanlib.atypes, artisanlib.ble_port |
| `src/artisanlib/santoker_r.py` | 105 | 8 | None | artisanlib.ble_port |
| `src/artisanlib/scale.py` | 665 | 73 | PyQt6.QtCore | artisanlib.acaia |
| `src/artisanlib/simulator.py` | 173 | 4 | None | artisanlib.util |
| `src/artisanlib/slider_style.py` | 113 | 0 | None |  |
| `src/artisanlib/statistics.py` | 804 | 31 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/artisanlib/stronghold.py` | 172 | 1 | None | artisanlib.atypes, artisanlib.util |
| `src/artisanlib/suppress_errors.py` | 97 | 3 | None |  |
| `src/artisanlib/table_style.py` | 74 | 2 | None | artisanlib.util |
| `src/artisanlib/time.py` | 56 | 7 | None |  |
| `src/artisanlib/transposer.py` | 1269 | 46 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/util.py` | 2202 | 97 | PyQt6.QtCore, PyQt6.QtGui | artisanlib.atypes, artisanlib.main |
| `src/artisanlib/weblcds.py` | 304 | 25 | None |  |
| `src/artisanlib/wheels.py` | 675 | 34 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util |
| `src/artisanlib/widgets.py` | 691 | 67 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.util |
| `src/artisanlib/wsport.py` | 416 | 16 | PyQt6.QtWidgets | artisanlib, artisanlib.main |
| `src/help/__init__.py` | 0 | 0 | None |  |
| `src/help/alarms_help.py` | 86 | 1 | PyQt6.QtWidgets |  |
| `src/help/autosave_help.py` | 140 | 1 | PyQt6.QtWidgets |  |
| `src/help/energy_help.py` | 82 | 1 | PyQt6.QtWidgets |  |
| `src/help/eventannotations_help.py` | 76 | 1 | PyQt6.QtWidgets |  |
| `src/help/eventbuttons_help.py` | 278 | 1 | PyQt6.QtWidgets |  |
| `src/help/eventsliders_help.py` | 185 | 1 | PyQt6.QtWidgets |  |
| `src/help/keyboardshortcuts_help.py` | 134 | 1 | PyQt6.QtWidgets |  |
| `src/help/modbus_help.py` | 30 | 1 | PyQt6.QtWidgets |  |
| `src/help/mqtt_help.py` | 25 | 1 | PyQt6.QtWidgets |  |
| `src/help/programs_help.py` | 26 | 1 | PyQt6.QtWidgets |  |
| `src/help/s7_help.py` | 29 | 1 | PyQt6.QtWidgets |  |
| `src/help/symbolic_help.py` | 202 | 1 | PyQt6.QtWidgets |  |
| `src/help/transposer_help.py` | 36 | 1 | PyQt6.QtWidgets |  |
| `src/plus/__init__.py` | 2 | 0 | None |  |
| `src/plus/account.py` | 149 | 2 | PyQt6.QtCore | artisanlib.util, plus |
| `src/plus/blend.py` | 452 | 31 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets |
| `src/plus/config.py` | 151 | 0 | None | artisanlib.main |
| `src/plus/connection.py` | 524 | 13 | PyQt6.QtCore | artisanlib, plus |
| `src/plus/controller.py` | 468 | 10 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.main, plus, plus.login |
| `src/plus/countries.py` | 313 | 0 | PyQt6.QtWidgets |  |
| `src/plus/login.py` | 297 | 6 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtSvgWidgets, PyQt6.QtWidgets | artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets, plus |
| `src/plus/notifications.py` | 132 | 3 | PyQt6.QtCore | artisanlib.notifications, plus |
| `src/plus/queue.py` | 511 | 13 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.util, plus |
| `src/plus/register.py` | 212 | 3 | PyQt6.QtCore | artisanlib.util, plus |
| `src/plus/roast.py` | 555 | 4 | None | artisanlib.atypes, artisanlib.util, plus |
| `src/plus/schedule.py` | 4421 | 192 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.dialogs, artisanlib.main, artisanlib.util, artisanlib.widgets, plus.config, plus.connection, plus.controller, plus.register, plus.stock, plus.sync, plus.util, plus.weight |
| `src/plus/stock.py` | 1790 | 58 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.util, plus |
| `src/plus/sync.py` | 960 | 17 | PyQt6.QtCore, PyQt6.QtWidgets | artisanlib.util, plus |
| `src/plus/util.py` | 452 | 42 | PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets | artisanlib.atypes, artisanlib.util, plus |
| `src/plus/weight.py` | 1873 | 114 | PyQt6.QtCore | artisanlib.main, artisanlib.scale |
| `src/proto/__init__.py` | 2 | 0 | None |  |
| `src/proto/artisan_roast_pb2.py` | 44 | 0 | None |  |
| `src/proto/IkawaCmd_pb2.py` | 67 | 0 | None |  |
| `src/uic/__init__.py` | 2 | 0 | None |  |
| `src/uic/BlendDialog.py` | 100 | 2 | PyQt6 |  |
| `src/uic/EnergyWidget.py` | 1378 | 2 | PyQt6 | artisanlib.widgets |
| `src/uic/MeasureDialog.py` | 182 | 2 | PyQt6 |  |
| `src/uic/SetupWidget.py` | 206 | 2 | PyQt6 |  |
| `src/uic/SliderCalculatorDialog.py` | 172 | 2 | PyQt6 |  |
