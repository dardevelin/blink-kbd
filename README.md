#blink-kbd - hexchat plugin GPLv3
---
**blink-kbd** is a python plugin for **hexchat** which blinks the backlight
of your keyboard or any other light controlled by lightcontroler.sh
whenever you get highlighted/notification in hexchat.

blink-kbd will leave the light on until hexchat regains
focus/activity. Due to this, if the blinking has already started
it will finished the cycle before consuming the notification.

**lightcontroler.sh** by default works with keyboard backlight.
I have only tested with *asus n551j-cn220h* laptop. However the plugin
is made such that it invocates lightcontroler.sh with the commands
'up' for *'lightON'* and 'down' for *'lightOFF'*. so as long you
_change/replace lightcontroler.sh_ to suit your environment
and maintain the behavior of **up** to represent _ON_ and **down** for _OFF_
you shouldn't need to change anything else.


##LICENSE - GPLv3 no later option. Ignore any references to later versions
See LICENSE to know your rights or go to
http://www.gnu.org/licenses/gpl-3.0.txt
