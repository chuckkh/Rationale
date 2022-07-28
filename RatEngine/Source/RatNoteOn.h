#pragma once
#include "RatEvent.h"
class RatNoteOn :
    public RatEvent
{
    int trigger() override;
};

