#include <stdlib.h>
#include <string.h>

char			*strdel(char **as)
{
	if (as)
	{
		free(*as);
		*as = NULL;
	}
	return (NULL);
}

char			*strjoin(char *s1, char *s2)
{
	char		*ms;

	if (!s1 || !s2)
		return (NULL);
	ms = (char*)malloc(sizeof(char) * (strlen(s1) + strlen(s2) + 1));
	strcpy(ms, s1);
	strcat(ms, s2);
	return (ms);
}

char			*strjoinf(char **s1, char *s2)
{
	char		*line;

	line = strjoin(*s1, s2);
	strdel(s1);
	return (line);
}

char			*strsub(char const *s, unsigned int start, size_t len)
{
	size_t		i;
	char		*ms;

	i = 0;
	if (!s)
		return (NULL);
	ms = (char*)malloc(sizeof(char) * (len - i + 1));
	while (i < len)
	{
		ms[i] = s[i + start];
		i++;
	}
	ms[i] = '\0';
	return (ms);
}

char			*strnew(size_t size)
{
	char		*mem;

	mem = (char*)malloc(size + 1);
	bzero(mem, size);
	mem[size] = '\0';
	return (mem);
}

int			isidigit(char c)
{
	return (c >= '0' && c <= '9');
}

int			isfdigit(char c)
{
	return ((c >= '0' && c <= '9') || c == '.');
}

int			atoiP(const char *str, int *i)
{
	unsigned char	*mstr;
	int		isNeg;
	int		final;

	mstr = (unsigned char*)str;
	final = 0;
	isNeg = 1;
	while ((mstr[*i] >= 9 && mstr[*i] <= 13) || mstr[*i] == 32)
		(*i)++;
	if (mstr[*i] == '-')
		isNeg = -1;
	if (mstr[*i] == '-' || mstr[*i] == '+')
		(*i)++;
	while (mstr[*i] >= '0' && mstr[*i] <= '9')
	{
		final *= 10;
		final += (mstr[*i] - '0');
		(*i)++;
	}
	return (isNeg * final);
}

static int		l(const char *s, int i, char c)
{
	int		b;

	b = 0;
	while (s[i] != c && s[i] != '\t' && s[i])
	{
		b++;
		i++;
	}
	return (b);
}

static int		wo(const char *s, char c)
{
	int		i = 0;
	int		count = 0;

	while (s[i])
	{
		while ((s[i] == c || s[i] == '\t') && s[i])
			i++;
		if (s[i] != c && s[i] != '\t' && s[i])
		{
			while (s[i] != c && s[i] != '\t' && s[i])
				i++;
			count++;
		}
	}
	return (count);
}

char			**strsplit(char const *s, char c)
{
	int		i = 0;
	int		j = 0;
	int		y;
	char		**t;

	if (!s)
		return (NULL);
	t = (char**)malloc(sizeof(char*) * (wo(s, c) + 1));
	while (s[i])
	{
		while ((s[i] == c || s[i] == '\t') && s[i])
			i++;
		if (s[i])
		{
			y = 0;
			t[j] = (char*)malloc(sizeof(char) * l(s, i, c) + 1);
			while (s[i] != c && s[i] != '\t' && s[i])
				t[j][y++] = s[i++];
			t[j++][y] = '\0';
		}
	}
	t[j] = 0;
	return (t);
}

void			delWordsTables(char ***tab)
{
	char		**tmp;

	if (!tab || !*tab)
		return ;
	tmp = *tab;
	while (**tab)
	{
		strdel(*tab);
		*tab += 1;
	}
	free(tmp);
	tmp = NULL;
}

int			countN(int nbr)
{
	unsigned int	val;
	int		count;

	count = 0;
	if (nbr < 0)
		val = -nbr;
	else
		val = nbr;
	if (!val || nbr < 0)
		count++;
	while (val)
	{
		val = val / 10;
		count++;
	}
	return (count);
}

char			*itoa(int n)
{
	char		*tab;
	unsigned int	m;
	int		k;

	k = countN(n);
	m = n < 0 ? -n : n;
	tab = (char*)malloc(sizeof(char) * k + 1);
	tab[k] = '\0';
	while (k)
	{
		k--;
		tab[k] = m % 10 + '0';
		m = m / 10;
	}
	if (n < 0)
		tab[k] = '-';
	return (tab);
}	
