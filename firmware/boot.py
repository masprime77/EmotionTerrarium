from tests import m0_bootstrap
from tests import m1_wifi_http
from tests import m2_weather_service
from tests import m3_ambient_controller
from tests import m4_step1_ping
from tests import m4_step2_emotion

# === DEV OPTIONS ===
DEBUG = False
M0_TEST = False
M1_TEST = False
M2_TEST = False
M3_TEST = False
M4_S1_TEST = False
M4_S2_TEST = True

def main():
    if DEBUG:
        if M0_TEST:
            print("=== Running m0_bootstrap ===")
            m0_bootstrap.main()
        
        if M1_TEST:
            print("=== Running m1_wifi_http ===")
            m1_wifi_http.main()

        if M2_TEST:
            print("=== Running m2_weather_service ===")
            m2_weather_service.main(location="D")
        
        if M3_TEST:
            print("=== Running m3_ambient_controller ===")
            m3_ambient_controller.main()

        if M4_S1_TEST:
            print("=== Running m4_step1_ping ===")
            m4_step1_ping.main()

        if M4_S2_TEST:
            print("=== Running m4_step2_emotion ===")
            m4_step2_emotion.main()

        return
    
if __name__ == "__main__":
    main()