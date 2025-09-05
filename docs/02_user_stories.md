# Step 2: User Stories – EmotionalTerrarium

## Introduction

User stories describe the system from the perspective of its users.
They capture *who* the user is, *what* they want, and *why* it matters.
Each story includes **acceptance criteria** that define when the story is considered done.

## User Stories

### Story 1 – Select a remote city

**As a** user
**I want** to select a remote city
**So that** I can see its real-time weather represented in the terrarium.

*Acceptance Criteria:*

- Given the device is connected to WiFi
- When I choose a valid city (e.g., Darmstadt)
- Then the terrarium updates to show the current weather.

---

### Story 2 – Display weather conditions

**As a** user
**I want** the terrarium lights and temperature to reflect weather conditions
**So that** I can perceive the environment of the selected city.

*Acceptance Criteria:*

- Given the system fetches weather data
- When the weather is “Clear sky”
- Then the LEDs display a warm white/yellow pattern.
- Given the weather is “Rain”
- Then the LEDs display a blue pulsing pattern.
- Additional acceptance criteria will be defined for other conditions such as snow, fog, and drizzle.

---

### Story 3 – Set my emotional state

**As a** user
**I want** to set my emotion and see it as a color in the central sphere
**So that** my mood is represented visually.

*Acceptance Criteria:*

- Given the system is on
- When I select “happy”
- Then the sphere glows green within 1 second.
- When I select “calm”
- Then the sphere glows blue.
- When I select “angry”
- Then the sphere glows red.

---

### Story 4 – Combine weather and emotion

**As a** user
**I want** the terrarium to show both the weather and my emotion at the same time
**So that** the system reflects the external and internal states together.

*Acceptance Criteria:*

- Given weather data and an emotion are set
- When both are active
- Then the weather pattern shows on the LEDs and the sphere displays the emotion color simultaneously.

---

### Story 5 – Recover from connection loss

**As a** user
**I want** the terrarium to reconnect automatically when WiFi is lost
**So that** I don’t need to restart it manually.

*Acceptance Criteria:*

- Given the WiFi connection drops
- When it becomes available again
- Then the device reconnects within 2 minutes without user intervention.

---

### Story 6 – Flexible weather source

**As a** user
**I want** the terrarium to support different ways of selecting the weather source
**So that** I can still use it even if automatic detection is not available.

*Acceptance Criteria:*

- Given I want to manually select the location
- When I enter a city (e.g., Darmstadt)
- Then the terrarium fetches and displays its current weather.
- Given I have internet access
- When I enable “location by IP”
- Then the system fetches weather automatically from my current location.
- Given I want the terrarium to reflect my immediate environment
- When the local sensor is active
- Then the terrarium uses ambient conditions as the weather source.

---

### Story 7 – Demo mode

**As a** presenter
**I want** a demo mode that cycles through weather patterns and emotions
**So that** I can showcase the project without needing live data or internet.

*Acceptance Criteria:*

- Given the device is offline
- When I enable demo mode
- Then the terrarium cycles through at least 3 weather conditions and 3 emotions in a loop.
- When demo mode is disabled
- Then the system returns to normal operation (real weather + selected emotion).

---

## Notes

- Stories will later be broken down into **tasks** in the coding roadmap.
- Additional stories can be added in future iterations if needed.
