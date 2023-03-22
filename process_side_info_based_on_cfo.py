import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import median_absolute_deviation


def detect_outliers(csi):
    # Compute the median and median absolute deviation (MAD) of each subcarrier
    med = np.median(csi, axis=1)
    mad = median_absolute_deviation(csi - med[:, np.newaxis], axis=1)

    # Compute the Z-score for each sub-carrier of each CSI data
    zscore = np.abs((csi - med[:, np.newaxis]) / mad[:, np.newaxis])

    # Identify outliers using a threshold of modified Z-score > 3
    threshold = 3
    outliers = np.any(zscore > threshold, axis=0)

    return outliers


def remove_csi_outliers_cfo(csi, freq_offset):
    # detect outliers based on frequency offset
    freq_outliers = np.logical_or(freq_offset < 24000, freq_offset > 37000)

    # detect outliers based on CSI
    csi_outliers = detect_outliers(csi)

    # remove corresponding packets from CSI
    outliers = np.logical_or(freq_outliers, csi_outliers)
    csi = csi[:, ~outliers]

    return csi


def process_side_info(num_eq, side_info_filename):
    # Load data from file
    a = np.loadtxt(side_info_filename)
    len_a = (len(a) // 4) * 4
    a = a[:len_a]

    b = a.reshape(-1, 4)
    num_data_in_each_side_info = 2 + 56 + num_eq * 52
    num_side_info = b.shape[0] // num_data_in_each_side_info

    # Initialize arrays
    side_info = np.zeros((num_data_in_each_side_info, num_side_info), dtype=np.complex128)
    timestamp = np.zeros(num_side_info)
    freq_offset = np.zeros(num_side_info)
    csi = np.zeros((56, num_side_info), dtype=np.complex128)
    equalizer = np.zeros((num_eq * 52, num_side_info), dtype=np.complex128)

    # Parse data into arrays
    for i in range(num_side_info):
        sp = i * num_data_in_each_side_info
        ep = (i + 1) * num_data_in_each_side_info
        timestamp[i] = b[sp, 0] + (2 ** 16) * b[sp, 1] + (2 ** 32) * b[sp, 2] + (2 ** 48) * b[sp, 3]
        freq_offset[i] = (20e6 * b[sp + 1, 0] / 512) / (2 * np.pi)

        side_info[:, i] = b[sp:ep, 0] + 1j * b[sp:ep, 1]
        csi[:, i] = side_info[2:58, i]
        equalizer[:, i] = side_info[58:, i]

    csi = np.roll(csi, -28, axis=0)
    equalizer[equalizer == 32767 + 1j * 32767] = np.nan

    # print(csi.shape)

    # Remove outliers
    csi = remove_csi_outliers_cfo(csi, freq_offset) # can remove the outliers without using CFO
    print(csi.shape)

    # Plot data
    plt.subplot(2, 1, 1)
    plt.plot(np.abs(csi))
    plt.title('CSI')
    plt.ylabel('abs')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(np.angle(csi))
    plt.ylabel('phase')
    plt.xlabel('subcarrier')
    plt.grid(True)

    # if not np.all(np.isnan(equalizer)):
    #     plt.figure()
    #     plt.scatter(np.real(equalizer), np.imag(equalizer))
    #     plt.grid(True)

    # plt.figure()
    # plt.plot(timestamp)
    # plt.title('time stamp (TSF value)')
    # plt.ylabel('us')
    # plt.xlabel('packet')
    # plt.grid(True)

    plt.figure()
    plt.plot(freq_offset)
    plt.title('freq offset (Hz)')
    plt.ylabel('Hz')
    plt.xlabel('packet')
    plt.grid(True)

    plt.show()

    '''save csi to .npy'''
    # np.save('1_new.npy', csi)


process_side_info(8, '3.8_1.txt')
