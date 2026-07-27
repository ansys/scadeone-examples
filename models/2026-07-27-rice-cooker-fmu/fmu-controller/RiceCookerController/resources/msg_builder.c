#include "swan_types.h"

#define SIZE_MSG 6

char* displayTime(swan_uint32 digits1, swan_uint32 digits2) {
    static char msg[SIZE_MSG];
    msg[0] = (char)((digits1 / 10) + '0');
    msg[1] = (char)((digits1 % 10) + '0');
    msg[2] = ':';
    msg[3] = (char)((digits2 / 10) + '0');
    msg[4] = (char)((digits2 % 10) + '0');
    msg[5] = (char)('\0'); // Null terminator
    return msg;
}

/* Function to convert seconds to MM:SS format for display */
char* Sec2MMSS_Utils_Msg(swan_uint32 sec) {
    swan_uint32 minutes = sec / 60;
    swan_uint32 seconds = sec % 60;
    return displayTime(minutes, seconds);
}

/* Function to convert seconds to HH:MM format for display */
char* Sec2HHMM_Utils_Msg(swan_uint32 sec) {
    swan_uint32 minutes = sec / 60;
    swan_uint32 hours = minutes / 60;
    minutes = minutes % 60;
    return displayTime(hours, minutes);
}