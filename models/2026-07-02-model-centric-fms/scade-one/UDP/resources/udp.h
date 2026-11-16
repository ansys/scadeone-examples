/* $ Ansys Scade One - Swan Code Generator - Version 2.4.0 - Build 0133 - Prerelease 
** Command: swan_cg.exe config.json
*************************************************************$ */
#ifndef UDP_H_
#define UDP_H_

#include <winsock2.h>
#include <swan_types.h>

typedef SOCKET socket_UDP;

extern void socket_init_UDP(socket_UDP * restrict swan_c1);

#define swan_cp_socket_UDP(swan_c1, swan_c2)                                  \
  (swan_assign((swan_c1), (swan_c2), sizeof (socket_UDP)))

extern swan_bool swan_eq_socket_UDP(
  const socket_UDP *swan_c1,
  const socket_UDP *swan_c2);


typedef WSADATA session_UDP;

extern void session_init_UDP(session_UDP * restrict swan_c1);

#define swan_cp_session_UDP(swan_c1, swan_c2)                                 \
  (swan_assign((swan_c1), (swan_c2), sizeof (session_UDP)))

extern swan_bool swan_eq_session_UDP(
  const session_UDP *swan_c1,
  const session_UDP *swan_c2);
#endif /* UDP_H_ */
/* $ Ansys Scade One - Swan Code Generator - Version 2.4.0 - Build 0133 - Prerelease 
** swan_imported_types.dh
*************************************************************$ */
