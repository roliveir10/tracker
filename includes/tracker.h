#ifndef TRACKER_H
# define TRACKER_H

# include "lib.h"
# include <string.h>
# include <stdlib.h>
# include <stdio.h>

typedef struct			s_file
{
	char			*name;
	int			tournamentId;
	struct s_file		*next;
}				t_file;

typedef struct			s_hand
{
	int			takeInCents;
	struct s_hand		*next;
}				t_hand;

typedef struct			s_game
{
	char			playerName[32];
	int			gameTypeId;
	int			tournamentId;
	int			buyIn;
	int			dayId;
	int			weekId;
	int			monthId;
	t_hand			*hand;
	struct s_game		*next;
}				t_game;

typedef struct			s_env
{
	t_sdl			sdl;
	int			isRunning;
}				t_env;

void				runTracker(t_env *env);
void				keyHandler(t_env *env, SDL_Event *event);
int				draw(t_env *env);
void				print_file(void);

// SORTING

void				sortFile(t_file **file);
#endif
