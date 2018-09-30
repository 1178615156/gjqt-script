@RD /s /q dist
"C:\Program Files (x86)\Python36-32\Scripts\pyinstaller.exe" ^
    --clean ^
    --onefile ^
    main.py
robocopy image_goal dist\image_goal
copy  dm-3.dll dist\dm-3.dll
copy  dm-7.dll dist\dm-7.dll
copy  application.conf dist\application.conf
del main.spec
del gjqt-script.zip
"C:\Program Files\7-Zip\7z.exe" a gjqt-script.zip  .\dist\*
move gjqt-script.zip .\dist\
@RD /s /q build