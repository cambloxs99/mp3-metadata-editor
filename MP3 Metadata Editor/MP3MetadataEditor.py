import tkinter as tk
from tkinter import filedialog
from mutagen.id3 import ID3
from mutagen.id3._frames import USLT, TPE1, TRCK, TIT2, TALB, TCON, TDRC, TPOS
from typing import Callable


class Button:
    def __init__(self, text, func: Callable, **kwargs):
        self.button = tk.Button(frame, text=text, command=func, **kwargs)
        self.button.grid(row=8, column=0)


class Entry:
    def __init__(self, var, row) -> None:
        var = tk.StringVar(value=var)
        self.entry = tk.Entry(frame, textvariable=var, width=20)
        self.entry.grid(row=row, column=1)


class Text:
    def __init__(self, text, row) -> None:
        self.text = tk.Text(frame, width=25, height=20)
        self.text.insert("1.0", text)
        self.text.grid(row=row, column=1)


class Label:
    def __init__(self, text, row) -> None:
        self.label = tk.Label(frame, text=text)
        self.label.grid(row=row, column=0)


def refresh():
    for widget in frame.winfo_children():
        widget.destroy()


def add(d, entries):
    for pos, key in enumerate(d.keys()):
        if isinstance(entries[pos], Entry):
            value = entries[pos].entry.get()
        else:
            value = entries[pos].text.get("1.0", "end-1c")
            song.add(USLT(encoding=3, desc="", text=value))

        if value == "" and key in song:
            song.pop(key)

        if value:
            if key == "TALB":
                song.add(TALB(encoding=3, text=value))
            elif key == "TPE1":
                song.add(TPE1(encoding=3, text=[value]))
            elif key == "TIT2":
                song.add(TIT2(encoding=3, text=[value]))
            elif key == "TCON":
                song.add(TCON(encoding=3, text=[value]))
            elif key == "TDRC":
                song.add(TDRC(encoding=3, text=[value]))
            elif key == "TRCK":
                song.add(TRCK(encoding=3, text=[value]))
            elif key == "TPOS":
                song.add(TPOS(encoding=3, text=[value]))
    song.save() # changes metadata, does not download a new file


def main():
    songPath = filedialog.askopenfilename(
        title="Select an MP3 file",
        filetypes=[("MP3 Files", "*.mp3")])
    
    try:
        global song
        song = ID3(songPath)
    except Exception as e:
        print(f"File Error: {e}")

    try:
        global frame
        root = tk.Tk()
        root.geometry("500x500")
        frame = tk.Frame(root, height=200, width=250)
        refresh()
        frame.pack()
        ds = {
            "TPE1": song['TPE1'][0] if 'TPE1' in song else "",
            "TIT2": song['TIT2'][0] if 'TIT2' in song else "",
            "TALB": song['TALB'][0] if 'TALB' in song else "",
            "TCON": song['TCON'][0] if 'TCON' in song else "",
            "TDRC": song['TDRC'][0] if 'TDRC' in song else "",
            "TRCK": song['TRCK'][0] if 'TRCK' in song else "",
            "TPOS": song["TPOS"][0] if "TPOS" in song else "",
            "USLT": song["USLT::XXX"] if 'USLT::XXX' in song else "" # only recognises lyrics without language identifier (default)
        } 
        labels = []
        entries = []
        def getTag(tag):
            match tag:
                case "USLT":
                    return 'Lyrics: '
                case "TRCK":
                    return 'Track Number: '
                case "TDRC":
                    return "Year: "
                case "TCON":
                    return "Genre: "
                case "TALB":
                    return "Album: "
                case "TIT2":
                    return "Title: "
                case "TPE1":
                    return "Artist: "
                case "TPOS":
                    return "Disc: "
                case _:
                    return ""
        for pos, (tag, value) in enumerate(ds.items()):
            tag = getTag(tag)
            labels.append(Label(tag, pos))
            if not tag == "Lyrics: ":
                entries.append(Entry(value, pos))
            else:
                entries.append(Text(value, pos))
        changeButton = Button("Confirm", lambda: add(ds, entries))


    except Exception as e:
        import traceback
        print(f"error: {e}")
        traceback.print_exc()
    root.mainloop()


if __name__ == "__main__":
    main()