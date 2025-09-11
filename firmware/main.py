from config import DEBUG, M0_TEST, M1_TEST, M2_TEST, M3_TEST
import default_boot
from tests import m0_bootstrap
from tests import m1_wifi_http
from tests import m2_weather_service
from tests import m3_ambient_controller
    
def main():
    if not DEBUG:
        default_boot.main()

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


if __name__ == "__main__":
    main()