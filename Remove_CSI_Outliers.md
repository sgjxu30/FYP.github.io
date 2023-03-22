# **Possible Ways to Remove CSI Outliers**

Below is the CSI with outliers.  
[![Screenshot-2022-11-30-at-12-23-49.png](https://i.postimg.cc/SRNpRbDC/Screenshot-2022-11-30-at-12-23-49.png)](https://postimg.cc/xJ7Zphr1)  
> Outliers Detection and Handling  
> https://zhuanlan.zhihu.com/p/41528651   
> Outliers Analysis  
> https://zhuanlan.zhihu.com/p/342801954  

## **3 Ways to deal with outliers**
1. Delete records containing outliers;
2. Interpolation treats outliers as missing values and uses missing value processing methods to deal with them. The advantage is to use existing data to replace or interpolate outliers.
3. Do nothing. Data analysis is conducted directly on the data set containing outliers.

In this case, I will delete the outliers since there are too much of them, I can not just leave it and feed them to the DL model.

## **Z-score**
### **Pauta Criterion (3∂ criterion)**
If the data follows a normal distribution, under the 3σ principle an outlier is defined as a value in a set of measurements that deviate from the mean by more than three standard deviations.

### **Python Script**
```Python
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
```

#### **Comments**
This methods somehow works, but the performance is not very good.  
There are still a large number of outliers remain.  

*Semester 2 Week 3 Updated*

## **Detect and remove the outliers base on frequency offset**

### Idea
When I was capturing CSI, I could always see the real time display of all the information (CSI, timestamp, equalizer, frequency offset), and I noticed that when there was a outlier shown in CSI plot, the frequency offset of the cooresponding packet is either very high or very low.

So I try to find the majority value of th frequency offset and write a function to remnove the csi whose frequency offset does not belongs to those values.


Say the frequency offset below 24000Hz and abovbe 37000Hz are the frequency offset of the outlier, here is the code to removw them. 

```Python
def detect_outliers(csi, freq_off):
    # detect outliers based on frequency offset
    freq_outliers = np.logical_or(freq_offset < 24000, freq_offset > 37000)

    csi = csi[:, ~freq_outliers]

    return outliers

```

#### **Comments**
This method can remove most outliers, but there are still a very few of outliers exist.

So I decide to combine the above two methods together, and now it works very well. The CSI samples are nice and clean.


```Python
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
```

*Updated Semester 2 Week 4 22 Feb*

## **Other Attempts**
In week 5, meanwhile I am modifying my CNN model, I was trying to find out other ways instead of remove the outliers based on freq_off since its changing all the time, which is very unstable. 

So K-means came to my mind.

```Python
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
```

### **Comments**
It's performance is the best to classify different shapes of CSI among all the methods that I have tried.

But it has 2 problems.
+ It will remove most of the data, and the remaining samples are inadequate to be treated as the training set.
  + Normally if I have captured over 2000 samples, I would only get 100-200 samples after processing.
+ If the environment disturbance is massive when capturing CSI, then the number of outliers may exceed the number of proper CSIs, thus only leaves the outliers after the process.

*Updated Semester 2 Week 5 28 Feb*




*I will upload the scripts 'process_side_info.py' for all the possible solutions I have tried.* 

