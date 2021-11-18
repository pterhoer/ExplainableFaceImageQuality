# Explainable Face Image Quality

***25.08.2021*** _start readme_


## Pixel-Level Face Image Quality Assessment for Explainable Face Recognition

* [Research Paper](https://arxiv.org/abs/2110.11001) 
* [Implementation on ArcFace](face_image_quality.py)



## Table of Contents 

- [Abstract](#abstract)
- [Key Points](#key-points)
- [Results](#results)
- [Installation](#installation)
- [Citing](#citing)
- [Acknowledgement](#acknowledgement)
- [License](#license)

## Abstract

An essential factor to achieve high performance in face recognition systems is the quality of its samples. Since these systems are involved in various daily life there is a strong need of making face recognition processes understandable for humans. In this work, we introduce the concept of pixel-level face image quality that determines the utility of pixels in a face image for recognition. Given an arbitrary face recognition network, in this work, we propose a training-free approach to assess the pixel-level qualities of a face image. To achieve this, a model-specific quality value of the input image is estimated and used to build a sample-specific quality regression model. Based on this model, quality-based gradients are back-propagated and converted into pixel-level quality estimates. In the experiments, we qualitatively and quantitatively investigated the meaningfulness of the pixel-level qualities based on real and artificial disturbances and by comparing the explanation maps on ICAO-incompliant faces. In all scenarios, the results demonstrate that the proposed solution produces meaningful pixel-level qualities. 

<img src="Overview.png" height="400">

## Key Points

- point 1
- point 2 ...

## Results
todo 


<img src="FQA-Results/001FMR_lfw_arcface.png" width="430" >  <img src="FQA-Results/001FMR_adience_arcface.png" width="430" >

## Installation
to do marco






## Citing

If you use this code, please cite the following paper.


```
@article{DBLP:journals/corr/abs-2110-11001,
  author    = {Philipp Terh{\"{o}}rst and
               Marco Huber and
               Naser Damer and
               Florian Kirchbuchner and
               Kiran Raja and
               Arjan Kuijper},
  title     = {Pixel-Level Face Image Quality Assessment for Explainable Face Recognition},
  journal   = {CoRR},
  volume    = {abs/2110.11001},
  year      = {2021},
  url       = {https://arxiv.org/abs/2110.11001},
  eprinttype = {arXiv},
  eprint    = {2110.11001},
  timestamp = {Thu, 28 Oct 2021 15:25:31 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2110-11001.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}


```

If you make use of our implementation based on ArcFace, please additionally cite the original ![ArcFace module](https://github.com/deepinsight/insightface).

## Acknowledgement

This research work has been funded by the German Federal Ministry of Education and Research and the Hessen State Ministry for Higher Education, Research and the Arts within their joint support of the National Research Center for Applied Cybersecurity ATHENE.
Portions of the research in this paper use the FERET database of facial images collected under the FERET program, sponsored by the DOD Counterdrug Technology Development Program Office.
This work was carried out during the tenure of an ERCIM ’Alain Bensoussan‘ Fellowship Programme.

## License 

This project is licensed under the terms of the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license.
Copyright (c) 2021 Fraunhofer Institute for Computer Graphics Research IGD Darmstadt

