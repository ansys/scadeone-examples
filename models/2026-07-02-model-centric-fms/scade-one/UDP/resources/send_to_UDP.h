#ifndef SEND_TO_UDP_H
#define SEND_TO_UDP_H

#include "udp.h"

void send_to_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* at */
  const address_IP *at,
  /* buffer */
  const array_u8_1036 *buffer,
  /* sz */swan_uint32 sz,
  /* s_out */socket_UDP * restrict s_out,
  /* sz_sent */swan_uint32 * restrict sz_sent);

#endif // SEND_TO_UDP_H