# **Preprocess CSI Before Training**
## **Combine all CSI samples**
Before feed all collected CSI samples to the model, I need to combine all the CSI for 5 different devices/files.

The CSI are filtered before using the script 'process_side_info_based_on_cfo.py' and the processed CSI are stored in 5 '.npy' files.

The process contains the following steps.
1. load all the files
2. find the smallest number of CSI samples among the five files
3. then all the other files should contain the same number of CSI samples to avoid data biasing
4. combine the CSI from 5 files to 1

The script is as follows.
```Python
# Load each .npy file into a separate variable
csi1 = np.load('3.8_1.npy')
csi2 = np.load('3.8_2.npy')
csi3 = np.load('3.8_3.npy')
csi4 = np.load('3.8_4.npy')
csi5 = np.load('3.8_5.npy')

# Get the smallest number of columns
min_cols = min(csi1.shape[1], csi2.shape[1], csi3.shape[1],csi4.shape[1],csi5.shape[1])

# Truncate the arrays to have the same number of columns
csi1 = csi1[:, :min_cols]
csi2 = csi2[:, :min_cols]
csi3 = csi3[:, :min_cols]
csi4 = csi4[:, :min_cols]
csi5 = csi5[:, :min_cols]

# Concatenate the CSI matrices along the second axis (columns)
combined_csi = np.hstack((csi1, csi2, csi3, csi4, csi5))
```

## **Give label to each single CSI sample**
After precessing all the CSI samples, I need to give each of them a label so that they  can be fed into the DL model.

The easiest way is to create a label array with the same length of all the CSI samples.

The script is shown below.
```Python
# Create a label array corresponding to each CSI matrix
labels1 = np.full(csi1.shape[1], 0)
labels2 = np.full(csi2.shape[1], 1)
labels3 = np.full(csi3.shape[1], 2)
labels4 = np.full(csi4.shape[1], 3)
labels5 = np.full(csi5.shape[1], 4)

# Combine the label arrays
combined_labels = np.concatenate((labels1, labels2, labels3, labels4, labels5))
```

## **Check the shape of the data and labels**
Just print their shape.
```Python
print(f"Combined CSI matrix shape: {combined_csi.shape}")
print(f"Combined labels array shape: {combined_labels.shape}")
```