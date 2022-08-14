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

#include "RatMidiInputCallback.h"

void RatMidiInputCallback::handleIncomingMidiMessage(juce::MidiInput* input, const juce::MidiMessage& msg)
{

	if (msg.isSongPositionPointer()) {
		std::cout << "\nReceived: SPP: " << msg.getSongPositionPointerMidiBeat();
	}
	else if (msg.isMidiClock()) {
		std::cout << "...tick ";
	}
	else if (msg.isMidiStart()) { std::cout << '\n' << "Received: MIDI Start"; }
	else if (msg.isMidiStop()) { std::cout << '\n' << "Received: MIDI Stop"; }
	else if (msg.isMidiContinue()) { std::cout << '\n' << "Received: MIDI Continue"; }
	else if (msg.isSysEx()) {
		std::cout << '\n' << "Received SysEx:";
		int sz = msg.getSysExDataSize();
		for (int i = 0; i < sz; i++) {
			std::cout << " " << * (msg.getSysExData() + i);
		}
	}
}