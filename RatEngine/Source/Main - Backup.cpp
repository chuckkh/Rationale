/*
  ==============================================================================

    This is the audio and MIDI engine for the Rationale microtonal composition program.

  ==============================================================================
*/

#include <JuceHeader.h>
#include "RatEngine.h"
//==============================================================================
int main (int argc, char* argv[])
{
    int portno;
    char* p;
    portno = (argc > 1 ? strtol(argv[1], &p, 10) : 5899);

    if (argc > 1) { std::cout << argv[1] << " " << portno << std::endl; }

    RatEngine ratEngine(portno);
    ratEngine.run();
    ratEngine.endItAll();
    return 0;
}
