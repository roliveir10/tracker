#include "tracker.h"

static t_text		getTextInfo(t_env *env)
{
	t_text		msg;

	msg.renderer = env->sdl.renderer;
	msg.pos.x = 0;
	msg.pos.y = 0;
	msg.pos.w = env->sdl.w;
	msg.pos.h = env->sdl.h;
	msg.police = env->sdl.arial_black_20;
	return (msg);
}

static void		setRgbaText(SDL_Color *color, int value)
{
	color->b = value % 256;
	value /= 256;
	color->g = value % 256;
	value /= 256;
	color->r = value % 256;
	value /= 256;
	color->a = 0;
}

static int		writeText(t_text *msg)
{
	if (!(msg->texte = TTF_RenderText_Shaded(msg->police, msg->str,
			msg->fg_color, msg->bg_color)))
		return (0);
	if (!(msg->texture = SDL_CreateTextureFromSurface(msg->renderer,
			msg->texte)))
		return (0);
	SDL_FreeSurface(msg->texte);
	if (SDL_QueryTexture(msg->texture, NULL, NULL,
			&msg->pos.w, &msg->pos.h) < 0)
	{
		SDL_DestroyTexture(msg->texture);
		return (0);
	}
	if (SDL_RenderCopy(msg->renderer, msg->texture, NULL, &msg->pos) < 0)
	{
		SDL_DestroyTexture(msg->texture);
		return (0);
	}
	SDL_DestroyTexture(msg->texture);
	return (1);
}

static int		drawText(t_text *msg)
{
	setRgbaText(&msg->bg_color, 0x0);
	setRgbaText(&msg->fg_color, 0xffffff);
	msg->pos.x = 100;
	msg->pos.y = 100;
	msg->str = strdup("Total games");
	if (!writeText(msg))
	{
		free(msg->str);
		return (0);
	}
	free(msg->str);
	return (1);
}

int			draw(t_env *env)
{
	t_text		msg;

	SDL_SetRenderDrawColor(env->sdl.renderer, 0, 0, 0, 255);
        SDL_RenderClear(env->sdl.renderer);
	msg = getTextInfo(env);
	if (!drawText(&msg))
	{
		dprintf(2, "Error drawing text\n");
		return (0);
	}

	SDL_RenderPresent(env->sdl.renderer);
	return (1);
}
