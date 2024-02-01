# Data Lifecycle: Generation and Collection,
# using user input for generation and untyped Python tuples for collection.
if __name__ == "__main__":
    readings = int(input("How many weather readings? "))
    all_readings = []

    for i in range(readings):
        temperature = float(input("Enter temperature: "))
        pressure = float(input("Enter pressure: "))
        humidity = float(input("Enter humidity: "))

        # Construct a tuple to contain the three readings and append it to the list.
        reading = (temperature, pressure, humidity)
        all_readings.append(reading)


    # Echo the input to output.
    print("Your readings:")
    for reading in all_readings:
        print(f"\tTemp: {reading[0]}", end="")
        print(f"\tPresure: {reading[1]}", end="")
        print(f"\tHumidity: {reading[2]}")