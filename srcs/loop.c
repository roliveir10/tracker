#include "tracker.h"


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
	}
}
