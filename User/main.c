#include "stm32f10x.h"
#include "OLED.h"
#include "serial.h"
#include "display.h"
#include "state_machine.h"

int main(void)
{
    OLED_Init();
    Serial_Init();
    Display_Init();
    State_Init();
    State_InitSysTick();
    State_ResetIdleTimer();

    Display_Refresh(State_GetCurrent(), 0);

    while (1)
    {
        uint8_t cmd = Serial_GetCommand();

        if (cmd == SERIAL_CMD_STATUS) {
            Serial_SendString(State_GetName());
            Serial_SendString("\r\n");
        } else if (cmd != SERIAL_CMD_NONE) {
            State_Transition(cmd);
            State_ResetIdleTimer();
            State_ResetAnim();
        }

        State_CheckIdle();
        State_CheckAnim();

        if (State_NeedsRefresh()) {
            Display_Refresh(State_GetCurrent(), State_GetFrame());
            State_ClearRefresh();
            State_InitSysTick(); /* Delay stops SysTick, restart it */
        }
    }
}
