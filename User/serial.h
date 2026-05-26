#ifndef __SERIAL_H
#define __SERIAL_H

#include "stm32f10x.h"

#define SERIAL_CMD_NONE    0xFF
#define SERIAL_CMD_INIT    0
#define SERIAL_CMD_IDLE    1
#define SERIAL_CMD_CODE    2
#define SERIAL_CMD_DOCS    3
#define SERIAL_CMD_THINK   4
#define SERIAL_CMD_SEARCH  5
#define SERIAL_CMD_EXPER   6
#define SERIAL_CMD_ERROR   7
#define SERIAL_CMD_STATUS  8

void Serial_Init(void);
uint8_t Serial_GetCommand(void);
void Serial_SendString(const char *str);

#endif
