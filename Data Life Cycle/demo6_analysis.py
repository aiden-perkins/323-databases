# Data Lifecycle: Storage.
# Reading from a CSV file.
# and writing the validated data out using pickle
import pickle

from weatherreading import WeatherReading


def valid_temperature(temperature: float):
    return -40 < temperature < 85


def valid_pressure(pressure: float):
    return 300 < pressure < 1200


def valid_humidity(humidity: float):
    return 20 < humidity < 80


def max_temperature(readings: list[WeatherReading]):
    return max(*map(lambda a: a.temperature, readings))


def min_pressure(readings: list[WeatherReading]):
    return min(*map(lambda a: a.pressure, readings))


def max_humidity(readings: list[WeatherReading]):
    return max(*map(lambda a: a.humidity, readings))


def valid_reading(temperature: float, pressure: float, humidity: float):
    return valid_temperature(temperature) and valid_pressure(pressure) and valid_humidity(humidity)


def get_readings_from_file(filename: str, skip_first_line: bool) -> list[WeatherReading]:
    with open(filename) as file:
        # Note that we're stating that the list is a List of WeatherReading instances
        all_readings: list[WeatherReading] = []
        first_line = True

        for line in file:
            if skip_first_line and first_line:
                first_line = False
                continue

            split = line.split(",")
            temperature = float(split[0])
            pressure = float(split[1])
            humidity = float(split[2])
            if valid_reading(temperature, pressure, humidity):
                reading = WeatherReading(temperature, pressure, humidity)
                all_readings.append(reading)
    
        return all_readings


if __name__ == "__main__":
    file_name = input("Enter CSV file name: ")
    weather_readings = get_readings_from_file(file_name, True)

    # Echo the input to output.
    print("Your readings:")
    for weather_reading in weather_readings:
        print(f"\tTemp: {weather_reading.temperature}", end="")
        print(f"\tPressure: {weather_reading.pressure}", end="")
        print(f"\tHumidity: {weather_reading.humidity}")

    print(max_temperature(weather_readings))
    print(min_pressure(weather_readings))
    print(max_humidity(weather_readings))

    pickle_demo = open('pickle_demo.bin', 'wb')
    pickle.dump(weather_readings, pickle_demo)
    pickle_demo.close()
