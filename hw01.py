import os
import re
import sys
import shutil
from pathlib import Path


MAP = {}                     # Dictionary used in transliteration of Cyrillic into Latin
''' Variables for creating a dictionary for the Latinization of Cyrillic '''
alphabet ='абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
latin = (['a','b','v','g','d','e','yo','zh','z','i','y','k','l','m','n','o','p','r','s',
          't','u','f','h','ts','ch','sh','shch','y','y',"'",'e','yu','ya','A','B','V','G',
          'D','E','Yo','Zh','Z','I','Y','K','L','M','N','O','P','R','S','T','U','F','H',
          'Ts','Ch','Sh','Shch','Y','Y',"'",'E','Yu','Ya'])

''' Dictionary to determine folder name by extension type '''
''' Write file extension names in uppercase'''
FOLDER_TO_EXTENT = ({('JPEG', 'PNG', 'JPG', 'SVG'): 'images',
                     ('AVI', 'MP4', 'MOV', 'MKV'): 'video',
                     ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'): 'documents',
                     ('MP3', 'OGG', 'WAV', 'AMR'): 'audio',
                     ('ZIP', 'GZ', 'TAR'): 'archives'})

''' List of folders excluded from processing '''
''' Write folder names in lowercase'''
FOLDER_SKIP = ['archives', 'video', 'audio', 'documents', 'images', 'others']

''' File name normalization '''
def normalize(name_file):
  name_file = str(name_file)
  latin_name = name_file.translate(MAP)              # Translation of Cyrillic into Latin
  invalid_char = set(re.findall(r'\W', latin_name))  # Set of INVALID characters in latin_name
  new_name = ''
  for s in latin_name:       # Replace "invalid" characters with "_" haracter
    if s in invalid_char:
      new_name += '_'
    else:
      new_name += s          
  return new_name            # normalized filename without extension

''' Determining the folder name by the file extension name '''
def find_name_folder(name_ext):
  name_ext = str(name_ext).upper()
  for key_tuple, name_folder in FOLDER_TO_EXTENT.items():
    if name_ext in key_tuple:
      new_folder = name_folder
      return new_folder.upper()
  return 'others'.upper()

''' Unpacking archive files '''
def Unpacking_zipped_files(unpack_file, unpack_folder):
  if not unpack_folder.is_dir():
    unpack_folder.mkdir()
  try:
    shutil.unpack_archive(unpack_file, unpack_folder)
  except:
    folder_bad = Path(unpack_folder.parent.parent, 'BAD_FILE')  # Folder for "bad" files
    if not folder_bad.is_dir():         
      folder_bad.mkdir()
    shutil.move(unpack_file, folder_bad)
  else:
    os.remove(unpack_file)           # Let's delete the successfully unpacked file     
  return None  
          
'''  '''
def file_processing(elements, start_folder):
  elements = Path(elements)
  name_file = elements.stem            # File name without extension
  new_name = normalize(name_file)      # New (normalized) file name
  ext_file = elements.suffix[1:] if elements.suffix else '  '
  new_folder = find_name_folder(ext_file)            
  target_file = Path(start_folder, new_folder, new_name+elements.suffix)
  target_folder = Path(start_folder, new_folder)
  
  if not target_folder.is_dir():       # Destination folder missing 
    target_folder.mkdir()              # let's create it
    
  if new_folder == 'ARCHIVES':         # This is a zipped file
    dir_unpack = Path(target_folder, new_name)  # Folder for unpacking archives
    Unpacking_zipped_files(elements, dir_unpack)
  else:
    shutil.move(elements, target_file) # Move the file to the target folder under a normalized name
  return new_folder, new_name+elements.suffix

''' Recursively analyze the contents of a specified folder'''
def parse_folder(iter_folder, start_folder, list_tuple):
  for elements in iter_folder.iterdir():
    if elements.is_dir():
      if not elements.name.lower() in FOLDER_SKIP:
        # Folder name is not in the "do not process" list
        # Let's continue analyzing the subfolder
        parse_folder(elements, start_folder, list_tuple)
    else:
      folder_and_file = file_processing(elements, start_folder)
      list_tuple.append(folder_and_file)
  return list_tuple

''' Deleting empty folders '''
def remove_empty_folder(name_folder, start_path):
  for elements in name_folder.iterdir():
    if elements.is_dir():
      try:
        elements.rmdir()
      except:
        pass
      else:
        elements = elements.parent
        if elements != start_path:
          elements = elements.parent
              
      remove_empty_folder(elements, start_path)

''' Print a list of files by category And a list of unknown file extensions '''
def write_list_kategori(list_kategori):
  list_kategori = list(list_kategori)
  dict_kategori = {}
  unknown_ext = []
  for t in list_kategori:
    if t[0].lower() == 'others':
      ext = Path(t[1]).suffix
      if  ext:
        unknown_ext.append(ext[1:])
    if t[0] in dict_kategori:
      dict_kategori[t[0]].append(t[1])
    else:
      dict_kategori[t[0]] = [t[1]]
      
  print('List of files by category:') 
  for key, value in dict_kategori.items():
    print('category: ',key)
    for s in value:
      print('  ',s)
    
  print('List of unknown extensions:')
  for s in unknown_ext:
    print('|{:<10}|'.format(s))
    
  return None    

''' Main procedure. Checking the presence of a folder, 
    creating a dictionary for transliteration and starting the folder analysis procedure '''
def main():
  global MAP
  list_file_ext = dict()               # List of files by category
      
  ''' Checking the number of parameters passed '''
  if len(sys.argv) == 1:
    return 'Error: The "Folder name for analysis" parameter is not specified'
  elif len(sys.argv) == 2:
    start_folder = Path(sys.argv[1])
  else:
    return 'Error: The number of parameters is more than two'
  
  if not start_folder.is_dir():        # Checking if a folder exists  
    return 'Error: Folder not found or name error'
  
  ''' Creating a dictionary (MAP) for transliteration '''
  for key, value in zip(alphabet, latin):
    MAP[ord(key)] = value
    
  ''' Analysis of folder contents.  
      Renaming and moving files into folders by type group '''
  list_tuple = []    
  list_kategori = parse_folder(start_folder, start_folder, list_tuple)
  write_list_kategori(list_kategori)      # Print a list of files by category
  
  remove_empty_folder(start_folder, start_folder)  # Deleting empty folders
    
  return 'Successful completion'
    
if __name__ == '__main__':
  print(main())
       