# AndroidColorsToIOS
Convert android colors.xml (including night mode values if used) into an iOS color catalog file system using simple python script.

![colors.xml](https://imgur.com/K6jeVtS)
![iOS colors](https://imgur.com/nkd6Lw4)

Already have a large color palette defined for your mobile app in Android using Android's colors.xml file format? Have night mode colors too?

Porting these colors over to iOS's color catalog system (introduced in iOS11) is a pain. iOS doesn't use a flat file format, doesn't use hex colors, and so on. Colors are described via one name and a JSON file. This JSON file can contain both light and dark mode values (introduced in iOS13) as opposed to the seperate file structure supported by Android.

Using this tool, you can quickly convert the Android colors.xml files into an iOS color catalog. 

Usage:

Future:
IOSColorToAndroid?
