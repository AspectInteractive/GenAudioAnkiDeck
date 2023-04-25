# GenAudioAnkiDeck

## What is it?

This little python program will convert a text output of selected cards from the Anki desktop app into either a set of individual audio or video cards with audio translations via text-to-speech. It can also merge these individual files into one large audio or video deck via the `all_in_one_file` option. If outputting to a video, the original language's written form is also shown (e.g. Hangul for Korean).

## Config Options

Below is an explanation of the config options within config.ini:

`orig_lang_font_name` : The font file to use for the original language when outputting video cards. E.g.: If you are learning Korean, this should be a Korean font or font with Korean characters.

`all_in_one_file` : Whether to output all of your audio/video cards into one large or to keep them separate (1 = Enabled)

`video_with_translations` : Whether to output all of your audio/video cards into one large or to keep them separate (1 = Enabled)

`cleanup_after` : Whether to delete individual card files after creating an 'all in one file' (see above) (1 = Enabled) 

## How To Use

You will first need the "Export Cards As Text" add-on for Anki (https://ankiweb.net/shared/info/1112021968), as well as FFMPEG installed on your machine.

1. Open Anki, click "Browse", then find the Notes you want to export (e.g. under "Today" you can click "Overdue" for those that are overdue).
2. Select all the cards (CTRL + A in Windows) then go to the top menu and select "Notes > Export Notes...". 
3. In the new pop-up choose "Notes in Plain Text (.txt)" as the "Export format" and make sure that the "Include HTML and media references" option is ticked
4. Save the file into the folder where you have placed GenAudioAnkiDeck, or somewhere you can find, and then make note of the file's name if it is in the GenAudioAnkiDeck folder, or full path if it's elsewhere
5. Update the `config.ini` file in your GenAudioAnkiDeck to have "`selected_notes_path`" parameter as the path to the file you saved in the last step. Note that if the file is in the same folder as GenAudioAnkiDeck, you only need to specify the filename, otherwise you need to specify the full path.
6. Update `config.ini` to have the path to your Anki app's media directory for the `anki_media_path` parameter
7. Update `config.ini` to use a font file of your choice for the original language you are learning in the `orig_lang_font_name` parameter. This font must either be in your system directory, or in the GenAudioAnkiDeck directory.
6. Run `main.py` and your output will be in `FinalCards\`, or the path you specified in `output_path` within `config.ini`