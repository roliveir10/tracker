#include <dirent.h>
#include <fcntl.h>
#include "tracker.h"

static char		*isExpresso(char *str)
{
	return (strstr(str, "Expresso"));
}

static char		*isRealMoney(char *str)
{
	return (strstr(str, "real"));
}

static char		*isSummaryFile(char *str)
{
	return (strstr(str, "summary"));
}

static int		getIdFromFileName(char *str)
{
	int		i = 0;
	int		tableName = 0;

	while (str[i] && str[i] != '(')
		i++;
	if (str[i])
		tableName = atoi(&str[i + 1]);
	return (tableName);
}

static int		getBuyIn(char *str)
{
	float		buyIn;
	float		rake;

	while (*str && !isdigit(*str))
		str++;
	buyIn = atof(str);
	while (*str && isfdigit(*str))
		str++;
	while (*str && !isdigit(*str))
		str++;
	rake = atof(str);
	return ((int)((rake + buyIn) * 100));
}

static void		getDateId(char *str, int *dayId, int *weekId, int *monthId)
{
	int		year;
	int		month;
	int		day;

	year = atoi(str + 19);
	month = atoi(str + 24);
	day = atoi(str + 27);

	*dayId = (year - 2020) * 365 + month * 30 + day;
	*weekId = (int)((*dayId) / 7);
	*monthId = (year - 2020) * 12 + month;
}

static void		getDataInFile(t_game **game, char *line)
{
	char		*tmp;

	tmp = strnstr(line, "Player : ", 9);
	if (tmp)
	{
		strcpy((*game)->playerName, tmp + 9);
		return ;
	}
	tmp = strnstr(line, "Buy-In : ", 9);
	if (tmp)
	{
		(*game)->buyIn = getBuyIn(tmp);
		return ;
	}
	tmp = strnstr(line, "Tournament started ", 19);
	if (tmp)
	{
		getDateId(tmp, &(*game)->dayId, &(*game)->weekId, &(*game)->monthId);
		return ;
	}
}

static int		isSaved(int id, t_game *game)
{
	while (game)
	{
		if (game->tableName == id)
			return (1);
		game = game->next;
	}
	return (0);
}

static void		freeFile(t_file **file)
{
	if (!*file)
		return ;
	freeFile(&(*file)->next);
	strdel(&(*file)->name);
	free(*file);
}

static void		createNewGame(t_game **game, t_game **tmp)
{
	if (!*game)
	{
		*game = (t_game*)malloc(sizeof(t_game));
		bzero(*game, sizeof(t_game));
		*tmp = *game;
		return ;
	}
	(*game)->next = (t_game*)malloc(sizeof(t_game));
	bzero((*game)->next, sizeof(t_game));
	*game = (*game)->next;
}

static void		synchroData(t_env *env, t_game **game, t_file *file, int *totalGames, int totalF)
{
	int		ret;
	int		fd;
	char		*line;
	t_game		*tmp;
	char		*currentPath;
	int		currentF = 0;

	tmp = *game;
	while (*game && (*game)->next)
		*game = (*game)->next;

	while (file)
	{
		if (!isSaved(file->tableName, tmp))
		{
			*totalGames += 1;
			createNewGame(game, &tmp);
			(*game)->tableName = file->tableName;
			(*game)->tournamentId = *totalGames;
		}
		currentPath = strjoin(HISTORYTESTPATH, file->name);
		fd = open(currentPath, O_RDONLY);
		if (fd > -1 && isSummaryFile(file->name))
		{
			while ((ret = getLine(fd, &line)) > 0)
			{
				getDataInFile(game, line);
				strdel(&line);
			}
		}
		file = file->next;
		close(fd);
		strdel(&currentPath);
		drawLoadingBar(env, currentF * 100 / totalF + 1);
		writeLoadingText(env, totalF, currentF);
		SDL_RenderPresent(env->sdl.renderer);
		currentF++;
	}
	*game = tmp;
}

void			saveDataInFile(t_game *game, int lastIdSaved)
{
	FILE		*file;

	file = fopen("history.dt", "a");
	while (game)
	{
		if (game->tableName > lastIdSaved)
			fprintf(file, "%d;%d;%s;%d;%d;%d;%d\n",
				game->tableName,
				game->tournamentId,
				game->playerName,
				game->buyIn,
				game->dayId,
				game->weekId,
				game->monthId);
		game = game->next;
	}
	fclose(file);
}

static int		getNbrData(char **data)
{
	int		i = 0;

	while (data[i])
		i++;
	return (i);
}

static void		fillGameStruct(t_game **game, char **data)
{
	(*game)->tableName = atoi(data[0]);
	(*game)->tournamentId = atoi(data[1]);
	strcpy((*game)->playerName, data[2]);
	(*game)->buyIn = atoi(data[3]);
	(*game)->dayId = atoi(data[4]);
	(*game)->weekId = atoi(data[5]);
	(*game)->monthId = atoi(data[6]);
}

void			getDataFromFile(t_game **game)
{
	int		fd;
	int		ret;
	char		*line;
	t_game		*tmp = *game;
	char		**data;
	int		nbrData;

	fd = open("history.dt", O_RDONLY);
	if (fd < 0)
		return ;
	while ((ret = getLine(fd, &line)) > 0)
	{
		data = strsplit(line, ';');
		nbrData = getNbrData(data);
		if (nbrData == DATAPERFILE && !isSaved(atoi(data[0]), tmp))
		{
			createNewGame(game, &tmp);
			fillGameStruct(game, data);
		}
		delWordsTables(&data);
		strdel(&line);
	}
	close(fd);
	*game = tmp;
}

static int		getLastIdSaved(t_game *game, int *totalGames)
{
	if (!game)
		return (0);
	while (game->next)
		game = game->next;
	*totalGames = game->tournamentId;
	return (game->tableName);
}

static void		createNewFile(t_file **file, t_file **tmp)
{
	if (!*file)
	{
		*file = (t_file*)malloc(sizeof(t_file));
		*tmp = *file;
		return ;
	}
	(*file)->next = (t_file*)malloc(sizeof(t_file));
	*file = (*file)->next;
}

void			synchro_file(t_env *env)
{
	DIR		*dir;
	struct dirent	*ent;
	t_file		*tmp = NULL;
	t_file		*file = NULL;
	int		id;
	int		lastIdSaved;
	int		totalF;

	getDataFromFile(&env->game);
	lastIdSaved = getLastIdSaved(env->game, &env->totalGames);
	dir = opendir(HISTORYTESTPATH);
	if (dir == NULL)
	{
		printf("Cannot open history files\n");
		return ;
	}
	while ((ent = readdir(dir)) != NULL)
	{
		if (isExpresso(ent->d_name) && isRealMoney(ent->d_name))
		{
			id = getIdFromFileName(ent->d_name);
			if (id > lastIdSaved)
			{
				createNewFile(&file, &tmp);
				file->tableName = id;
				file->name = strdup(ent->d_name);
				file->next = NULL;
			}
		}
	}
	closedir(dir);
	file = tmp;
	totalF = sortFile(&file);
	drawBgLoadingBar(env);
	synchroData(env, &env->game, file, &env->totalGames, totalF);
	freeFile(&file);
	saveDataInFile(env->game, lastIdSaved);
	removeBgBar(env);
	SDL_RenderPresent(env->sdl.renderer);
}
