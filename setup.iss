[Setup]
AppName=LessonAlarmScheduler
AppVersion=1.0
DefaultDirName={autopf}\LessonAlarm
DefaultGroupName=LessonAlarm
OutputDir=output
OutputBaseFilename=LessonAlarmInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\elvin\Desktop\lessonAlarmScheduler\app.exe"; DestDir: "{localappdata}\LessonAlarmSchedule"; Flags: ignoreversion
Source: "C:\Users\elvin\Desktop\lessonAlarmScheduler\schedule.json"; DestDir: "{localappdata}\LessonAlarmSchedule"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\LessonAlarm"; Filename: "{localappdata}\LessonAlarmSchedule\app.exe"

[Run]
Filename: "{localappdata}\LessonAlarmSchedule\app.exe"; Description: "Запустить LessonAlarm"; Flags: nowait postinstall skipifsilent