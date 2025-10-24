import requests
import json
from colorama import Fore, Style, init
from pyfiglet import figlet_format

# Initialize colorama
init(autoreset=True)

class WeatherApp:
    def __init__(self):
        self.API_KEY = "1f626ad2308680eebdbd773c00935264"
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.FILE_NAME = "pakistan_weather.txt"
        self.user_name = ""

    def neon_print(self, text, color=Fore.MAGENTA, delay=0.02):
        """Print text with glowing neon animation."""
        for char in text:
            print(color + char, end="", flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)

    def banner(self):
        """Display neon-style banner."""
        print(Fore.CYAN + Style.BRIGHT)
        print(figlet_format("WEATHER CLI APPLICATION", font="digital"))
        print(Fore.LIGHTMAGENTA_EX + "✨ Made by Abdul Wajid Halepoto ✨")
        print(Fore.YELLOW + "----------------------------------------------\n")

    def get_weather(self, city):
        """Fetch weather data."""
        try:
            params = {"q": f"{city},PK", "appid": self.API_KEY, "units": "metric"}
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()

            if data.get("cod") == "404":
                self.neon_print(f"❌ '{city}' not found in Pakistan.", Fore.RED)
                self.neon_print("💡 Tip: Try another nearby city.\n", Fore.YELLOW)
                return None

            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize()
            }

        except requests.exceptions.RequestException:
            self.neon_print("⚠️ Internet connection error.", Fore.RED)
            return None

    def save_to_file(self, weather):
        """Save weather to file."""
        with open(self.FILE_NAME, "a", encoding="utf-8") as file:
            json.dump(weather, file)
            file.write("\n")
        self.neon_print("💾 Saved to 'pakistan_weather.txt'.", Fore.CYAN)

    def show_history(self):
        """Display saved weather data."""
        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if not lines:
                    self.neon_print("⚠️ No weather history found yet.", Fore.YELLOW)
                    return

                self.neon_print("\n📜 Saved Weather History:\n", Fore.MAGENTA)
                for line in lines:
                    record = json.loads(line)
                    print(Fore.GREEN + f"{record['city']}, {record['country']}: "
                          f"{record['temp']}°C, {record['description']}")
                print()
        except FileNotFoundError:
            self.neon_print("⚠️ No weather history found yet.", Fore.YELLOW)

    def run(self):
        """Main program."""
        self.banner()
        self.user_name = input(Fore.LIGHTGREEN_EX + "Enter your name: ").strip() or "User"
        self.neon_print(f"\n👋 Welcome, {self.user_name}! Let's check the weather in Pakistan.\n", Fore.GREEN)

        while True:
            print(Fore.CYAN + "Choose an option:")
            print(Fore.LIGHTYELLOW_EX + "1️⃣  Enter your city")
            print("2️⃣  Show saved history")
            print("3️⃣  Exit")

            choice = input(Fore.LIGHTBLUE_EX + "\nEnter your choice (1/2/3): ").strip()

            if choice == "1":
                city = input(Fore.LIGHTCYAN_EX + "Enter Pakistani city name: ").strip()
                weather = self.get_weather(city)
                if weather:
                    print(Fore.LIGHTMAGENTA_EX + f"\n🌆 Weather in {weather['city']}, {weather['country']}:")
                    print(Fore.LIGHTRED_EX + f"🌡 Temperature: {weather['temp']}°C "
                          f"(Feels like {weather['feels_like']}°C)")
                    print(Fore.LIGHTBLUE_EX + f"💧 Humidity: {weather['humidity']}%")
                    print(Fore.LIGHTGREEN_EX + f"☁️ Condition: {weather['description']}\n")
                    self.save_to_file(weather)

            elif choice == "2":
                self.show_history()

            elif choice == "3":
                self.neon_print(f"👋 Goodbye, {self.user_name}! Stay safe 🌤️\n", Fore.LIGHTYELLOW_EX)
                break

            else:
                self.neon_print("⚠️ Invalid choice! Please select 1, 2, or 3.\n", Fore.RED)


# --- Run the app ---
if __name__ == "__main__":
    app = WeatherApp()
    app.run()