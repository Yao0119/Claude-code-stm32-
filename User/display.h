#ifndef __DISPLAY_H
#define __DISPLAY_H

#include "stm32f10x.h"

void Display_Init(void);
void Display_Refresh(uint8_t state, uint8_t frame);
void Display_WriteString(uint8_t page, uint8_t col_pixels, const char *str);

#endif
