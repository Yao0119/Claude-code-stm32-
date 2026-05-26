#include "display.h"
#include "OLED.h"
#include "cat_sprites.h"
#include "state_machine.h"

extern const uint8_t OLED_F8x16[][16];

/* Write one 8x16 char at (page, pixel_col). Uses pages page..page+1 */
static void Display_WriteChar(uint8_t page, uint8_t col, char c)
{
    uint8_t idx;
    if (c < ' ' || c > '~') c = ' ';
    idx = c - ' ';
    OLED_SetCursor(page, col);
    for (uint8_t i = 0; i < 8; i++) {
        OLED_WriteData(OLED_F8x16[idx][i]);
    }
    OLED_SetCursor(page + 1, col);
    for (uint8_t i = 0; i < 8; i++) {
        OLED_WriteData(OLED_F8x16[idx][i + 8]);
    }
}

void Display_WriteString(uint8_t page, uint8_t col_pixels, const char *str)
{
    while (*str) {
        Display_WriteChar(page, col_pixels, *str);
        col_pixels += 8;
        str++;
    }
}

/* Blit 72x48 cat sprite frame at (base_page, col) */
static void Display_Cat(uint8_t base_page, uint8_t col, uint8_t sprite_idx, uint8_t frame)
{
    const CatSprite *cs = &cat_sprites[sprite_idx];
    const uint8_t (*sprite)[72] = cs->frames[frame % cs->count];

    for (uint8_t page = 0; page < 6; page++) {
        OLED_SetCursor(base_page + page, col);
        for (uint8_t c = 0; c < 72; c++) {
            OLED_WriteData(sprite[page][c]);
        }
    }
}

/*
 * Screen layout (128x64):
 * Pages 0-1: Status name centered (8x16 font)
 * Pages 2-7: 72x48 cat sprite centered at col 28
 */
void Display_Init(void)
{
    OLED_Clear();
}

void Display_Refresh(uint8_t state, uint8_t frame)
{
    const char *text = State_GetText(state);
    uint8_t len = 0;
    while (text[len]) len++;
    uint8_t col = (128 - len * 8) / 2;

    /* Status name centered on pages 0-1 */
    Display_WriteString(0, col, text);

    /* Cat sprite centered on pages 2-7 */
    Display_Cat(2, 28, state, frame);
}
