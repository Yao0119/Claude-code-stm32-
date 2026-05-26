#include "state_machine.h"

#define IDLE_TIMEOUT_MS  30000
#define ANIM_INTERVAL_MS 500

static uint8_t current_state = STATE_INIT;
static volatile uint8_t refresh_flag = 0;
static volatile uint32_t sys_ticks = 0;
static uint32_t last_activity_tick = 0;
static uint32_t last_anim_tick = 0;
static uint8_t anim_frame = 0;

static const char *state_names[STATE_COUNT] = {
    "INIT", "IDLE", "CODE", "DOCS", "THINK", "SEARCH", "EXPER", "ERROR"
};

static const char *status_texts[STATE_COUNT] = {
    "Booting...",      /* INIT   - 10 chars */
    "Idle Ready",       /* IDLE   - 10 chars */
    "Write Code",       /* CODE   - 10 chars */
    "Write Docs",       /* DOCS   - 10 chars */
    "Analyzing..",      /* THINK  - 11 chars */
    "Searching..",      /* SEARCH - 11 chars */
    "Experiments",      /* EXPER  - 11 chars */
    "ERROR! Alert"      /* ERROR  - 11 chars */
};

void State_Init(void)
{
    current_state = STATE_INIT;
    refresh_flag = 1;
}

void State_Transition(uint8_t new_state)
{
    if (new_state < STATE_COUNT && new_state != current_state) {
        current_state = new_state;
        refresh_flag = 1;
    }
}

uint8_t State_GetCurrent(void)
{
    return current_state;
}

const char* State_GetName(void)
{
    return state_names[current_state];
}

const char* State_GetText(uint8_t state)
{
    if (state < STATE_COUNT)
        return status_texts[state];
    return "";
}

uint8_t State_NeedsRefresh(void)
{
    return refresh_flag;
}

void State_ClearRefresh(void)
{
    refresh_flag = 0;
}

void State_InitSysTick(void)
{
    SysTick->LOAD = 72000 - 1;
    SysTick->VAL  = 0;
    SysTick->CTRL = 0x07; /* HCLK, TICKINT, ENABLE */
}

void State_TickIncrement(void)
{
    sys_ticks++;
}

void State_ResetIdleTimer(void)
{
    last_activity_tick = sys_ticks;
}

void State_CheckIdle(void)
{
    if (current_state != STATE_IDLE) {
        if ((sys_ticks - last_activity_tick) >= IDLE_TIMEOUT_MS) {
            current_state = STATE_IDLE;
            refresh_flag = 1;
            last_activity_tick = sys_ticks;
            anim_frame = 0;
            last_anim_tick = sys_ticks;
        }
    }
}

void State_CheckAnim(void)
{
    if ((sys_ticks - last_anim_tick) >= ANIM_INTERVAL_MS) {
        last_anim_tick = sys_ticks;
        anim_frame++;
        refresh_flag = 1;
    }
}

uint8_t State_GetFrame(void)
{
    return anim_frame;
}

void State_ResetAnim(void)
{
    anim_frame = 0;
    last_anim_tick = sys_ticks;
}
