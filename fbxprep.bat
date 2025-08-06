::####################################################################################
::# Kalev Mölder       2025       https://tinkering.ee        molder.kalev@gmail.com #
::#                                                                                  #
::# FBX Prep Launch Bat Script                                                       #
::####################################################################################

:: Assumes that Python with TkInter is installed and in path
:: Simply runs the python script. 

:: Seems trivial but I find that
:: when working with graphical assets my brain is in "mouse mode"
:: So opening up a terminal and typing some command out
:: feels like friction at that moment.

:: having something to just doubleclick
:: is really nice in that moment

cmd /c "python %CD%\fbxprepui.py"