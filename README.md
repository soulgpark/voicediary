# Voice Diary: Emotion Tracking with Speech Recognition

Voice Diary is a diary application that converts user speech into text and analyzes emotions to record them. It visually displays emotions and helps users track their emotional patterns over time :smiley:


## Table of Contents
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Installation](#installation)
   - [Setup Environment](#setup-environment)
4. [Execution](#execution)
   - [Demo](#demo)
   - [User Interface Overview](#user-interface-overview)
   - [How It Works](#how-it-works)


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

### User Interface Overview
1. **Main Page**: The homepage where users can record their voice, analyze emotions, and navigate to past records or the calendar.
2. **Past Record**: A page showing previous transcriptions and their corresponding emotions for specific dates.
3. **Emotion Calendar**: A calendar view displaying the emotions recorded for each day.

### How It Works
1. **Recording**
   - Click the "Recording" button to start recording your voice.
   - Click "Stop Recording" when you're done.
   - The recorded audio is sent to the server for transcription and emotion analysis.
   
2. **Text Conversion**
   - The recorded voice is converted into text using Google Cloud Speech-to-Text API.

3. **Emotion Analysis**
   - The transcription is analyzed using Google Cloud Natural Language API to determine the emotion (happy :smile:, sad :cry:, angry :pout:, neutral:neutral_face:).

4. **Data Visualization**
   - The transcription and emotion are saved with the current date.
   - Users can view emotions in a **calendar view** or check detailed **past records**.

