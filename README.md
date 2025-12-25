# AtomMangaReader

**AtomMangaReader**, also referred to as **AMR**, is an application designed to read manga on Kobo eReaders.  
It is a lightweight, Kobo-first manga reader focused on simplicity, performance, and minimal user interface, built to work within the constraints of Kobo devices and their built-in browser.

AtomMangaReader is a fork of **Banana Manga Reader** and has since diverged in design and implementation.  
It is maintained independently and prioritises modern, reliable sources and a cleaner reading experience.

The application is designed to be easy to install and use, with minimal configuration required. While customization is possible by editing the HTML and Python code, the default setup aims to provide a complete, distraction-free manga reading experience out of the box.

AtomMangaReader focuses on **reading manga you already know about**, rather than discovery. As a result, search functionality is intentionally simple.

---

## Features

- Read manga from online sources optimised for reliability and performance
- Add manga titles to a favourites list for quick access
- Download chapters for offline reading  
  - A network connection is required to open the browser  
  - An internet connection is **not** required once chapters are downloaded
- Clean, unobstructed reading experience  
  - No UI elements while reading pages  
  - Tap left or right edges to change pages  
  - Tap the centre to open the menu
- Add your own manga manually to the library  
  - On the microSD card, navigate to:  
    ` 
    KOBOeReader/.AMR/static/library
    ` 
  - Folder structure:
    ` 
    library/
      Manga Title/
        Chapter Title/
          page001.png
          page002.jpg
    ` 
  - Extracted CBR/CBZ archives already match this layout
- All files remain inside the mnt/onboard partition  
  - No files are written to / or /usr  
  - Updates, removal, and backups are safe and simple

---

## Installation

1. Ensure at least **300 MB** of free space on your Kobo microSD card.
2. Install **NickelMenu**:  
   https://www.mobileread.com/forums/showthread.php?t=329525
3. Prevent downloaded images from appearing as books:
   - Connect your Kobo to your computer
   - Open:
     ` 
     KOBOeReader/.kobo/Kobo eReader.conf
     ` 
   - Under [FeatureSettings], add:
     ` 
     ExcludeSyncFolders=\.(?!kobo|adobe).*?
     ` 
4. Download the latest AtomMangaReader release from the Releases page.
5. Extract the archive. You should obtain a folder named .AMR.
6. Copy .AMR into the root KOBOeReader directory.
7. Create a NickelMenu entry:
   - Open:
     ` 
     KOBOeReader/.AMR/nickelmenuconfig.txt
     ` 
   - Copy its contents
   - Paste them into a config file inside:
     ` 
     KOBOeReader/.adds/nm/
     ` 

Safely eject your device when finished.

---

## Updating

1. Connect your Kobo to your computer.
2. Back up the following if you wish to keep them:
   - KOBOeReader/.AMR/static/library
   - KOBOeReader/.AMR/static/mangafavs.csv
3. Download the latest release.
4. Replace the existing .AMR folder with the new one.
5. Restore your library and favourites to the same locations.
6. Safely eject the device.

---

## Launching and Using AtomMangaReader

1. Open NickelMenu and select **Start AMR server**
2. Open NickelMenu again and select **Open AMR**
3. Read and enjoy
4. Always exit the app via **Close app**  **Shut down**

Failing to shut down correctly may leave the server running in the background.

---

## Notes

- A network connection is required to open the application because it runs through the Kobo browser.
- An internet connection is **not** required if content is already cached or downloaded.

---

## Uninstalling AtomMangaReader

1. Connect your Kobo to your computer.
2. Navigate to:

