# Boards performance smoke test

## Run (non-GUI)

```bash
jmeter -n -t perf/boards_smoke.jmx -l reports/boards_smoke.jtl
```

Windows example (JMeter installed at E:\apache-jmeter-5.6.3):

```powershell
& "E:\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t perf/boards_smoke.jmx -l reports/boards_smoke.jtl
```

## Generate HTML dashboard report

```bash
jmeter -g reports/boards_smoke.jtl -o reports/boards_smoke_html
```

Windows example:

```powershell
& "E:\apache-jmeter-5.6.3\bin\jmeter.bat" -g reports/boards_smoke.jtl -o reports/boards_smoke_html
```

If the output folder already exists, JMeter will fail. Remove it first or pick a new output folder:

```powershell
Remove-Item -Recurse -Force reports\boards_smoke_html
& "E:\apache-jmeter-5.6.3\bin\jmeter.bat" -g reports/boards_smoke.jtl -o reports/boards_smoke_html
```

## Scenario
- 20 VUs
- 2-minute ramp-up
- 3-minute steady duration
- Flow: login -> create board -> create 2 cards -> move 1 card -> GET /boards

## Thresholds (documented targets)
- p95 < 800ms for GET /boards
- error rate < 1%

Notes:
- API target defaults to `http://localhost:8000/api/v1` via variables in the JMX.
- Adjust `API_HOST`/`API_PORT` in the JMX if needed.
