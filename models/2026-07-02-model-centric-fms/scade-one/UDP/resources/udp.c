
#include <winsock2.h>
#include <stdio.h>
#include <string.h>
#include "udp.h"

#pragma comment(lib, "ws2_32.lib")

void socket_init_UDP(socket_UDP * restrict swan_c1){}


void session_init_UDP(session_UDP * restrict swan_c1){}



/* UDP::startup */
void startup_UDP(/* wsa */session_UDP * restrict wsa){
    WSAStartup(MAKEWORD(2, 2), wsa);
}

/* UDP::cleanup */
void cleanup_UDP(/* sess */ const session_UDP *sess){
    WSACleanup();
}




/* UDP::mk_socket */
void mk_socket_UDP( const session_UDP *sess, socket_UDP * restrict s){


    *s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    /* Make it non blocking: reading to the socket returns nothing if there is no data */
    u_long mode = 1; /* 1 = non-blocking, 0 = blocking */
    ioctlsocket(*s, FIONBIO, &mode);

  }


/* UDP::bind */
void bind_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* local_address */
  const address_IP *local_address,
  /* s_out */socket_UDP * restrict s_out){
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(local_address->port);
    addr.sin_addr.S_un.S_un_b.s_b1 = local_address->address[0];
    addr.sin_addr.S_un.S_un_b.s_b2 = local_address->address[1];
    addr.sin_addr.S_un.S_un_b.s_b3 = local_address->address[2];
    addr.sin_addr.S_un.S_un_b.s_b4 = local_address->address[3];
    
    bind(*s_in, (struct sockaddr *)&addr, sizeof(addr));
    *s_out = *s_in;
  }

/* UDP::send_to */
void send_to_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* at */
  const address_IP *at,
  /* buffer */
  const array_u8_1036 *buffer,
  /* sz */swan_uint32 sz,
  /* s_out */socket_UDP * restrict s_out,
  /* sz_sent */swan_uint32 * restrict sz_sent){

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(at->port);
    addr.sin_addr.S_un.S_un_b.s_b1 = at->address[0];
    addr.sin_addr.S_un.S_un_b.s_b2 = at->address[1];
    addr.sin_addr.S_un.S_un_b.s_b3 = at->address[2];
    addr.sin_addr.S_un.S_un_b.s_b4 = at->address[3];

    *sz_sent = sendto(*s_in, (const char *)(&buffer[0]), sz, 0, (struct sockaddr *)&addr, sizeof(addr));
    *s_out = *s_in;
  }

void recv_from_UDP(
  /* s_in */
  const socket_UDP *s_in,
  /* s_out */socket_UDP * restrict s_out,
  /* buffer */array_u8_1036 * restrict buffer,
  /* sz */swan_uint32 * restrict sz,
  /* from */address_IP * restrict from){

    struct sockaddr_in addr;
    int addr_len = sizeof(addr);
    int recv_sz;

    recv_sz = recvfrom(*s_in, (char *)(*buffer), 1036, 0, (struct sockaddr *)&addr, &addr_len);
    if (recv_sz < 0) {     
      *sz = 0;
    } else {
      *sz = recv_sz;
    }

    from->port = ntohs(addr.sin_port);
    from->address[0] = addr.sin_addr.S_un.S_un_b.s_b1;
    from->address[1] = addr.sin_addr.S_un.S_un_b.s_b2;
    from->address[2] = addr.sin_addr.S_un.S_un_b.s_b3;
    from->address[3] = addr.sin_addr.S_un.S_un_b.s_b4;
    *s_out = *s_in;
}


/* UDP::close */
void close_UDP(/* s */ const socket_UDP *s){
    closesocket(*s);    
}


