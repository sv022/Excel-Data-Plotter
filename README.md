# Excel Data Plotter

![Current Version](https://img.shields.io/badge/version-1.0.0-green.svg)

This is python application built with Tkinter that plots data from Excel files.

![Preview](https://raw.githubusercontent.com/sv022/MockDB/refs/heads/main/ExcelPlotter/preview.png)

---

## Features

- Minimalistic Design
- 3D & 2D plots
- Language support

<!-- ![UI Demo](TODO)


![2D Plot](TODO)


![3D Plot](TODO) -->

---

## Setup

### Running from source

Clone this repo to your desktop and run `pip install -r requirements.txt` to install all the dependencies.

Once the dependencies are installed, run `python main.py` to start the application.

### Downloading the executable

You can download the latest version of the application from [here](https://github.com/sv022/Excel-Data-Plotter/releases/latest).

### Builing executable from source

You can build an executable from source by running

`pyinstaller --noconfirm --onefile --windowed --name "Excel Data Plotter" --icon "app\public\icon.ico" --add-data "app\public\icon.ico;app\public\" main.py`

---

## Usage

Select XLSX file by clicking "Select file" button.

> ⚠️ Warning  
> Selecting a file that does not contain a table-structured data will not result in an error, but will lead to unpredictable behaviour.

Once the file is loaded click on the column headers to select or deselect them.

Once you have selected the columns, click "2D Plot" or "3D Plot" button to view the respective plot.

---
