[![339Kvix.md.png](https://iili.io/339Kvix.md.png)](https://freeimage.host/i/339Kvix)

# YTAnalyzer (BETA)

**YTAnalyzer** is an **open source** terminal tool made in Python that is currently in beta.

- Interactive and optimized interface, with colored messages and styled prompts.
- Supports multiple languages (currently English and Brazilian Portuguese).

Currently, it includes an analysis function called **PlaylistChecker**, which analyzes YouTube playlists.

In the future, it will be a complete tool for YouTube analysis.

## Installation

## On Windows

- [Python 3.7 or higher](https://www.python.org/downloads/)
- Windows 10/11 - 64 Bits (May work on other versions of Windows, but it has not been tested).

**Open the CMD**

1. Install Git if you don't have it.

```
curl -LO https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe
```
3. After that, execute:
```
start Git-2.48.1-64-bit.exe
```
4. Clone the repository and then open it.

```
git clone https://github.com/gabrieldukee/YTAnalyzer.git
cd YTAnalyzer
```

## On Linux

1. Install Git if you don't have it.

```
sudo apt-get install git
```
2. Clone the repository and then open it.
```
git clone https://github.com/gabrieldukee/YTAnalyzer.git
cd YTAnalyzer
```

## Setting Up the Tool

Before running the tool, you will need to obtain a YouTube API key, which is essential for the tool to function.

### Obtaining Your YouTube API Key

You can **get your API in 2 minutes** by watching this quick [Tutorial](https://www.youtube.com/watch?v=ltdJOX_DVtE)

### Configuring the API Key in the Project

Open the `config.txt` file (at the root of the project) and insert your key as follows:
`YT_API_KEY=YOUR_KEY_HERE`

After that, run the tool by typing:

```
python ytanalyzer.py
```

The tool will automatically install the necessary **dependencies** from the `requirements.txt` file for it to work.

After the **installation**, a **guide** on how to use the tool will open. All interactions with the tool are done through the **keyboard**.

## Guide
```
 INITIAL CONFIGURATION


1. YouTube API Setup (if you haven't done so already):

   a) Open the "YTAnalyzer" folder and then open the "config.txt" file.

   b) Insert your YouTube API key in the following format:
      YT_API_KEY=YOUR_KEY_HERE

2. Language / Exit:

   [L] Languages       Type L to switch the interface language.
   [X] Exit            Type X to exit the program.


 YOUTUBE ANALYSIS TOOLS

                            - PLAYLIST CHECKER -

  This function allows you to analyze YouTube playlists, displaying data such as title, 
  duration and video statistics. The user can choose between analyzing the entire 
  playlist or a specific range of videos. The results can be saved 
  in .xlsx or .txt formats.


Usage:

  python ytanalyzer.py -playlist [start] [end] [options]


Analysis Options:

  -d          Displays the durations of the videos and the total.
  -v          Displays the number of views per video and the total number of views.
  -l          Displays the number of likes per video and the total number of likes.
  -c          Displays the number of comments per video and the total number of comments.
  -date       Includes the date and time of the analysis.


Input Examples:

  1) Complete simple analysis of the playlist (displays title, number and duration):
      **python ytanalyzer.py -playlist**

  2) Customizable simple analysis (videos 1 to 5 of the playlist):
      python ytanalyzer.py -playlist 1 5*

  3) Displaying comments:
      python ytanalyzer.py -playlist -c

  4) Combined options (displays videos 1 to 14 from the playlist, along with durations, 
            views, likes, comments, and date):
      python ytanalyzer.py -playlist 1 14 -d -v -l -c -date


Playlist URL:

  After entering, the tool will ask for the playlist URL or ID:
  "Enter the playlist ID or URL:"

  Provide the URL or ID:
    URL: www.youtube.com/watch?v=JGwWNGJdvx8&list=PL_Q15fKxrBb4gT7eMNvTvrFMmqDDNMXMk
    ID:  PL_Q15fKxrBb4gT7eMNvTvrFMmqDDNMXMk


Reports:

  After the analysis, choose one of the options if you want to save the result to a file:
    [1] Save result as XLSX       Excel Report (Recommended)
    [2] Save result as TXT        Text file Report


 EXTRA TIPS
   General terminal/CMD tips

  1) Tab - Auto-completion:
      Press the Tab key to automatically complete a command or directory path.
      This helps save time, avoiding the typing of long paths or incomplete commands.

  2) Up/Down Arrow - Command History:
      Use the up arrow key to scroll through previously executed commands and the down arrow 
      key to return to more recent commands.
```