class WeatherReading:
    def __init__(self, temperature : float, pressure : float, humidity : float):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity

    def temperature_celcius(self) -> float:
        return (self.temperature - 32) * 5 / 9
