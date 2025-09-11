import boot
from utilities.timeout_input import input_with_timeout
from tests import m0_bootstrap
from tests import m1_wifi_http
from tests import m2_weather_service
from tests import m3_ambient_controller

def main():
    select = input_with_timeout(prompt="Press Enter to enter debug mode (or wait 3s for default boot): ", timeout=3, default="n") == ""

    if not select:
        boot.main()
        return

    all_tests = input_with_timeout("Run all tests? (y/n): ", timeout=5, default="n").strip().lower() == 'y'

    if not all_tests:
        m0 = input("Run m0_bootstrap? [LED builtin test] (y/n): ").strip().lower() == 'y'
        m1 = input("Run m1_wifi_http? [Connection and HTTP test](y/n): ").strip().lower() == 'y'
        m2 = input("Run m2_weather_service? [Weather fetch test](y/n): ").strip().lower() == 'y'
        m3 = input("Run m3_ambient_controller? [Ambient light control test](y/n): ").strip().lower() == 'y'
    
    if all_tests or m0:
        print("=== Running m0_bootstrap ===")
        m0_bootstrap.main()
    
    if all_tests or m1:
        print("=== Running m1_wifi_http ===")
        m1_wifi_http.main()

    if all_tests or m2:
        print("=== Running m2_weather_service ===")
        m2_weather_service.main(location="D")
    
    if all_tests or m3:
        print("=== Running m3_ambient_controller ===")
        m3_ambient_controller.main()


if __name__ == "__main__":
    main()