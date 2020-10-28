import os
import sys
import datetime
import tqdm
import json
import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load
from skyfield.api import Topos
from argparse import ArgumentParser
from generate_image import create_image

if __name__ == '__main__':

    ### Argument Parser ###
    parser = ArgumentParser()

    parser.add_argument('--T', help='The time from which you want to generate data in the format YYYY-MM-DD', default="2000-01-01")
    parser.add_argument('--dt', help='The timestep between data points in days.', default=30, type=int)
    parser.add_argument('--timesteps', help='The number of data points to generate.', default=100, type=int)

    parser.add_argument('--planets', help='Which planets out of (mercury, venus, mars, jupiter, saturn, neptune, uranus) to include in the dataset.', nargs='+', default=None)

    parser.add_argument('--long', help='The longitude of the location on earth the data is observed from in degrees.', default=20.5937, type=float)
    parser.add_argument('--lat', help='The longitude of the location on earth the data is observed from in degrees.', default=78.9629, type=float)

    parser.add_argument('--tools', help='The list of tools used to calculate error. You can add more tools in tools.json.', default=[], nargs='+')
    parser.add_argument('--tools_file', help='The json files that contain data about each tool,', default="tools.json")
    parser.add_argument('--alt_error', help='The maximum error in the measurement of altitude in degrees.', default=0.0, type=float)
    parser.add_argument('--az_error', help='The maximum error in the measurement of azmith in degrees.', default=0.0, type=float)
    parser.add_argument('--ra_error', help='The maximum error in the measurement of right ascension in hours.', default=0.0, type=float)
    parser.add_argument('--dec_error', help='The maximum error in the measurement of declination in degrees.', default=0.0, type=float)
    parser.add_argument('--dist_error', help='The maximum error in the measurement of distance in kilometers.', default=0.0, type=float)

    parser.add_argument('--data_file', help="The data file to which the data json is stored.", default="planet_data.json")

    parser.add_argument('--image', help='Generate images for each data point.', action='store_true')
    parser.add_argument('--image_folder', help='The folder to which images are stored', default='image_data')


    ### Initialize Variables ###
    args = parser.parse_args()
    raw_data = load('de422.bsp') # This will take a long time, but is only necessary once
    if args.image:
        try:
            os.mkdir(args.image_folder)
        except FileExistsError:
            pass

    ### Initalize Planet Information ###
    earth = raw_data['earth']
    possible_planets = ['mercury', 'mars', 'venus', 'jupiter', 'saturn', 'neptune', 'uranus']
    longitude = str(args.long) + ' N'
    latitude = str(args.lat) + ' E'
    position = earth + Topos('20.5937 N', '78.9629 E')
    planets = ['mercury', 'mars', 'venus', 'jupiter', 'saturn'] if not args.planets else [planet.lower() for planet in args.planets]
    for planet in planets:
        if planet not in possible_planets:
            raise ValueError('One or more planets you have passed in are not valid arguments.')
    ts = load.timescale()

    ### Set Up Time Data ###
    t = datetime.datetime.strptime(args.T, "%Y-%m-%d")
    t_delta = datetime.timedelta(days=args.dt)

    ### Define Error For Each Measurement Based Off Of Inputted Tools ###
    alt_error = []
    az_error = []
    ra_error = []
    dec_error = []
    dist_error = []
    with open(args.tools_file, 'rb') as file:
        possible_tools = json.load(file)
    for tool in args.tools:
        if tool.lower() not in possible_tools.keys():
            raise ValueError('One or more tools you have passed in are not valid arguments.')
        else:
            if 'alt' in possible_tools[tool].keys():
                alt_error.append(possible_tools[tool]['alt'])
            if 'az' in possible_tools[tool].keys():
                az_error.append(possible_tools[tool]['az'])
            if 'ra' in possible_tools[tool].keys():
                ra_error.append(possible_tools[tool]['ra'])
            if 'dec' in possible_tools[tool].keys():
                dec_error.append(possible_tools[tool]['dec'])
            if 'dist' in possible_tools[tool].keys():
                dist_error.append(possible_tools[tool]['dist'])
    alt_error = min(alt_error) if alt_error else args.alt_error
    az_error = min(az_error) if az_error else args.az_error
    ra_error = min(rat_error) if ra_error else args.ra_error
    dec_error = min(dec_error) if dec_error else args.dec_error
    dist_error = min(dist_error) if dist_error else args.dist_error

    ### Create Data Array ###
    processed_data = []

    ### Run Through Times ###
    for _ in tqdm.tqdm(range(args.timesteps), desc="Generating..."):

        ### Create Dictionary for Time time ###
        current_dict = {
            'time': str(t),
            'planet_data': {},
        }

        ### Iterate Through Planets for This Time ###
        for p in planets:
            ### Get Data For This Time ###
            astrometric = position.at(ts.utc(t.year, t.month, t.day)).observe(raw_data[p + ' barycenter'])
            alt, az, _ = astrometric.apparent().altaz()
            ra, dec, dist = astrometric.apparent().radec(epoch = "date")

            ### Adding Noise ###
            alt = alt.degrees + np.random.normal(0, alt_error / 3)
            az = az.degrees + np.random.normal(0, az_error / 3)
            ra = ra.hours + np.random.normal(0, ra_error / 3)
            dec = dec.degrees + np.random.normal(0, dec_error / 3)
            dist = dist.km + np.random.normal(0, dist_error / 3)

            ### Save Planet Data with Error ###
            current_dict['planet_data'][p] = {
                'alt': alt,
                'az': az,
                'ra': ra,
                'dec': dec,
                'dist': dist
            }

        ## Generate Images and Save Location ###
        if args.image:
            filename = os.path.join(args.image_folder, current_dict['time'][:10] + ".png")
            current_dict['image'] = filename
            create_image(current_dict['planet_data'], filename=filename)

        ### Add Dictionary to Data Array ###
        processed_data.append(current_dict)
        t += t_delta

    ### Dump Data Array ###
    with open(args.data_file, 'w') as file:
        json.dump(processed_data, file, indent=4)
