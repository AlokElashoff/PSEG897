# Planetary Dataset
Anjali Kantharuban, Alok Elashoff, Rushil Kapadia, Nikhil Mandava, and Jinyoung Bae

## Description

Our project provides a tool to use get positional information about the eight planets in our solar system given a specific time range in YYY-MM-DD form and position in latitude and longtitude. We return the azimuth, altitude measurements as well as the right ascention and declination for an alternate measurement. The distance of the planet is also provided. 

We provide the option to further get data that would be representitive of that of ancient civilizations by providing an option to add the tools used during measurement, adding relevant error to the fields that would have been introduced by those tools.

Lastly, with a image flag, we allow the creating of a night sky image to be generated form the specific (possibly tool generated) data providing a realistic depiction of what the data at the time with specific tools could look like in the form of planets in the night sky. We furthermore provide another class to create a video from the generated images, creating a depiction of the night over the given timespan in the form of planetal positions. 
## Requirenments 

We provide a requirenments.txt. Run: 
```
pip install -r requirenments.txt 
```
to make sure you have all necessary requirenments to run the project.


## Generating Data

This dataset contains a list of planetary data in the following format:
```
{
  'time': "YYYY-MM-DD",
  'image': "image_folder/YYYY-MM-DD.png",
  'planet_data': {
    'mercury': {
      'az': azimuth,
      'alt': altitude,
      'ra': right_ascension,
      'dec': declination,
      'dist': distance
    }
    ...
  }
}
```

There are seven available planets - Mercury, Venus, Mars, Jupiter, Saturn, Neptune, and Uranus. When generating this dataset with default arguments, only the first five are included because before the advent of modern instruments, Neptune and Uranus when not visible.

When generating the dataset with custom parameters there are a series of flags that can be used:
```
-h, --help            show this help message and exit
--T T                 The time from which you want to generate data in the
                        format YYYY-MM-DD
--dt DT               The timestep between data points in days.
--timesteps TIMESTEPS
                      The number of data points to generate.
--planets PLANETS [PLANETS ...]
                      Which planets out of (mercury, venus, mars, jupiter,
                      saturn, neptune, uranus) to include in the dataset.
--long LONG           The longitude of the location on earth the data is
                      observed from in degrees.
--lat LAT             The longitude of the location on earth the data is
                      observed from in degrees.
--alt_error ALT_ERROR
                      The maximum error in the measurement of altitude in
                      degrees.
--az_error AZ_ERROR   The maximum error in the measurement of azmith in
                      degrees.
--ra_error RA_ERROR   The maximum error in the measurement of right
                      ascension in hours.
--dec_error DEC_ERROR
                      The maximum error in the measurement of declination in
                      degrees.
--dist_error DIST_ERROR
                      The maximum error in the measurement of distance in
                      kilometers.
--data_file DATA_FILE
                      The data file to which the data json is stored.
--image               Generate images for each data point.
--image_folder IMAGE_FOLDER
                      The folder to which images are stored
```
