#include "sgl.h"
#include <stdlib.h>
#include <time.h>

static SGLuint32 lTexture0[107UL] = 
{
 0x000000U, 0x000000U, 988U, 0xFFFFFFU, 0x000000U, 0xFFFFFFU, 0x000000U, 0x000000U, 75U, 0xFFFFFFU, 0xFFFFFFU, 1U, 0x000000U, 0x000000U, 74U, 0xFFFFFFU, 0xFFFFFFU, 0U, 0x000000U, 0xFFFFFFU,
 0xFFFFFFU, 0U, 0x000000U, 0x000000U, 75U, 0xFFFFFFU, 0x000000U, 0x000000U, 77U, 0xFFFFFFU, 0x000000U, 0x000000U, 505U, 0xFFFFFFU, 0xFFFFFFU, 1U, 0x000000U, 0x000000U, 74U, 0xFFFFFFU,
 0x000000U, 0x000000U, 1U, 0xFFFFFFU, 0x000000U, 0x000000U, 72U, 0xFFFFFFU, 0x000000U, 0x000000U, 3U, 0xFFFFFFU, 0x000000U, 0x000000U, 71U, 0xFFFFFFU, 0x000000U, 0x000000U, 3U, 0xFFFFFFU,
 0x000000U, 0x000000U, 71U, 0xFFFFFFU, 0x000000U, 0x000000U, 3U, 0xFFFFFFU, 0x000000U, 0x000000U, 72U, 0xFFFFFFU, 0x000000U, 0x000000U, 1U, 0xFFFFFFU, 0x000000U, 0x000000U, 74U, 0xFFFFFFU,
 0xFFFFFFU, 1U, 0x000000U, 0x000000U, 837U, 0xFFFFFFU, 0x000000U, 0x000000U, 77U, 0xFFFFFFU, 0x000000U, 0x000000U, 75U, 0xFFFFFFU, 0xFFFFFFU, 3U, 0x000000U, 0x000000U, 75U, 0xFFFFFFU,
 0x000000U, 0x000000U, 77U, 0xFFFFFFU, 0x000000U, 0x000000U, 1336U
};

SGLuint8 lTexture1[14400UL];

 void getTexture(SGLuint8 rand_power, SGLuint8 (*texPix)[60UL][80UL]) {
	SGLuint32 i,j,k,l;
	i=0;
	k=0;
	l=0;
	SGLuint32 rndValue;
	srand( time( NULL ) );	
		
	while (i < 107UL) {
		if ( i < 106UL && lTexture0[i] == lTexture0[i+1] ) {
			
			for (j=0; j < lTexture0[i+2] + 2; j++){
				rndValue = rand() % 100;
				if ( rndValue > rand_power) {
					rndValue = (lTexture0[i] + rndValue) % 255;
				} else {
					rndValue = lTexture0[i];
				}
				
				lTexture1[k] = rndValue;
				lTexture1[k+1] = rndValue;
				lTexture1[k+2] = rndValue;
				k=k+3;
				
				(**texPix)[l] = rndValue;
				l=l+1;
			}
			i = i+3;
			
		} else {
			rndValue = rand() % 100;
			if ( rndValue > rand_power) {
				rndValue = (lTexture0[i] + rndValue) % 255;
			} else {
				rndValue = lTexture0[i];
			}
			
			lTexture1[k] = rndValue;
			lTexture1[k+1] = rndValue;
			lTexture1[k+2] = rndValue;
			k=k+3;
	
			(**texPix)[l] = rndValue;
			i = i+1;			
			l=l+1;
		}
	}
	sglTexImage2Dubv(0L, SGL_BITMAP_RGB_NOT_TRANSPARENT, 80L, 60L, lTexture1, SGL_CLAMP);	
 }
void posIndex60(SGLint32 n, SGLfloat size, SGLfloat (*pos)[60UL]) {
	SGLuint32 i;
	for (i=0; i<n;i++) {
		(*pos)[i] = i * size/n;
	}
}

void posIndex80(SGLint32 n, SGLfloat size, SGLfloat (*pos)[80UL]) {
	SGLuint32 i;
	for (i=0; i<n;i++) {
		(*pos)[i] = i * size/n;
	}
}
