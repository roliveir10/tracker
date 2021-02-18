#include "tracker.h"

static void		clickBtnEvent(t_env *env, int id)
{
	void		(*function[NBRBUTTON])(t_env *) = {synchro_file};
	int		lstBtn[NBRBUTTON] = {SYNC};
	int		i = 0;

	while (i < NBRBUTTON)
	{
		if (lstBtn[i] == id)
			function[i](env);
		i++;
	}
}

static void		update(t_env *env)
{
	int		x;
	int		y;
	int		i = 0;
	SDL_Rect	curRect;

	if (env->keyPress[CLICK])
	{
		x = env->mouse.deltaX;
		y = env->mouse.deltaY;
		while (i < NBRBUTTON)
		{
			curRect = env->btn[i].rect;
			if (x > curRect.x && x < curRect.x + curRect.w
				&& y > curRect.y && y < curRect.y + curRect.h)
			{
				clickBtnEvent(env, i);
				break ;
			}
			i++;
		}
		env->keyPress[CLICK] = 0;
	}
}

void			runTracker(t_env *env)
{
	SDL_Event	event;

	env->isRunning = 1;
	while (env->isRunning)
	{
		while (SDL_PollEvent(&event))
		{
			if (event.type == SDL_QUIT
				|| (event.type == SDL_KEYDOWN
					&& event.key.keysym.sym == SDLK_ESCAPE)
				|| (event.type == SDL_WINDOWEVENT
					&& event.window.event == SDL_WINDOWEVENT_CLOSE))
			{
				env->isRunning = 0;
				break ;
			}
			keyHandler(env, &event);
		}
		update(env);
	}
}
