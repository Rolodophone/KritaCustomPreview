#!/bin/bash

# I created this script to make it easier to apply changes to the plugin
# IT IS ONLY TESTED ON MY PC; IT MAY NOT WORK FOR YOURS

echo 'I created this script to make it easier to apply changes to the plugin
IT IS DESIGNED SOLELY FOR MY PC; IT MAY NOT WORK FOR YOURS
'

cp -r ./custompreview ~/.local/share/krita/pykrita
cp ./custompreview.desktop ~/.local/share/krita/pykrita
killall krita && krita