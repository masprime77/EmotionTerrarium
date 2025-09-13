from config import COLOR_EMOTION_DEFAULT, COLOR_HAPPY, COLOR_SAD, COLOR_ANGRY, COLOR_DISGUST, COLOR_FEAR, COLOR_ANXIETY, COLOR_ENVY, COLOR_EMBARRASSMENT, COLOR_BORED

EMOTION_MAP = {
    "default": COLOR_EMOTION_DEFAULT,
    "happy": COLOR_HAPPY,
    "sad": COLOR_SAD,
    "angry": COLOR_ANGRY,
    "disgust" : COLOR_DISGUST,
    "fear": COLOR_FEAR,
    "anxiety": COLOR_ANXIETY,
    "envy": COLOR_ENVY,
    "embarrassed": COLOR_EMBARRASSMENT,
    "bored": COLOR_BORED,
}

def color_for_emotion(label):
    label = str(label).strip().lower()
    try:
        return EMOTION_MAP.get(label, "Unknown")
    except:
        return "Unknown"