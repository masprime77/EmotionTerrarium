# 🌍 EmotionalTerrarium – Visual Representation of Weather Conditions

This document describes how to represent the **most common weather conditions** with **RGB lights** and **wind effects** in the *EmotionalTerrarium* project.

---

## ☀️ Clear and Cloudy Skies

| Code | Condition         | Suggested RGB       | Light Effect                        | Wind         |
|------|------------------|---------------------|-------------------------------------|--------------|
| 0    | Clear sky        | (255, 255, 200)     | Warm fixed light (sun)              | None         |
| 1    | Mainly clear     | (255, 255, 220) + (180, 200, 255) | Warm light with soft blue sparkles | None         |
| 2    | Partly cloudy    | (200, 200, 255)     | White/blue mix, slow fading         | None         |
| 3    | Overcast         | (150, 150, 180)     | Diffused gray-blue uniform light    | None         |

---

## 🌫️ Fog

| Code | Condition                  | Suggested RGB   | Light Effect                        | Wind              |
|------|----------------------------|-----------------|-------------------------------------|-------------------|
| 45/48| Fog / Rime fog             | (220, 220, 220) | Slow fade in/out, diffuse effect    | Fan on low speed  |

---

## 🌧️ Rain and Drizzle

| Code        | Condition                  | Suggested RGB   | Light Effect                         | Wind             |
|-------------|----------------------------|-----------------|--------------------------------------|------------------|
| 51–55       | Drizzle (light to dense)  | (150, 200, 255) | Light blue, irregular flicker        | None             |
| 61–65       | Rain (light to heavy)     | (50, 100, 255)  | Intense blue, stronger flicker       | Gentle bursts    |
| 80–82       | Rain showers (light to violent) | (0, 80, 255) | Bright blue with quick white flashes | Moderate bursts  |

---

## ❄️ Snow

| Code | Condition               | Suggested RGB   | Light Effect                          | Wind             |
|------|-------------------------|-----------------|---------------------------------------|------------------|
| 71–75| Snow fall (light-heavy) | (240, 240, 255) | Cold white, slow flicker              | None             |
| 85–86| Snow showers            | (200, 220, 255) | White/blue mix, short sparkles        | Gentle bursts    |
| 77   | Snow grains             | (255, 255, 255) | Cold white with quick “sparkling” flicker | None         |

---

## 🌩️ Thunderstorms

| Code | Condition                   | Suggested RGB          | Light Effect                           | Wind                 |
|------|-----------------------------|------------------------|----------------------------------------|----------------------|
| 95   | Thunderstorm                | (80, 0, 120)           | Dark blue/purple with violent white flashes | Strong bursts     |
| 96–99| Thunderstorm with hail      | (100, 100, 255) + (255, 255, 255) | Same as above + rapid white/icy flashes | Irregular strong bursts |

---

## 🌬️ Wind Intensity (general)

- **Light breeze:** fan at low speed, constant.  
- **Moderate wind:** bursts every few seconds.  
- **Strong wind / storm:** rapid, unpredictable bursts.  

---

## 💡 Implementation Notes
- Combine **colors + light effects (flicker, fade, flashes)** with **fan control**.  
- Use mixed patterns for combined conditions (e.g., partly cloudy + rain, snow + wind).  
- Scale **flicker/wind intensity** with the severity of the weather condition.  

---