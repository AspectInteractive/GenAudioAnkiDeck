import configparser
import os
import re
from pathlib import Path
import pyttsx3
import drawtrnstext

config = configparser.ConfigParser()
config.readfp(open(r'config.ini'))
orig_lang_font_name = str(config.get('Settings', 'orig_lang_font_name'))
concat_to_single_file = config.get('Settings', 'all_in_one_file')
video_with_translations = config.get('Settings', 'video_with_translations')
cleanup_after = config.get('Settings', 'cleanup_after')
anki_media_path = Path(config.get('Paths', 'anki_media_path'))
selected_notes_path = Path(config.get('Paths', 'selected_notes_path'))
output_path  = Path(config.get('Paths', 'output_path'))
translated_path = output_path / 'TranslatedCards'
translated_prefix = 'trns_'
output_prefix = 'final_'

delay1_file = 'silence2s.mp3'
delay2_file = 'silence2s.mp3'
ffmpeg_concat_list_file = 'ffmpeg_concat_list.txt'
ffmpeg_image_file = 'translated_text.png'
concat_filename = 'final_output_concat'
audiofile_extension = '.mp3'
videofile_extension = '.mp4'

def read_text_to_arr(input_file):
    with input_file.open(mode="r", encoding="utf-8") as f:
        lines_arr = []
        for line in f:
            trimmed_line_arr = re.split(r'\t+', line.rstrip('\t').rstrip('\n'))
            lines_arr.append(trimmed_line_arr)
    return lines_arr

if __name__ == "__main__":
    engine = pyttsx3.init()
    card_lines_arr = read_text_to_arr(selected_notes_path)
    card_files = []

    os.makedirs(translated_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    remove_html_regex = re.compile('<.*?>')
    filewithext_regex = r'[^:]*(?=])'
    file_regex = r'[^:]*(?=\.)'
    ffmpeg_concat_list = []
    
    for card in card_lines_arr:
        sound_index = [index for (index, word) in enumerate(card) if '[sound:' in word] # the sound file's position in the list varies, so we have to find it
        if (len(card) >= 2 and len(sound_index) > 0):
            original_word = card[0]
            translated_word = re.sub(remove_html_regex, '', card[1])
            
            file = re.search(filewithext_regex, card[sound_index[0]]).group()
            file_without_extension = file[:file.rfind('.')]
            print(f"Original Word: {original_word};\Translated Word: {translated_word};\tFile: {file}")

            anki_media_path_with_file = anki_media_path / file
            translated_file = translated_prefix + file
            translated_path_with_file = translated_path / translated_file
            output_path_with_file = output_path / (output_prefix + file)
            output_path_with_videofile = output_path / (output_prefix + file_without_extension + videofile_extension)
            engine.save_to_file(translated_word, str(translated_path_with_file))
            engine.runAndWait()

            # Merge Translation MP3 with Original MP3
            ffmpeg_command = (f'ffmpeg -y -i "{translated_path_with_file}" -i "{delay1_file}" -i "{anki_media_path_with_file}" -i "{delay2_file}" -filter_complex ' +
                              f'"[0:a:0][1:a:0][2:a:0][3:a:0]concat=n=4:v=0:a=1[outa]" -map "[outa]" "{output_path_with_file}"')
            os.system(ffmpeg_command)
            if(cleanup_after == '1'):
                os.remove(translated_path_with_file)

            # Add Image of Word to each file
            if(video_with_translations == '1'):
                img_out = drawtrnstext.draw_text(original_word, orig_lang_font_name)
                img_out.save(ffmpeg_image_file)
                ffmpeg_add_img_command = (f'ffmpeg -y -loop 1 -i "{ffmpeg_image_file}" -i "{output_path_with_file}" -shortest -acodec copy -pix_fmt yuv420p' +
                                          f' -vcodec mpeg4 -tune stillimage "{output_path_with_videofile}"')
                os.system(ffmpeg_add_img_command)
                os.remove(ffmpeg_image_file)
                os.remove(output_path_with_file)

            # Create Text File of all Output Files
            if(concat_to_single_file == '1'):
                output_path_with_file_for_concat = output_path_with_videofile if video_with_translations == '1' else output_path_with_file
                ffmpeg_concat_list.append("file '" + str(output_path_with_file_for_concat) + "'")

    if(concat_to_single_file == '1'):
        concat_file = concat_filename + (videofile_extension if video_with_translations == '1' else audiofile_extension)
        output_path_with_concat_file = output_path / concat_file
        ffmpeg_command2 = f'ffmpeg -y -f concat -safe 0 -i "{ffmpeg_concat_list_file}" -c copy "{output_path_with_concat_file}"'
        with open(ffmpeg_concat_list_file, 'w') as f:
            f.write('\n'.join(ffmpeg_concat_list))
        os.system(ffmpeg_command2)
        if(cleanup_after == '1'):
            with open(ffmpeg_concat_list_file, 'r') as f:
                for line in f:
                    file_path = Path(line[5:].replace('\'','').rstrip('\n'))
                    os.remove(str(file_path))
        os.remove(ffmpeg_concat_list_file)
