from mrjob.job import MRJob
from mrjob.step import MRStep

class ClimateAnalysis(MRJob):
    """
    A MapReduce job to analyze climate data.
    - Mapper: Emits the region and temperature.
    - Reducer: Calculates the average temperature for each region.
    """

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_temps,
                   reducer=self.reducer_avg_temp)
        ]

    def mapper_get_temps(self, _, line):
        """
        Mapper to parse CSV lines and emit temperature data for each region.
        It gracefully handles header rows, malformed lines, and missing temperature values.
        """
        try:
            # Split the CSV line
            parts = line.split(',')
            
            # Assuming the structure: timestamp,region,temperature,humidity,pressure
            if len(parts) == 5:
                region = parts[1]
                temperature_str = parts[2]

                # Skip the header row
                if region == 'region':
                    return

                # Ensure temperature is a valid float
                if temperature_str:
                    temperature = float(temperature_str)
                    yield region, temperature
        except (ValueError, IndexError):
            # This will catch errors from trying to float() a non-numeric string
            # or index errors from malformed lines. We simply ignore these lines.
            self.increment_counter('errors', 'malformed_line', 1)

    def reducer_avg_temp(self, region, temps):
        """
        Reducer to calculate the average temperature for a given region.
        It sums up all temperatures and divides by the count.
        """
        total_temp = 0
        count = 0
        for temp in temps:
            total_temp += temp
            count += 1
        
        # Avoid division by zero if a region has no valid temperature data
        if count > 0:
            average_temp = total_temp / count
            yield region, round(average_temp, 2)

if __name__ == '__main__':
    ClimateAnalysis.run()
