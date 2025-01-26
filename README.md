# Project Name

Short description or introduction to the project.

## Overview

The main run will search shares from the fmp api.
Then, the run will query various metrics for each share.
The metrics are then stored in a dataframe, and later as Excel file.
The shares will be evaluated based on constraints within several categories.

The following categories are evaluated based on the following constraints:

- Undervalued
PE: < 15
PB: < 1.0
ROE: > 15%


- Growth


- Buy on the dip

## Installation

### Requirements

- Python 3.x

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/project_name.git
