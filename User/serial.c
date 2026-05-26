#include "serial.h"
#include <string.h>

#define RING_SIZE 64

static volatile uint8_t rx_ring[RING_SIZE];
static volatile uint8_t rx_head = 0;
static volatile uint8_t rx_tail = 0;

void Serial_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    USART_InitTypeDef USART_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA | RCC_APB2Periph_USART1, ENABLE);

    /* PA9 = USART1 TX (alternate push-pull) */
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    /* PA10 = USART1 RX (input floating) */
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
    GPIO_Init(GPIOA, &GPIO_InitStructure);

    /* USART1: 115200, 8N1 */
    USART_InitStructure.USART_BaudRate = 115200;
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;
    USART_InitStructure.USART_StopBits = USART_StopBits_1;
    USART_InitStructure.USART_Parity = USART_Parity_No;
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;
    USART_Init(USART1, &USART_InitStructure);

    /* Enable RX interrupt */
    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);

    /* NVIC configuration */
    NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);

    USART_Cmd(USART1, ENABLE);
}

void USART1_IRQHandler(void)
{
    if (USART_GetITStatus(USART1, USART_IT_RXNE) != RESET) {
        uint8_t next = (rx_head + 1) % RING_SIZE;
        if (next != rx_tail) {
            rx_ring[rx_head] = USART_ReceiveData(USART1);
            rx_head = next;
        } else {
            USART_ReceiveData(USART1); /* overflow: discard */
        }
    }
}

uint8_t Serial_GetCommand(void)
{
    static char buf[16];
    static uint8_t idx = 0;

    while (rx_tail != rx_head) {
        char c = (char)rx_ring[rx_tail];
        rx_tail = (rx_tail + 1) % RING_SIZE;

        if (c == '\n' || c == '\r') {
            if (c == '\r') continue; /* skip CR, wait for LF */
            if (idx == 0) continue;
            buf[idx] = '\0';
            idx = 0;

            if (!strcmp(buf, "INIT"))   return SERIAL_CMD_INIT;
            if (!strcmp(buf, "IDLE"))   return SERIAL_CMD_IDLE;
            if (!strcmp(buf, "CODE"))   return SERIAL_CMD_CODE;
            if (!strcmp(buf, "DOCS"))   return SERIAL_CMD_DOCS;
            if (!strcmp(buf, "THINK"))  return SERIAL_CMD_THINK;
            if (!strcmp(buf, "SEARCH")) return SERIAL_CMD_SEARCH;
            if (!strcmp(buf, "EXPER"))  return SERIAL_CMD_EXPER;
            if (!strcmp(buf, "ERROR"))  return SERIAL_CMD_ERROR;
            if (!strcmp(buf, "STATUS")) return SERIAL_CMD_STATUS;
        } else if (idx < 15) {
            buf[idx++] = c;
        } else {
            idx = 0; /* overflow, reset */
        }
    }
    return SERIAL_CMD_NONE;
}

void Serial_SendString(const char *str)
{
    while (*str) {
        while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET);
        USART_SendData(USART1, *str++);
    }
}
