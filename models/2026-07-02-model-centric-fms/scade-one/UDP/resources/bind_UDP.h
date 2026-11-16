#ifndef BIND_UDP_H
#define BIND_UDP_H


#include "udp.h"
  void bind_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* local_address */
  const address_IP *local_address,
  /* s_out */socket_UDP * restrict s_out);
#endif // BIND_UDP_H