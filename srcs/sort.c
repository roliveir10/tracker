#include "tracker.h"

static int		findIndexMin(int *tabT, int length, int start)
{
	int		min;
	int		index;
	int		i;

	min = tabT[start];
	i = start;
	index = start;
	while (i < length)
	{
		if (tabT[i] <= min)
		{
			min = tabT[i];
			index = i;
		}
		i++;
	}
	return (index);
}

static int		totalFile(t_file *file)
{
	int		totalF = 0;

	while (file)
	{
		totalF++;
		file = file->next;
	}
	return (totalF);
}
static void		convertLstToTab(t_file *file, int **tableName, char ***name)
{
	int		*tmpTableName = *tableName;
	char		**tmpName = *name;

	while (file)
	{
		**tableName = file->tableName;
		**name = file->name;
		file = file->next;
		*tableName += 1;
		*name += 1;
	}
	*tableName = tmpTableName;
	*name = tmpName;
}

static void		convertTabToLst(t_file **file, int *tabTableName, char **tabName)
{
	t_file		*tmp = *file;
	int		i = 0;

	while (*file)
	{
		(*file)->name = tabName[i];
		(*file)->tableName = tabTableName[i];
		*file = (*file)->next;
		i++;
	}
	*file = tmp;
}

int			sortFile(t_file **file)
{
	int		*tabTableName;
	char		**tabName;
	int		totalF = 0;
	int		i = 0;
	int		min;
	int		swapInt;
	char		*swapName;

	totalF = totalFile(*file);
	if (totalF == 0)
		return (totalF);
	tabTableName = (int*)malloc(sizeof(int) * totalF);
	tabName = (char**)malloc(sizeof(char*) * totalF);

	convertLstToTab(*file, &tabTableName, &tabName);

	while (i < totalF)
	{
		min = findIndexMin(tabTableName, totalF, i);
		swapInt = tabTableName[i];
		swapName = tabName[i];
		tabTableName[i] = tabTableName[min];
		tabName[i] = tabName[min];
		tabTableName[min] = swapInt;
		tabName[min] = swapName;
		i++;
	}

	convertTabToLst(file, tabTableName, tabName);

	free(tabTableName);
	free(tabName);
	return (totalF);
}
