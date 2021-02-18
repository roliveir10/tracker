#ifndef TRACKER_H
# define TRACKER_H

# include "lib.h"
# include <string.h>
# include <stdlib.h>
# include <stdio.h>
# include <unistd.h>

# define DATAPERFILE		7
# define HISTORYPATH		"/Users/robinoliveira/Documents/Winamax Poker/accounts/malicious_/history/"
# define HISTORYTESTPATH	"/Users/robinoliveira/Desktop/history_test/"
# define NBRBUTTON		1

# define NBR_KEY		1

typedef enum			e_key
{
	CLICK
}				t_key;

typedef enum			e_btnName
{
	SYNC
}				t_btnName;

typedef struct			s_file
{
	char			*name;
	int			tableName;
	struct s_file		*next;
}				t_file;

typedef struct			s_hand
{
	int			takeInCents;
	struct s_hand		*next;
}				t_hand;

typedef struct			s_game
{
	int			tableName;
	char			playerName[32];
	int			tournamentId;
	int			buyIn;
	int			dayId;
	int			weekId;
	int			monthId;
	t_hand			*hand;
	struct s_game		*next;
}				t_game;

typedef struct			s_btn
{
	SDL_Rect		rect;
	SDL_Color		color;
	t_text			msg;
}				t_btn;

typedef struct			s_mouse
{
	double			deltaX;
	double			deltaY;
}				t_mouse;

typedef struct			s_env
{
	t_sdl			sdl;
	int			isRunning;
	t_game			*game;
	int			totalGames;
	t_btn			btn[NBRBUTTON];
	char			keyPress[NBR_KEY];
	t_mouse			mouse;
}				t_env;

void				runTracker(t_env *env);
void				keyHandler(t_env *env, SDL_Event *event);
int				draw(t_env *env);

// SORTING

int				sortFile(t_file **file);
void				synchro_file(t_env *env);

// READING

# define BUFF_SIZE		1024

int				getLine(const int fd, char **line);

// UI

int				initSyncButton(t_env *env);
void				drawBgLoadingBar(t_env *env);
void				drawLoadingBar(t_env *env, int currentLoad);
void				removeBgBar(t_env *env);
void				writeLoadingText(t_env *env, int totalF, int curF);

// LIBFT

char				*strdel(char **as);
char				*strjoin(char *s1, char *s2);
char				*strjoinf(char **s1, char *s2);
char				*strsub(char const *s, unsigned int start, size_t len);
char				*strnew(size_t size);
int				isidigit(char c);
int				isfdigit(char c);
int				atoiP(const char *str, int *i);
char				**strsplit(char const *s, char c);
void				delWordsTables(char ***tab);
int				countN(int n);
char				*itoa(int n);
#endif
