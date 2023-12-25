The function distributes files in the specified folder
by destination folder depending on the file extension:
   File extension                           Destination folder
'JPEG', 'PNG', 'JPG', 'SVG'                        images   
'AVI', 'MP4', 'MOV', 'MKV'                         video
'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'        documents 
'MP3', 'OGG', 'WAV', 'AMR'                         audio 
'ZIP', 'GZ', 'TAR'                                 arhives
other files                                        others
In the file name, cyrillic characters are replaced with latinones,
characters other than letters, numbers and the "_" symbol are replaced with
symbol "_". Archived files are unpacked into the ARHIVES folder
into a subfolder with the name of the archive file.
The function is called from the command line:
      clean-folder <folder name>