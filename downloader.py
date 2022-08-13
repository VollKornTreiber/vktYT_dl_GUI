from __future__ import unicode_literals;
import youtube_dl;
import PySimpleGUI as sg;

#https://github.com/ytdl-org/youtube-dl

print("vktYT_dl_GUI - By VollKornTreiber, 2022");

class Loader:
    def __init__(self):
        super().__init__();
        sg.theme("reddit");
        self.layout = [
            [sg.Text("Insert your Link, choose your format and quality and download. Dead-simple!")],
            [sg.Text("URL"), sg.Input(key = "INP"), sg.Button("Ins", key = "BUT_PASTE")],
            [[sg.Radio("Audio only", "FORMAT", default = True), sg.Text("Extracts the audio from the video"), sg.Combo(["32","96","128","160","192","256","320"], default_value="128", key = "QUAL")], 
             [sg.Radio("Video", "FORMAT"), sg.Text("Downloads the entire video"), sg.Combo(["144p","240p","360p","480p","720p","1080","1440p","4K","8K"], default_value="720p", key = "QUAL")]
            ],
            [sg.Button("Start!", key = "BUT_ACTION"), sg.Button("Abort!", key = "BUT_ABORT", disabled = True)],
            [sg.Text("Ready...", key = "OUTP")],
            [sg.ProgressBar(key = "BAR", max_value = 100, size = (50,20), visible = False)],
            [sg.Button("Quit", key = "BUT_QUIT")],
            [sg.Text("GUI by VollKornTreiber, 2022")]
        ];
        
        self.window = sg.Window("Youtube Downloader", self.layout);

    def Action(self, link, form, qual):

        self.settings = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': form,
                'preferredquality': qual,
            }],
        };

        try:
            with youtube_dl.YoutubeDL(self.settings) as ydl:
                ydl.download([link]);
        except:
            pass;




dLoader = Loader();

while True:
    event, val = dLoader.window.read();

    if event == sg.WINDOW_CLOSED or event == "BUT_QUIT":
        print("Closing...");
        break;
 
    if event == "BUT_PASTE":
        dLoader.window["INP"].update(sg.clipboard_get());

    if event == "BUT_ACTION":
        dLoader.window["INP"](disabled = True);
        dLoader.window["BUT_ACTION"](disabled = True);
        dLoader.window["BUT_PASTE"](disabled = True);
        dLoader.window["BUT_QUIT"](disabled = True);
        dLoader.window["BUT_ABORT"](disabled = False);
        dLoader.window["BAR"].update(visible = True);
        #dLoader.Action(val["INP"]);

dLoader.window.close();

