<div align="center">
  <img src="static/images/AMR_logo.svg" alt="Atom Manga Reader Logo" width="150" />
  <h1>Atom Manga Reader</h1>
</div>

**Atom Manga Reader**, also referred to as **AMR**, is an application designed to read manga on Kobo eReaders.  
It is a lightweight, Kobo-first manga reader focused on simplicity, performance, and minimal user interface, built to work within the constraints of Kobo devices and their built-in browser.

Atom Manga Reader is a fork of **Banana Manga Reader** and has since diverged in design and implementation.  
It is maintained independently and prioritises modern, reliable sources and a cleaner reading experience.

The application is designed to be easy to install and use, with minimal configuration required. While customization is possible by editing the HTML and Python code, the default setup aims to provide a complete, distraction-free manga reading experience out of the box.

Atom Manga Reader focuses on **reading manga you already know about**, rather than discovery. As a result, search functionality is intentionally simple.

---

## Features

1. **Online Manga Reading**: Read manga from online sources (currently powered by **Weeb Central**).
2. **Favorites**: Add titles to a favorites list for easy access.
3. **Library**: Add titles to a personal library.
4. **E-Ink Optimized UI**: A clean, high-contrast interface designed specifically for E-Ink screens.
5. **Navigation**:
   - Tap **Left** for Previous Page.
   - Tap **Right** for Next Page.
   - Tap **Center** to open the menu.
   - Keyboard support (Left/Right arrows).

## Work in Progress (WIP)

The following features are currently in development or partially implemented:

1. **Offline Reading**: Saving chapters for offline reading is currently being reworked.
2. **Caching**: Improved caching for smoother reading is in progress.
3. **Download Manager**: Better management of downloaded chapters.

## Installation

1. Make sure you have 300 MB or more space on your Kobo microSD card.
2. Install <a href="https://www.mobileread.com/forums/showthread.php?t=329525">NickelMenu</a>. If you don't have it installed already, click the link and follow the instructions there. NickelMenu will help us create a menu item to launch AMR.
3. To prevent images from showing up as books, perform the following operation by connecting your Kobo to your computer:
   - Navigate to KOBOeReader/.kobo/Kobo and open Kobo eReader.conf in the text editor of your choice
   - Scroll down to find `[FeatureSettings]` , if it doesn't exist, create it! (type it in)
   - Under `[FeatureSettings]`, paste the following: `ExcludeSyncFolders=\\.(?!kobo|adobe).*?`
4. Download the latest release of Atom Manga Reader.
5. Unzipping the file should give you a folder named ".AMR". Copy this folder to the root of your microSD card. (The root is the KOBOeReader folder. Simply drag ".AMR" to KOBOeReader)
6. Create a menu entry using NickelMenu.
   - From KOBOeReader/.AMR, open "nickelmenuconfig.txt" and copy it's contents.
   - Navigate to KOBOeReader/.adds/nm/
   - If a config file does not exist, create a new text file with any name, for example, "config.txt"
   - Paste the contents from "nickelmenuconfig.txt" into the config file.
7. Safely eject your eReader from your computer.

You are now ready to use Atom Manga Reader!

## Updating

1. Connect your Kobo to your computer and Navigate to KOBOeReader
2. If you wish to retain your manga library and favorites, make a copy your library folder (KOBOeReader/.AMR/static/library) and favorites (KOBOeReader/.AMR/static/mangafavs.csv) to a different location on your computer.
3. Download the latest release.
4. Unzipping the file should give you a folder named ".AMR". Copy this folder to the root of your microSD card. (The root is the KOBOeReader folder. Simply drag ".AMR" to KOBOeReader). This will replace the older .AMR folder with the new one. Alternatively, you can manually delete the .AMR folder in the KOBOeReader folder and copy over the new one obtained by unzipping the downloaded zip file.
5. Move the manga library and favorites to the newly replaced .AMR folder in the same locations. The manga library "library" folder favorites "mangafavs.csv" should both be moved to the KOBOeReader/.AMR/static/ folder
6. Safely eject your eReader from your computer.

The application has now been updated.

## Launching and Using AMR

Once you have installed AMR, you can launch the app by performing the following steps:

1. Open NickelMenu on your Kobo eReader and select "Start AMR server". Click "OK".
2. Open NickelMenu on your Kobo eReader and select "Open AMR".
3. Enjoy! More details and instructions for use can be found under "Navigation" from the hamburger menu in the top left corner of the application/browser window.
4. Make sure you always exit the app by navigating to "Close app" from the hamburger menu. Press the "Shut down" button. (Not shutting down this way will keep the AMR server running in the background. You don't want there to be multiple instances using up CPU resources when you start AMR again next time. So, it's best to close the app this way)

### Note:

You will need to be connected to a network to open the application, since it works using the kobo browser. (You do not need an internet connection. Connecting to a network without internet access seems to work)

## Uninstall AMR

To uninstall AMR, connect your Kobo to your computer and navigate to KOBOeReader/.AMR and create a file (any type) called "uninstall".
Next, run the startup script from your Kobo: go to nickel menu and select Start AMR server.
This will remove AMR and all of the contents of KOBOeReader/.AMR. Any downloaded contents will be lost. Make a backup of the KOBOeReader/.AMR/static/library directory to keep your downloads.
To remove the NickelMenu entries, you will have to open the config file from KOBOeReader/.adds/nm/ and remove the entries manually.

## Obligatory Disclaimer:

I have developed and tested the application on a Kobo Libra 2, which is the only Kobo device I own. I cannot guarantee that it will work as intended on other Kobo devices. Use at your own risk. I am not responsible for any damages/ bricking of your devices.

## Known Bugs and occurances:

1. The first time you open the app using "Open AMR", it may fail, as it needs a couple of seconds for the server to start. Future trials will be faster
2. There is a small image near the hamburger menu icon when the app opens up. This seems to be an artifact of the eink screen. It disappears after clicking/touching anywhere else.
3. Once a chapter link is clicked, loading the first manga page may require about 30 seconds. This is because all of the images are downlaoded to the cache for fast scrolling.
4. Sometimes, when opening a manga chapter, the screen will be blank except for a small box with a "?" in the middle of the screen. Hitting the refresh icon of the browser will solve this problem. This seems to happen because some times the program jumps to the next step without completing the current step (starts to show image without actually fetching it first)

## More

Go to <a href="https://www.mobileread.com/forums/showthread.php?t=348950">mobileread</a> for more details and to ask questions

## Acknowlegements

Many thanks to all the developers of <a href="https://github.com/pgaskin/NickelMenu">NickelMenu</a> for creating a tool that allows us to experiment with our Kobos.

The idea of using the browser and the startup script were inspired by the <a href="https://www.mobileread.com/forums/showthread.php?t=262353">WebPortal</a> project by <a href="https://github.com/frostschutz">frostschutz</a>

## Leave a Tip!

If you enjoyed using Atom Manga Reader, leave a nice comment on the mobileread page. Better yet, leave me a tip in my tip jar! (paypal: buxared14@gmail.com) As a novice in python, HTML and Linux, it took me many hours and many months to get here. AMR will always remain free, so consider donating. Thanks!

## I hope you have fun using Atom Manga Reader!
