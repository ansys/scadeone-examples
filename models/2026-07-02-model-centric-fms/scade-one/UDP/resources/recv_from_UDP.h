#ifndef RECV_FROM_UDP_H
#define RECV_FROM_UDP_H

#include "udp.h"


  void recv_from_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* s_out */socket_UDP * restrict s_out,
  /* buffer */array_u8_1036 * restrict buffer,
  /* sz */swan_uint32 * restrict sz,
  /* from */address_IP * restrict from);
#endif // RECV_FROM_UDP_H
