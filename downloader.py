#This downloader GUI makes use of the Youtube_dl library.
#ffmpeg is required for this in order to convert to Mp3/mp4: https://github.com/FFmpeg/FFmpeg
#Youtube_dl by ytdl-org: https://github.com/ytdl-org/youtube-dl

from __future__ import unicode_literals;
import youtube_dl;
import PySimpleGUI as sg;

VER = 0.5;

print("vktYT_dl_GUI - By VollKornTreiber, 2022");
print("This is the output window. Don't close it.");

class Loader:

    def __init__(self):
        super().__init__();
        sg.theme("GreenTan");

        #prepare middle row for audio/video option
        self.col_audio = [[sg.Radio("Audio only", "FORMAT", key = "BUT_AUDIO", enable_events = True, default = True), sg.Text("Extract the audio")], [sg.Text("Bitrate: "), sg.Combo(["32","96","128","160","192","256","320"], default_value="128", key = "AUD_QUAL")]];
        self.col_video = [[sg.Radio("Video", "FORMAT", enable_events = True, key = "BUT_VIDEO"), sg.Text("Download the entire video")], [sg.Text("Resolution: "), sg.Combo(["144","240","360","480","720","1080","1440","2160","4320"], default_value="720", key = "VID_QUAL", disabled = True)]];

        #prepare whole layout
        self.layout = [
            [sg.Text("Insert your Link, choose your format and quality and download. Dead-simple!")],
            [sg.Text("URL"), sg.Input(key = "INP"), sg.Button("Paste", key = "BUT_PASTE")],
            [sg.HSeparator()],

            [
             sg.Column(self.col_audio), 
             sg.VSeparator(),
             sg.Column(self.col_video),
            ],

            [sg.HSeparator()],
            [sg.Button("Start!", key = "BUT_ACTION"), sg.Button("Quit", key = "BUT_QUIT")],
            [sg.Text("GUI by VollKornTreiber, 2022")]
        ];
        
        #prepare window with title
        self.window = sg.Window("Youtube Downloader GUI v"+str(VER), self.layout);

    def Action(self):
        
        #called when "Start" button is pressed.
        #Check audio/video options first
        
        if val["BUT_AUDIO"] == True:
            self.settings = {
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": val["AUD_QUAL"],
                }],
            };

        if val["BUT_VIDEO"] == True:
            self.settings = {
                "format": "bestvideo[height<="+val["VID_QUAL"]+"]+bestaudio/best[height<="+val["VID_QUAL"]+"]"
            };
        
        #After audio/video options check, initiate download

        print("\n-------------------------------------");
        print("Please wait... This may take a while.");
        print("-------------------------------------");

        try:
            with youtube_dl.YoutubeDL(self.settings) as ydl:
                ydl.download([val["INP"]]);
                print("\n------------------------------------------------------");
                print("Finished! You can download something else if you want.");
        except:
            print("\n------------------------------------------------------");
            print("Download failed! An Error has occurred! Check the log.");
        finally:
            
            print("------------------------------------------------------");


#instantiate main window
dLoader = Loader();

while True:
    event, val = dLoader.window.read();

    if event == sg.WINDOW_CLOSED or event == "BUT_QUIT":
        #called when "Quit" button is pressed or window is closed
        print("Closing...");
        break;
 
    if event == "BUT_PASTE":
        #insert from clipboard
        dLoader.window["INP"].update(sg.clipboard_get());

    if event == "BUT_AUDIO":
        dLoader.window["AUD_QUAL"].update(disabled = False);
        dLoader.window["VID_QUAL"].update(disabled = True);
        
    if event == "BUT_VIDEO":
        dLoader.window["AUD_QUAL"].update(disabled = True);
        dLoader.window["VID_QUAL"].update(disabled = False);

    if event == "BUT_ACTION":
        #initiate download
        dLoader.Action();
    
#quit
dLoader.window.close();

