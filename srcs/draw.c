#include "tracker.h"

static t_text		getTextInfo(t_env *env, int pSize)
{
	t_text		msg;

	msg.renderer = env->sdl.renderer;
	msg.pos.x = 0;
	msg.pos.y = 0;
	msg.pos.w = env->sdl.w;
	msg.pos.h = env->sdl.h;
	if (pSize == 10)
		msg.police = env->sdl.arial_black_10;
	else
		msg.police = env->sdl.arial_black_14;
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
	return (1);
	setRgbaText(&msg->bg_color, 0x0);
	setRgbaText(&msg->fg_color, 0xffffff);
	msg->pos.x = 290;
	msg->pos.y = 180;
	msg->str = strdup("Games played");
	if (!writeText(msg))
	{
		free(msg->str);
		return (0);
	}
	free(msg->str);
	return (1);
}

void			writeLoadingText(t_env *env, int totalF, int curF)
{
	t_text		msg;
	char		*toJoin;

	msg = getTextInfo(env, 14);
	setRgbaText(&msg.bg_color, 0x0);
	setRgbaText(&msg.fg_color, 0xffffff);
	msg.pos.x = 865;
	msg.pos.y = 75;

	msg.str = itoa(curF);
	toJoin = itoa(totalF);
	msg.str = strjoinf(&msg.str, "/");
	msg.str = strjoinf(&msg.str, toJoin);
	strdel(&toJoin);
	writeText(&msg);
	strdel(&msg.str);
}

static void		drawBar(t_sdl sdl, SDL_Rect *bar, int color)
{
	SDL_SetRenderTarget(sdl.renderer, sdl.texture);
	SDL_SetRenderDrawColor(sdl.renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
	if (color)
		SDL_SetRenderDrawColor(sdl.renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);

	SDL_RenderFillRect(sdl.renderer, bar);
	SDL_SetRenderTarget(sdl.renderer, NULL);
	SDL_RenderCopy(sdl.renderer, sdl.texture, NULL, NULL);
}

void			drawBgLoadingBar(t_env *env)
{
	SDL_Rect	bgBar;

	bgBar.x = 300;
	bgBar.y = 80;
	bgBar.w = 560;
	bgBar.h = 10;
	drawBar(env->sdl, &bgBar, 0);
}

void			drawLoadingBar(t_env *env, int currentLoad)
{
	SDL_Rect	ldBar;

	ldBar.x = 301;
	ldBar.y = 81;
	ldBar.w = currentLoad * 0.01 * 558;
	ldBar.h = 8;
	drawBar(env->sdl, &ldBar, 1);
}

void			removeBgBar(t_env *env)
{
	SDL_Rect	bar;

	bar.x = 280;
	bar.y = 80;
	bar.w = 600;
	bar.h = 10;
	drawBar(env->sdl, &bar, 1);
}

int			draw(t_env *env)
{
	t_text		msg;
	
	msg = getTextInfo(env, 14);
	drawText(&msg);
	SDL_RenderCopy(env->sdl.renderer, env->sdl.texture, NULL, NULL);
	SDL_RenderPresent(env->sdl.renderer);
	return (1);
}
