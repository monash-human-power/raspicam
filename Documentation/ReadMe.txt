This repo handles the software management of the raspberry pi camera system the Monash Human Power Team uses.

A brief list of the relevant files is included here:
1) Camera.py = Main Camera script which handles camera feed and overlays time onto the display
2) CameraVel.py = Secondary Camera script which handles camera feed and overlays speed in km/hr onto the display. Uses a reed switch input.
3) convert.sh = Shell script for handling conversion of video files at the end of a run. Also manages SD card storage of video files so SD card does not get too full.
4) run.py = Master script which indicates status of system to external observers and runs other files based on input from a user.
5) orchestrator_test.py = Test script for orchestrator.py. To run enter 'pytest' in the terminal to run the tests

When running these scripts please don't use the idle IDE on the raspberry pi. Instead open a terminal window and navigate to "cd ~/Documents/MHP_Raspicam" and run
scripts using "python ____.py". This is because files may contain a mix of tabs and spaces and it may not work in the idle IDE. To fix issues in the idle IDE relating to this
parse through the files and replace any tabs with 4 spaces.
