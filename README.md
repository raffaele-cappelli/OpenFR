# OpenFR
A collection of Python modules, using OpenCV and NumPy, that implement the main steps in fingerprint recognition.

## Fingerprint segmentation module
Fingerprint segmentation is the first step of most fingerprint recognition algorithms. This module implements a simple but fast and effective method for fingerprint segmentation. Experimental results on FVC2000, FVC2002, and FVC2004 databases shows that the performance of this software is aligned to other state-of-the-art techniques.

### Files
- segmentation.py: Python module.
- segmentation.ipynb: Jupyter notebook containing examples and a simple framework for optimizing parameters and testing on FVC databases.

### Performance results
The accuracy of this module was measured following the same protocol adopted in \[1\], using FVC2000/2002/2004 databases and the ground truth information kindly provided by the authors of \[1\]. The following table reports segmentation error rates of some state-of-the-art approaches and of this segmentation algorithm. As in \[1\], parameters were optimized on FVC sets "B" and the tests were performed on sets "A".
Despite its simplicity, the algorithm implemented in this module is, on the average, more accurate than all the other ones.

| Database | GFB [3]<sup>*</sup> | HCR [4]<sup>*</sup> | MVC [2]<sup>*</sup> | STFT [5]<sup>*</sup> | FDB [1] | BioLab [6] | OpenFR |
| --- | ---:| ---:| ---:| ---:| ---:| ---:| ---:|
| FVC2000-DB1 | 13.26 | 11.15 | 10.01 | 16.70 |  5.51 | 6.83 | 4.71	|
| FVC2000-DB2 | 10.27 |  6.25 | 12.31 |  8.88 |  3.55 | 4.57 | 4.14	|
| FVC2000-DB3 | 10.63 |  7.80 |  7.45 |  6.44 |  2.86 | 5.79 | 3.73	|
| FVC2000-DB4 |  5.17 |  3.23 |  9.74 |  7.19 |  2.31 | 5.69 | 2.35	|
| FVC2002-DB1 |  5.07 |  3.71 |  4.59 |  5.49 |  2.39 | 3.59 | 1.99	|
| FVC2002-DB2 |  7.76 |  5.72 |  4.32 |  6.27 |  2.91 | 4.24 | 2.75	|
| FVC2002-DB3 |  9.60 |  4.71 |  5.29 |  5.13 |  3.35 | 6.07 | 4.12	|
| FVC2002-DB4 |  7.67 |  6.85 |  6.12 |  7.70 |  4.49 | 8.09 | 4.08	|
| FVC2004-DB1 |  5.00 |  2.26 |  2.22 |  2.65 |  1.40 | 1.73 | 1.09	|
| FVC2004-DB2 | 11.18 |  7.54 |  8.06 |  9.89 |  4.90 | 8.28 | 4.03	|
| FVC2004-DB3 |  8.37 |  4.96 |  3.42 |  9.35 |  3.14 | 3.82 | 2.50	|
| FVC2004-DB4 |  5.96 |  5.15 |  4.58 |  5.18 |  2.79 | 5.00 | 2.80	|
| Average     |  8.33 |  5.78 |  6.51 |  7.57 |  3.30 | 5.31 | 3.19 |

<sup>*</sup>As reported in [1].

[1] Thai DH, Huckemann S, Gottschlich C (2016) Filter Design and Performance Evaluation for Fingerprint Image Segmentation. PLoS ONE 11(5).  
[2] Bazen AM, Gerez SH. Segmentation of Fingerprint Images. In: Proc. ProRISC. Veldhoven, The Netherlands; 2001. p. 276–280.  
[3] Shen LL, Kot A, Koo WM. Quality measures of fingerprint images. In: Proc. AVBPA. Halmstad, Sweden; 2001. p. 266–271.  
[4] Wu C, Tulyakov S, Govindaraju V. Robust point-based feature fingerprint segmentation algorithm. In: Proc. ICB 2007. Seoul, Korea; 2007. p. 1095–1103.  
[5] Chikkerur S, Cartwright A, Govindaraju V. Fingerprint image enhancement using STFT analysis. Pattern Recognition. 2007; 40(1):198–211.  
[6] R. Cappelli, M. Ferrara, and D. Maio, "A Fast and Accurate Palmprint Recognition System Based on Minutiae," IEEE Transactions on Systems, Man, and Cybernetics, Part B: Cybernetics, 2012.  

