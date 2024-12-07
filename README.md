# Voice Diary: Emotion Tracking with Speech Recognition

Voice Diary is a diary application that converts user speech into text and analyzes emotions to record them :smiley: It visually displays emotions and helps users track their emotional patterns over time.


## Table of Contents
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Installation](#installation)
   - [Setup Environment](#setup-environment)
4. [Execution](#execution)
   - [Demo](#demo)


## Features

- **Voice Recording**: Record user speech and send it to the server.
- **Text Conversion**: Convert speech to text.
- **Emotion Analysis**: Analyze emotions from the converted text.
- **Calendar View**: Visualize emotional data in a calendar format.
- **History Tracking**: View text and emotions for specific dates.


## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: JSON file for data storage
- **Cloud Services**:
  - Google Cloud Speech-to-Text API
  - Google Cloud Natural Language API


## Installation

### Setup Environment
1. Install the required packages
```bash
   pip install flask google-cloud-speech google-cloud-language pydub
```
2. Install FFmpeg
  - Download and install FFmpeg, then add it to your system PATH.
 3. Set up Google Cloud Service Account
  - Generate a service account key (JSON) from Google Cloud Console


## Execution

### Demo

https://github.com/user-attachments/assets/2df8e10c-fd9f-432d-a681-10fee57ce52b
