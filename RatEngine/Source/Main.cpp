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

class Application : public juce::JUCEApplication
{
public:
    //==========================================================================
    Application() = default;
    const juce::String getApplicationName() override { return "RationaleEngine"; }
    const juce::String getApplicationVersion() override { return "0.0.1"; }

    void initialise(const juce::String&) override
    {
        int cbport = 5899;
        auto clArgs = getCommandLineParameterArray();
        if (clArgs.size() > 1)
        {
            const juce::String *portStr = &clArgs[1];
            if (portStr->containsOnly("0123456789")) {
                cbport = portStr->getIntValue();
            }
        }
        //ratEngine->setCbPort(cbport);
        ratEngine.reset(new RatEngine(cbport, *this));
        ratEngine->run();

        
    }

    void shutdown() override
    {
    }


    std::unique_ptr<RatEngine> ratEngine;
};

START_JUCE_APPLICATION (Application)
