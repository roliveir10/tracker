#include "tracker.h"

int			initSyncButton(t_env *env)
{
	env->btn[SYNC].rect.x = 950;
	env->btn[SYNC].rect.y = 60;
	env->btn[SYNC].rect.h = 30;
	env->btn[SYNC].rect.w = 30;
	return (1);
}
