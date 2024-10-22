# 3D Human Pose Estimation using Mixture Density Networks

This repository contains the implementation of the paper *"Generating Multiple Hypotheses for 3D Human Pose Estimation with Mixture Density Network"*. This project includes training, testing, and analysis scripts, along with all necessary dependencies and a description of the dataset used.

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Dataset](#dataset)
- [Training the Model](#training-the-model)
- [Testing the Model](#testing-the-model)
- [Results](#results)
- [PDF Report](#pdf-report)
- [Contact Information](#contact-information)

## Project Structure

```plaintext
.
├── data/                 # Directory containing the dataset (.npz files)
├── src/                  # Source codes for training, testing, and analysis
│   ├── train.py          # Script for training the model
│   ├── test.py           # Script for testing the model
│   ├── analysis.py       # Script for analyzing results
├── requirements.txt      # List of dependencies
├── README.md             # This readme file
├── report.pdf            # PDF containing implementation details and results
