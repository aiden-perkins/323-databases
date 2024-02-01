# Data Lifecycle: Generation and Collection, demo 2,
# using user input for generation and type-annotated Python class for collection.
from weatherreading import WeatherReading

if __name__ == "__main__":
    readings = int(input("How many weather readings? "))
    all_readings : list[WeatherReading] = []

    for i in range(readings):
        temperature = float(input("Enter temperature: "))
        pressure = float(input("Enter pressure: "))
        humidity = float(input("Enter humidity: "))

        # Construct a tuple to contain the three values and append it to the list.
        reading = WeatherReading(temperature, pressure, humidity)
        all_readings.append(reading)


    # Echo the input to output.
    print("Your readings:")
    for reading in all_readings:
        print(f"\tTemp: {reading.temperature}", end="")
        print(f"\tPressure: {reading.pressure}", end="")
        print(f"\tHumidity: {reading.humidity}")