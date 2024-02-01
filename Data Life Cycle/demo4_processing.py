# Data Lifecycle: Processing.
# Filtering bad readings from input.
from weatherreading import WeatherReading


def valid_temperature(temperature : float):
    return -40 < temperature < 85


def valid_pressure(pressure : float):
    return 300 < pressure < 1200


def valid_humidity(humidity : float):
    return 20 < humidity < 80

def valid_reading(temperature : float, pressure : float, humidity : float):
    return valid_temperature(temperature) and valid_pressure(pressure) and valid_humidity(humidity)

if __name__ == "__main__":
    readings = int(input("How many weather readings? "))
    all_readings : list[WeatherReading] = []

    for i in range(readings):
        temperature = float(input("Enter temperature: "))
        pressure = float(input("Enter pressure: "))
        humidity = float(input("Enter humidity: "))

        # Construct a tuple to contain the three readings and append it to the list
        if valid_reading(temperature, pressure, humidity):
            reading = WeatherReading(temperature, pressure, humidity)
            all_readings.append(reading)


    # Echo the input to output.
    print("Your readings:")
    for reading in all_readings:
        print(f"\tTemp: {reading.temperature}", end="")
        print(f"\tPressure: {reading.pressure}", end="")
        print(f"\tHumidity: {reading.humidity}")