//    Copyright 2008, 2009, 2010, 2022 Charles S. Hubbard, Jr.
//
//    This file is part of Rationale.
//
//    Rationale is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    Rationale is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with Rationale.  If not, see <http://www.gnu.org/licenses/>.
					  
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
