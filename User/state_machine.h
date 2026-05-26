#ifndef __STATE_MACHINE_H
#define __STATE_MACHINE_H

#include "stm32f10x.h"

#define STATE_INIT    0
#define STATE_IDLE    1
#define STATE_CODE    2
#define STATE_DOCS    3
#define STATE_THINK   4
#define STATE_SEARCH  5
#define STATE_EXPER   6
#define STATE_ERROR   7
#define STATE_COUNT   8

void State_Init(void);
void State_Transition(uint8_t new_state);
uint8_t State_GetCurrent(void);
const char* State_GetName(void);
const char* State_GetText(uint8_t state);
uint8_t State_NeedsRefresh(void);
void State_ClearRefresh(void);

void State_InitSysTick(void);
void State_TickIncrement(void);
void State_ResetIdleTimer(void);
void State_CheckIdle(void);

void State_CheckAnim(void);
uint8_t State_GetFrame(void);
void State_ResetAnim(void);

#endif
