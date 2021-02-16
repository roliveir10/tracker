#include <stdlib.h>
#include <strings.h>
#include "tracker.h"

void			delenv(t_sdl *sdl)
{
	if (sdl->texture)
		SDL_DestroyTexture(sdl->texture);
	if (sdl->renderer)
		SDL_DestroyRenderer(sdl->renderer);
	if (sdl->window)
		SDL_DestroyWindow(sdl->window);
	SDL_Quit();
	exit(1);
}

static int		initLib(t_sdl *sdl)
{
	if (SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		dprintf(2, "SDL_Init failed. Aborting...\n");
		return (0);
	}
	if (!(sdl->window = SDL_CreateWindow(WIN_TITLE, SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED, 1200, 900, 0)))
	{
		dprintf(2, "SDL_CreateWindow failed. Aborting...\n");
		return (0);
	}
	SDL_GetWindowSize(sdl->window, &sdl->w, &sdl->h);
	sdl->wId = SDL_GetWindowID(sdl->window);
	if (!(sdl->renderer = SDL_CreateRenderer(sdl->window, -1,
			SDL_RENDERER_PRESENTVSYNC)))
	{
		dprintf(2, "SDL_CreateRenderer failed. Aborting...\n");
		return (0);
	}
	if (!(sdl->texture = SDL_CreateTexture(sdl->renderer,
			SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING,
			sdl->w, sdl->h)))
	{
		dprintf(2, "SDL_CreateTexture failed. Aborting...\n");
		return (0);
	}
	if (TTF_Init() == -1)
	{
		dprintf(2, "TTF_Init failed. Aborting...\n");
		return (0);
	}
	if (!(sdl->arial_black_20 = TTF_OpenFont("/Library/Fonts/Arial Unicode.ttf", 20)))
	{
		dprintf(2, "Invalid font. Aborting...\n");
		return (0);
	}
	return (1);
}

int			main(void)
{
	t_env		env;
	int		ret;

	bzero(&env, sizeof(t_env));
	ret = initLib(&env.sdl);
	if (!ret)
		return (1);
	ret = draw(&env);
	if (!ret)
		return (1);
	print_file();
	runTracker(&env);
	delenv(&env.sdl);
	return (0);
}
