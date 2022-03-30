#include "JuceHeader.h"
#include <queue>
#include <map>
#include "RatIO.h"
#include "RatEvent.h"
#include "juce_audio_devices/juce_audio_devices.h"

#pragma once

class RatIOManager : juce::Timer	
{
public:
	
private:
	juce::OwnedArray<juce::OwnedArray<RatIO>> outputs;
	juce::OwnedArray<juce::OwnedArray<RatIO>> inputs;
	std::queue<RatEvent> events;
	juce::Array<MidiDeviceInfo> availableMidiDevices;
};

