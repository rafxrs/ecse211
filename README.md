# Sample code for Robots!

Whenever you work with code in DPM, we recommend that you always have the `utils/` folder with your main scripts. "main scripts" meaning: "any code files with .py extension that you execute to control the robot". You put the main scripts next to the `utils/` folder so that you can use the library utility code we provide to you. We wrote this code to make programming the robot easier for you. You don't have to use it, but it is likely to help you a lot to be using it.

# Special Notes (optional read)

In the labs, we also provide a method of installing `simpleaudio` onto the BrickPi for sound production. Our `utils.sound` utility code utilizes `simpleaudio` to create an even simpler method of producing sounds than simpleaudio already has. You may use `simpleaudio` itself, but you must still work within the constraints of the labs that use and produce sound.

The original BrickPi API can be found through https://github.com/DexterInd/BrickPi3 and more specifically, this file: https://github.com/DexterInd/BrickPi3/blob/master/Software/Python/brickpi3.py on GitHub as well. Our `utils.brick` is a wrapper library on top of this `brickpi3` api, which is already on every BrickPi robot when you get it. You don't need to install anything. You may use either our `utils.brick` wrapper library or `brickpi3`, but again, we simplified and added many utility funcitons to `utils.brick` to make programming easier.