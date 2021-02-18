#include "tracker.h"

static int	printline(int fd, char **stat, char **line)
{
	int		k;
	char	*tmp;

	k = 0;
	while (stat[fd][k] != '\n' && stat[fd][k])
		k++;
	if (stat[fd][k] == '\n')
	{
		*line = strsub(stat[fd], 0, k);
		if ((tmp = strdup(stat[fd] + k + 1)) == NULL)
			return (-1);
		free(stat[fd]);
		stat[fd] = tmp;
		if (stat[fd][0] == '\0')
			strdel(&stat[fd]);
	}
	else if (stat[fd][k] == '\0')
	{
		*line = strdup(stat[fd]);
		strdel(&stat[fd]);
	}
	return (1);
}

int			getLine(const int fd, char **line)
{
	static char	*stat[1023];
	char		buff[BUFF_SIZE + 1];
	int			ret;
	char		*tmp;

	if (fd < 0 || !line || BUFF_SIZE < 1)
		return (-1);
	while ((ret = read(fd, buff, BUFF_SIZE)) > 0)
	{
		if (!(stat[fd]))
			stat[fd] = strnew(1);
		buff[ret] = '\0';
		if ((tmp = strjoin(stat[fd], buff)) == NULL)
			return (-1);
		free(stat[fd]);
		stat[fd] = tmp;
		if (strchr(buff, '\n'))
			return (printline(fd, stat, line));
	}
	if (ret == -1)
		return (-1);
	else if (ret == 0 && stat[fd] == NULL)
		return (0);
	return (printline(fd, stat, line));
}
