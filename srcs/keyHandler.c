#include "tracker.h"

static void		mouseButtonDown(t_env *env, SDL_Event *event)
{
	if (event->button.button == SDL_BUTTON_LEFT)
		env->keyPress[CLICK] = 0;
}

static void		mouseButtonUp(t_env *env, SDL_Event *event)
{
	if (event->button.button == SDL_BUTTON_LEFT)
		env->keyPress[CLICK] = 1;
}

static void		mouseMotion(t_env *env, SDL_Event *event)
{
	env->mouse.deltaX = event->button.x;
	env->mouse.deltaY = event->button.y;
}

void			keyHandler(t_env *env, SDL_Event *event)
{
	if (event->type == SDL_MOUSEBUTTONDOWN)
		mouseButtonDown(env, event);
	if (event->type == SDL_MOUSEBUTTONUP)
		mouseButtonUp(env, event);
	if (event->type == SDL_MOUSEMOTION)
		mouseMotion(env, event);
}
