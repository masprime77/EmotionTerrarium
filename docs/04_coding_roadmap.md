*Step by step code implementation*

# Step 4: Coding Roadmap – EmotionalTerrarium

## Introduction

The coding roadmap describes how the EmotionalTerrarium will be implemented step by step.
It translates user stories and architecture into concrete milestones, coding tasks, and acceptance criteria.
This ensures the development stays organized, avoids missing features, and allows incremental testing.

---

## 1. Definition of Done (DoD)

A feature is considered done when:

- All acceptance criteria are met.
- The code runs without crashes in the normal workflow.
- Error handling is implemented (no silent failures).
- Logs are printed for major events (connect, fetch, update).
- Configuration files are externalized (`config.json` not committed).
- Documentation is updated (README and `/docs`).

---

## 2. Milestones & Vertical Slices

### M0 — Bootstrap (repo + hello hardware)

**import timeUser value:** Board blinks to confirm setup.

- Create firmware structure (`/drivers`, `/services`, `/config`, `/controllers`).
- Implement `drivers/led_builtin.py` for on-board LED.
- `main.py`: loop at 1 Hz → blink LED.

*Acceptance Criteria:*

- On boot, LED blinks for 5 seconds.
- No exceptions after 2 minutes idle.

---

### M1 — Wi-Fi & HTTP

**User value:** Device connects to internet.

- `services/wifi.py`: connect with retries, log IP.
- `services/http.py`: helper to fetch JSON from URL.
- `config/config.json` for WiFi credentials.

*Acceptance Criteria:*

- On boot, prints: `[WiFi] Connected. IP: …`.
- HTTP GET to test URL returns JSON or logs error.

---

### M2 — Weather Service

**User value:** Device understands sky state.

- `services/weather_service.py`: fetch city weather via API.
- `services/mapping_wmo.py`: map WMO codes → labels (clear, rain, snow…).
- Basic caching of last result.

*Acceptance Criteria:*

- Given a known latitude and longitude, `weather_service` returns `{wmo, label, temp, humidity, time}`.
- On API failure, cached result (<15 min old) is returned.

---

### M3 — Weather → LED Patterns

**User value:** Weather is visible in the terrarium.

- `controllers/ambient_controller.py`: render LED ring for each condition.
- Example mapping:
  - Clear → warm white
  - Cloudy → soft blue
  - Rain → pulsing blue
  - Snow → cold white

*Acceptance Criteria:*

- For each condition, LEDs show the expected pattern.
- Stable for at least 5 minutes.

---

### M4 — Emotion Input

**User value:** User sets mood color.

- `services/emotion_service.py`: map emotion → RGB.
- Input method (first via serial command, later via button or UI).

*Acceptance Criteria:*

- When sending `emotion:happy`, sphere turns green in <1s.
- Weather pattern continues running in background.

---

### M5 — Combine Weather + Emotion

**User value:** Both are visible together.

- Merge weather LEDs with emotion sphere.
- Update weather every 10 min; emotion instantly.
- Non-blocking main loop.

*Acceptance Criteria:*

- Emotion updates do not block weather updates.
- System stable for 30 minutes.

---

### M6 — Flexible Weather Source

**User value:** Choose source of weather data.

- Support manual city input, IP-based location, or local sensor.
- Extend `weather_service` with three providers.

*Acceptance Criteria:*

- Manual city fetch works (e.g., Darmstadt).
- IP-based fetch works with internet.
- Local sensor can override API when enabled.

---

### M7 — Demo Mode

**User value:** Showcase project offline.

- Add demo mode cycling through 3 weather patterns + 3 emotions.
- Toggle via config flag or command.

*Acceptance Criteria:*

- When offline, demo mode runs loop.
- When disabled, system returns to real data.

---

### M8 — Resilience & Polishing

**User value:** Reliable experience.

- Auto-reconnect WiFi.
- Watchdog for loop.
- Heartbeat LED to indicate alive status.
- Serial command `status?` prints JSON.

*Acceptance Criteria:*

- Disconnect/reconnect WiFi works automatically.
- `status?` returns valid JSON with uptime + last weather.

---

## 3. Issue Templates

All milestones will be tracked as GitHub issues.
Example template:

```markdown
## Feature
<short description>

## Acceptance Criteria
- [ ] Given … when … then …

## Tasks
- [ ] Code
- [ ] Test
- [ ] Docs
```
