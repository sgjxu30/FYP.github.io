import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import median_absolute_deviation
from scipy.stats import mode
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics.pairwise import cosine_distances

'''1st method to remove the outliers, but still remain some'''


def detect_outliers(csi):
    # Compute the median and median absolute deviation (MAD) of each subcarrier
    med = np.median(csi, axis=1)
    mad = median_absolute_deviation(csi - med[:, np.newaxis], axis=1)

    # Compute the Z-score for each subcarrier of each CSI data
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


'''2nd method to remove the outliers, best performance,'''
'''only this method is called when process the data'''


def remove_csi_outliers_lof(csi, n_neighbors=20, contamination='auto'):
    # Flatten CSI array into a 2D matrix
    X = csi.T.real

    # Compute the LOF scores for each data point
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, metric=cosine_distances)
    lof.fit(X)
    outliers = lof.negative_outlier_factor_ < -lof.offset_

    # Remove the CSIs that are outliers
    csi = csi[:, ~outliers]

    return csi


def remove_csi_outliers_kmeans(csi):
    # Flatten CSI array into a 2D matrix
    X = csi.T.real

    # Compute the number of clusters based on the square root of the number of data points
    num_clusters = int(np.sqrt(X.shape[0]))

    # Apply k-means clustering to the data
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)

    # Identify the cluster with the most data points
    largest_cluster = mode(kmeans.labels_).mode[0]

    # Remove the CSIs that are not part of the largest cluster
    outliers = kmeans.labels_ != largest_cluster
    csi = csi[:, ~outliers]

    return csi

def remove_csi_outliers_kmeans2(csi, max_outliers_frac):
    # Flatten CSI array into a 2D matrix
    X = csi.T.real

    # Compute the number of clusters based on the square root of the number of data points
    num_clusters = int(np.sqrt(X.shape[0]))

    # Apply k-means clustering to the data
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)

    # Get the number of data points in the largest cluster
    largest_cluster_size = np.max(np.bincount(kmeans.labels_))

    # Identify the outliers as points that are not in the largest cluster
    is_outlier = np.ones(X.shape[0], dtype=bool)
    for label in np.unique(kmeans.labels_):
        if np.sum(kmeans.labels_ == label) == largest_cluster_size:
            # Skip the largest cluster, since it's not an outlier
            continue
        cluster_points = X[kmeans.labels_ == label, :]
        cluster_distances = np.linalg.norm(cluster_points - kmeans.cluster_centers_[label, :], axis=1)
        # Identify the max_outliers_frac fraction of points in the cluster that are furthest from the cluster center
        num_outliers_in_cluster = int(np.ceil(max_outliers_frac * cluster_points.shape[0]))
        outlier_indices_in_cluster = np.argsort(cluster_distances)[-num_outliers_in_cluster:]
        is_outlier[kmeans.labels_ == label][outlier_indices_in_cluster] = True

    # Remove the CSIs that are outliers
    csi = csi[:, ~is_outlier]

    return csi

def remove_csi_outliers_kmeans_th(csi, threshold):
    # Flatten CSI array into a 2D matrix
    X = csi.T.real

    # Compute the number of clusters based on the square root of the number of data points
    num_clusters = int(np.sqrt(X.shape[0]))

    # Apply k-means clustering to the data
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)

    # Calculate the distance of each point to its assigned cluster centroid
    distances = np.min(cdist(X, kmeans.cluster_centers_), axis=1)

    # Identify the outliers based on the threshold
    outliers = distances > threshold

    # Remove the CSIs that are outliers
    csi = csi[:, ~outliers]

    return csi

def remove_csi_outliers_realpart(csi):
    # Identify the CSI data whose real part values do not lie in the interval (300, 400)
    outliers = np.mean(np.logical_or(csi.real < 220, csi.real > 400), axis=0) > 0.5

    csi = csi[:, ~outliers]
    return csi

def remove_csi_fluctuations(csi, threshold=20):
    # Calculate the standard deviation of the real part values across all subcarriers for each packet
    stds = np.std(csi.real, axis=0)

    # Identify the packets with a high standard deviation
    outliers = stds > threshold

    # Remove the CSI data that are outliers
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
    # csi = remove_csi_outliers_realpart(csi)
    # csi = remove_csi_outliers_cfo(csi, freq_offset) # can remove the outliers without using CFO
    # csi = remove_csi_outliers_kmeans(csi)  # best performance using k-means

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
    np.save('5_pre.npy', csi)


process_side_info(8, '5.txt')
