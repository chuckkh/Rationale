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