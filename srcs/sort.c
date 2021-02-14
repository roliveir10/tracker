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

void			sortFile(t_file **file)
{
	t_file		*tmp;
	int		*tabTournamentId;
	char		**tabName;
	int		totalT;
	int		i;
	int		min;
	int		swapInt;
	char		*swapName;

	totalT = 0;
	i = 0;
	tmp = *file;
	while (*file)
	{
		totalT++;
		*file = (*file)->next;
	}
	*file = tmp;

	tabTournamentId = (int*)malloc(sizeof(int) * totalT);
	tabName = (char**)malloc(sizeof(char*) * totalT);

	while (*file)
	{
		tabTournamentId[i] = (*file)->tournamentId;
		tabName[i] = (*file)->name;
		*file = (*file)->next;
		i++;
	}
	*file = tmp;
	i = 0;
	while (i < totalT)
	{
		min = findIndexMin(tabTournamentId, totalT, i);
		swapInt = tabTournamentId[i];
		swapName = tabName[i];
		tabTournamentId[i] = tabTournamentId[min];
		tabName[i] = tabName[min];
		tabTournamentId[min] = swapInt;
		tabName[min] = swapName;
		i++;
	}
	i = 0;
	while (*file)
	{
		(*file)->name = tabName[i];
		(*file)->tournamentId = tabTournamentId[i];
		*file = (*file)->next;
		i++;
	}
	*file = tmp;
	free(tabTournamentId);
	free(tabName);
}
