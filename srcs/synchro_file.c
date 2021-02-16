#include <dirent.h>
#include "tracker.h"

static int		parsTableName(char *str)
{
	int		i = 0;
	int		tableName = 0;

	while (str[i] && str[i] != '(')
		i++;
	if (str[i])
		tableName = atoi(&str[i + 1]);
	return (tableName);
}

void			print_file(void)
{
	DIR		*dir;
	struct dirent	*ent;
	t_file		*file = NULL;
	t_file		*tmp = NULL;
	int		id;

	if ((dir = opendir("/Users/oliviernachin/Documents/Winamax Poker/")) != NULL)
	{
		while ((ent = readdir(dir)) != NULL)
		{
			id = parsTableName(ent->d_name);
			if (id && !file)
			{
				file = (t_file*)malloc(sizeof(t_file));
				file->tournamentId = id;
				file->name = strdup(ent->d_name);
				tmp = file;
			}
			else if (id)
			{
				file->next = (t_file*)malloc(sizeof(t_file));
				file->next->tournamentId = id;
				file->next->name = strdup(ent->d_name);
				file = file->next;
			}
		}
		closedir(dir);
	}
	else
	{
		printf("Cannot open history files\n");
		return ; // return TODO
	}
	file = tmp;
	sortFile(&file);
	while (file)
	{
		printf("%s\n", file->name);
		file = file->next;
	}
	file = tmp;
}
