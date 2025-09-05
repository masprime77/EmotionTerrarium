*Here comes the project vision*

# Step 1: MVP Definition – EmotionalTerrarium

## Context

Many people want to feel connected to distant places and to visualize emotions in a tangible way. In the case of the group the neccesity of feeling the environment that our family in our home countries are experienceing.
The EmotionalTerrarium combines environmental data (weather) and personal emotional input into a physical, aesthetic object.

## Problem

- Weather data from distant cities feels abstract when only shown in apps or text.
- Emotional states are also abstract and often difficult to share visually.
- There is no simple, physical medium that merges *external* (climate) and *internal* (emotions) conditions.

## Target Users

- Students and researchers interested in IoT and HCI (Human-Computer Interaction).
- People who want an artistic object that connects emotions with the environment.
- Potentially museums, art installations, or home users seeking ambient displays.

## Main Use Cases

1. User selects a remote city → the terrarium displays its current weather.
2. User sets their emotional state → the central sphere lights up with a matching color.
3. Combined view: the terrarium shows *weather conditions* and *emotions* at the same time.

## Success Metrics

- Weather is displayed with at least 80% accuracy (clear, rain, snow, etc.).
- Emotion colors update instantly (<1s delay).
- System works continuously for at least 2 hours without manual reset.
- Users can correctly identify at least 3 emotions and 3 weather types.

## Assumptions & Risks

- **Assumptions:** Internet connection is available, sensors/actuators are reliable.
- **Risks:**
  - Scope creep if too many features are added.
  - Difficulty in defining universal mappings from emotions to colors.

## Out of Scope (for MVP)

- Complex emotion recognition (AI-based sentiment analysis).
- Long-term environmental regulation inside the terrarium.
- Mobile app integration.

## MVP Features (Must-Haves)

- WiFi connection to fetch weather data from a remote city.
- LEDs to represent weather (e.g., sunny = yellow/white, cloudy = gray/blue, rain = blue blinking, snow = white).
- Temperature control (basic: heating element or fan).
- Central RGB sphere for emotions (user chooses color manually).
- Basic documentation and demo.
