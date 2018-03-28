-- unit阵容
select mi.id, mi.name, p.name, ph.date, u.name, uh.rank from memberinfo mi, performance p, performance_history ph, unit u, unit_history uh where mi.id = uh.`member_id` and p.id = u.`performance_id` and uh.`unit_id` = u.id and p.id = ph.`performance_id` and uh.`performance_history_id` = ph.id order by uh.`performance_history_id`, u.id, uh.rank;

-- 每场公演的人数
select count(ph.id) as co, mph.`member_id`, ph.date, p.name from `member_performance_history` mph, `performance_history` ph, `performance` p where p.`id`=ph.`performance_id` and p.team=5
and ph.id=mph.`performance_history_id` group by ph.id;

-- 各队平均年龄
select mi.team, team.name,  avg((year(now())-year(birthday)-1) + ( DATE_FORMAT(birthday, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )) as age
from memberinfo mi, team where is_valid=1 and mi.team <> 6 and mi.team = team.id
group by team;

-- 各期平均年龄
select batch, avg((year(now())-year(birthday)-1) + ( DATE_FORMAT(birthday, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )) as age
 from memberinfo where team <> 6 and is_valid = 1 group by `batch`;