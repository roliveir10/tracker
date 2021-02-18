#ifndef LIB_H
# define LIB_H

# include "SDL.h"
# include "SDL_ttf.h"

# define WIN_TITLE "Expresso Tracker"

typedef struct			s_text
{
	char			*str;
	SDL_Rect		pos;
	SDL_Color		fg_color;
	SDL_Color		bg_color;
	SDL_Surface		*texte;
	SDL_Texture		*texture;
	SDL_Renderer		*renderer;
	TTF_Font		*police;
}				t_text;

typedef struct			s_sdl
{
	SDL_Window		*window;
	int			h;
	int			w;
	unsigned int		wId;
	SDL_Renderer		*renderer;
	SDL_Texture		*texture;
	TTF_Font		*arial_black_14;
	TTF_Font		*arial_black_10;
	unsigned int		*image;
}				t_sdl;

#endif
