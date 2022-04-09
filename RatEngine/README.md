# RatEngine
The inner engine for Rationale.
This is written in C++ using JUCE, to replace the previous use of the Csound API for better audio and MIDI support.
This engine, in binary form, is called from within Rationale as a subprocess and controlled using threads and sockets.