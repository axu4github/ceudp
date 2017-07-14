
## SQL测试语句

### 单表`select`语句

```sql
select * from tags

select * from ratings

select * from movies

select * from links

select * from genome_tags

select * from genome_scores
```

### 单表`select`语句带`where`条件

```sql
select * from tags where userid = '88738'

select * from ratings where userid = '88738'

select * from movies where genres like '%Drama%' # 显示有问题

select * from links where movieid = '131250'

select * from genome_tags where tag in ('1920s', '1930s', '1950s')

select * from genome_scores where relevance > 0.1 and relevance < 0.2 # 需要添加FLOAT字段 # FLOAT显示位数
```

### 单表`select`语句带`limit`条件

```sql
select * from tags where userid = '88738' limit 20
```

### 单表`select`语句带`group by`条件

```sql
select movieid, count(*) as count from tags where userid = '88738' group by movieid

select movieid, count(*) as count from ratings where userid = '88738' group by movieid

select genres, count(*) as count from movies where genres like '%Drama%' group by genres # 显示有问题

select movieid, count(*) as count from links where movieid = '131250' group by movieid

select tag, count(*) as count from genome_tags where tag in ('1920s', '1930s', '1950s') group by tag

select movieid, count(*) as count from genome_scores where relevance > 0.1 and relevance < 0.2 group by movieid # 需要添加FLOAT字段 # FLOAT显示位数
```

### 单表`select`语句带`order by`条件

```sql
select movieid, count(*) as count from tags where userid = '88738' group by movieid order by count desc

select movieid, count(*) as count from ratings where userid = '88738' group by movieid order by count desc

select genres, count(*) as count from movies where genres like '%Drama%' group by genres order by count # 显示有问题 # 默认是升序

select movieid, count(*) as count from links where movieid = '131250' group by movieid

select tag, count(*) as count from genome_tags where tag in ('1920s', '1930s', '1950s') group by tag order by count asc

# Top5
select movieid, count(*) as count from genome_scores where relevance > 0.1 and relevance < 0.2 group by movieid order by count desc limit 5 # 需要添加FLOAT字段 # FLOAT显示位数
```

### 双表`select`语句带`where`条件

```sql
# Exception in thread "broadcast-exchange-6" java.lang.OutOfMemoryError: GC overhead limit exceeded
# select * from genome_scores as s, genome_tags as t where t.tagid = s.tagid
# 大表放在前面的效率会快很多

select * from genome_scores as s, genome_tags as t where t.tagid = s.tagid

select * from genome_scores as s, genome_tags as t where t.tagid = s.tagid and t.tag in ('1920s', '1930s', '1950s') and s.relevance > 0.1 and s.relevance < 0.2

# select * from genome_scores as s left join genome_tags as t on t.tagid = s.tagid

# select t.userid, t.movieid, r.rating from tags as t left join ratings as r on r.userid = t.userid

select * from ratings as r, tags as t where r.userid = t.userid and r.movieid = t.movieid 

select * from movies as m, links as l where m.movieid = l.movieid and m.genres like '%Romance%'
```

### 双表`select`语句带`limit`条件

```sql
select * from genome_scores as s, genome_tags as t where t.tagid = s.tagid limit 20

select * from genome_scores as s, genome_tags as t where t.tagid = s.tagid and t.tag in ('1920s', '1930s', '1950s') and s.relevance > 0.1 and s.relevance < 0.2 limit 20

select * from ratings as r, tags as t where r.userid = t.userid and r.movieid = t.movieid limit 20

select * from movies as m, links as l where m.movieid = l.movieid and m.genres like '%Romance%' limit 20
```

### 双表`select`语句带`group by`条件

```sql
select s.tagid, count(*) as count from genome_scores as s, genome_tags as t where t.tagid = s.tagid group by s.tagid

select s.tagid, count(*) as count from genome_scores as s, genome_tags as t where t.tagid = s.tagid and t.tag in ('1920s', '1930s', '1950s') and s.relevance > 0.1 and s.relevance < 0.2 group by s.tagid

# slow 20s+
select t.userid, count(*) as count from ratings as r, tags as t where r.userid = t.userid and r.movieid = t.movieid group by t.userid

select m.genres, count(*) as count from movies as m, links as l where m.movieid = l.movieid and m.genres like '%Romance%' group by m.genres
```

### 双表`select`语句带`order by`条件

```sql
select s.tagid, count(*) as count from genome_scores as s, genome_tags as t where t.tagid = s.tagid group by s.tagid order by count desc

select s.tagid, count(*) as count from genome_scores as s, genome_tags as t where t.tagid = s.tagid and t.tag in ('1920s', '1930s', '1950s') and s.relevance > 0.1 and s.relevance < 0.2 group by s.tagid order by count desc

# slow 20s+
select t.userid, count(*) as count from ratings as r, tags as t where r.userid = t.userid and r.movieid = t.movieid group by t.userid order by count desc

select m.genres, count(*) as count from movies as m, links as l where m.movieid = l.movieid and m.genres like '%Romance%' group by m.genres order by count desc 
```

### 双表`select`语句带`join`条件

```sql
select s.tagid, count(*) as count from genome_scores as s left join genome_tags as t on t.tagid = s.tagid group by s.tagid order by count desc

select s.tagid, count(*) as count from genome_scores as s left join genome_tags as t on t.tagid = s.tagid and t.tag in ('1920s', '1930s', '1950s') and s.relevance > 0.1 and s.relevance < 0.2 group by s.tagid order by count desc

# slow 20s+
select t.userid, count(*) as count from ratings as r left join tags as t on r.userid = t.userid and r.movieid = t.movieid group by t.userid order by count desc limit 5

select m.genres, count(*) as count from movies as m left join links as l on m.movieid = l.movieid and m.genres like '%Romance%' group by m.genres order by count desc
```


### 级联表`select`语句带`join`条件

```sql
select r.movieid, m.title, m.genres, r.count from (select movieid, count(*) as count from ratings where rating > 4 group by movieid order by count desc) as r left join movies as m on r.movieid = m.movieid

select * from (select * from genome_scores where relevance > 0.1 and relevance < 0.2) as s, genome_tags as t, movies as m where s.tagid = t.tagid and s.movieid = m.movieid

select s.movieid, count(*) as count from (select * from genome_scores where relevance > 0.1 and relevance < 0.2) as s, genome_tags as t, movies as m where s.tagid = t.tagid and s.movieid = m.movieid group by s.movieid order by count desc
```

### 物化视图表`select`语句带`where`条件

```sql
# 创建表名: "ratings_and_tags"
# 物化视图SQL语句:
# select r.userid, r.movieid, r.rating, r.timestamp as r_times, t.tag, t.timestamp as t_times from ratings as r, tags as t where r.userid = t.userid and r.movieid = t.movieid 

select * from ratings_and_tags
```

### 物化视图表`select`语句带`limit`条件

```sql
select * from ratings_and_tags limit 20
```

### 物化视图表`select`语句带`group by`条件

```sql
select userid, movieid, count(*) as count from ratings_and_tags group by userid, movieid
```

### 物化视图表`select`语句带`order by`条件

```sql
select userid, movieid, count(*) as count from ratings_and_tags group by userid, movieid order by count desc
```

### 物化视图表`select`语句带`join`条件

```sql
select * from (select userid, movieid, count(*) as count from ratings_and_tags group by userid, movieid order by count desc) as rt left join movies as m on rt.movieid = m.movieid
```
