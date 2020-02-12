import cv2
import matplotlib.pyplot as plt
import nidaqmx
import numpy as np
import pyvisa
import time

from pathlib import Path


class Oscilloscope:

    def __init__(self, id):
        self.id = id

    def connect(self):
        resources = pyvisa.ResourceManager()
        self.scope = resources.open_resource(self.id)

        # The WORD format is the most accurate for Keysight Oscilloscopes.
        # Data is transferred as signed 16bit integers in 2 bytes.
        self.scope.write(":WAV:FORMAT WORD")

        # Set the byte order to Big-Endian (default for Infinium oscilloscopes)
        self.scope.write(":WAV:BYTEORDER MSBF")

        # Since we're transferring binary data we need to
        # remove the newline read termination
        self.scope.read_termination = None
        print("Oscilloscope Connected Successfully.")

    def get_sample(self):
        return self.scope.query_binary_values(":WAV:DATA?", 'h', is_big_endian=True, container=np.array)


class DAQ:

    def __init__(self):
        self.task = nidaqmx.Task()

    def connect(self):
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # phase 1
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai1")  # phase 2
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai2")  # phase 3
        print("DAQ Card Connected Successfully.")

    def get_sample(self):
        return np.array(self.task.read(number_of_samples_per_channel=600)).T


class FLIR:

    def __init__(self, id):
        self.id = id

    def connect(self):
        self.cap = cv2.VideoCapture(self.id + cv2.CAP_DSHOW)

        print("FLIR Camera Connected Successfully.")

    def get_image(self):
        ret, frame = self.cap.read()
        return frame


def get_measurements(scope, daq, camera, vibration, current, thermal, n_images, n_datapoints, datapoint_frequency):
            i = 0
            j = datapoint_frequency
            k = 0
            while i < n_datapoints:
                start = time.time()
                current[i:j, 1::] = daq.get_sample()
                vibration[i:j, 1] = scope.get_sample()
                i = j
                j += datapoint_frequency
                if i % 6000 == 0:
                    thermal[k] = camera.get_image()
                    k += 1
                    print(f"{int(float(i)/n_datapoints*100)} % of samples collected.")
                    print(f"Approximately {int(running_time - (running_time*float(i)/n_datapoints))} seconds remaining")
                    print("\n")
                time_taken = time.time() - start
                time.sleep(1 - time_taken)
            return vibration, current, thermal


if __name__ == '__main__':

#############################################################
#########################   ADMIN   #########################

    fault = "8bars"
    loading = "half_load"
    directory = Path(f"C:/Users/fraser/Desktop/Project/code/data/{fault}/{loading}")

#############################################################
#############################################################

    # define measurement settings
    running_time = 1200        # seconds (20 mins)
    sample_length = 10          # seconds
    datapoint_frequency = 600   # datapoints per second

    image_resx = 240    # (pixels for FLIR C2)
    image_resy = 320    # (pixels for FLIR C2)
    image_delay = 10    # seconds between images

    n_images = running_time // sample_length
    n_datapoints = running_time * datapoint_frequency   # 720,000

    # initialise instruments
    scope = Oscilloscope('USB0::0x0957::0x0588::CN52170825::0::INSTR')
    daq = DAQ()
    camera = FLIR(0)

    # connect to instruments
    scope.connect()
    daq.connect()
    camera.connect()

    print("\n")

    # initialise measurement arrays
    current = np.zeros((n_datapoints, 4))
    vibration = np.zeros((n_datapoints, 2))
    thermal = np.zeros((n_images, image_resx, image_resy, 3))

    current[:, 0] = [t for t in np.linspace(0, running_time, n_datapoints)]
    vibration[:, 0] = [t for t in np.linspace(0, running_time, n_datapoints)]

    print("arrays initialised")
    print(f"current shape:   {current.shape}")
    print(f"vibration shape:   {vibration.shape}")
    print(f"image shape:   {thermal.shape}")
    print("\n")

    # take measurements
    vibration_data, current_data, thermal_data  = get_measurements(scope, daq, camera, vibration, current, thermal, n_images, n_datapoints, datapoint_frequency)

    # save current measurements to file
    current_data_filepath = Path(f"{directory}/current_data_{fault}_{loading}.csv")

    print(f"Saving Current Data to {directory} ...")

    np.savetxt(current_data_filepath, current_data, delimiter=",",
               header="time, phase1, phase2, phase3")

    print(f"Current data saved as {current_data_filepath}")

    # save vibration measurements to file
    vibration_data_filepath = Path(f"{directory}/vibration_data_{fault}_{loading}.csv")

    print(f"Saving Vibration Data to {directory} ...")

    np.savetxt(vibration_data_filepath, vibration_data,
               delimiter=",", header="time, vibration")

    print(f"Vibration data saved as {vibration_data_filepath}")

    # save images to file
    print(f"Saving Thermal Images to {directory} ...")

    for image in range(0, len(thermal_data)):
        filepath = Path(f"{directory}/thermal_image_{image}.png")
        cv2.imwrite(str(filepath), thermal_data[image])

    print(f"Images saved to {directory}")

    # script finished
    print(f"Data Collected for {fault} under {loading} condition.")
    print("\n\n\n\n")
    cv2.destroyAllWindows()
