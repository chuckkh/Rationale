#pragma once
#include "RatEvent.h"
class RatNoteOff :
    public RatEvent
{
    int trigger() override;
};

