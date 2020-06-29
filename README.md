# Krita Custom Preview

A docker for displaying a custom preview of your image.

![Docker](https://raw.githubusercontent.com/Rolodophone/KritaCustomPreview/master/screenshots/docker.png)

This plugin adds a docker which displays a smaller version of the image you have open. This can be used to get a sense of how your drawing looks overall while you are zoomed in. The preview resizes dynamically, so you can choose how large or small you want it. In addition, it uses nearest-neighbor scaling, so it's perfect for pixel art.

The docker includes two buttons for setting foreground and background images, which are displayed in front of and behind the preview. You could use the foreground image for seeing how your drawing looks like as a round icon. The path to these foreground and background images is saved in the .kra file.

I've included a few basic foreground and background images that people might find useful, but of course you can make your own as well! If you think other people would find your own foreground or background image useful, feel free to upload them to GitHub and submit a pull request.

## How to install

Copy the _custompreview_ folder and _custompreview.desktop_ to your _pykrita_ folder. You can find the _pykrita_ folder by opening Krita and going to _Settings_ > _Manage resources..._ > _open resource folder_. Then restart Krita and enable the plugin in _Settings_ > _Configure Krita_ > _Python Plugin Manager_.