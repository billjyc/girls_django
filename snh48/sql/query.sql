select * from `memberinfo`;

-- 每场公演的上场成员
insert into `member_performance_history` (`member_id`, `performance_history_id`) values
(10081, 384), (10082, 384), (10083, 384), (10084, 384), (10087, 384), (10088, 384),
(10089, 384), (10090, 384), (10091, 384), (10093, 384), (10096, 384), (10110, 384),
(10126, 384), (10164, 384), (10167, 384), (10006, 384), (10063, 384), (10067, 384),
(10181, 384), (10182, 384), (10185, 384), (10186, 384), (10187, 384), (10188, 384),
(10189, 384), (10191, 384), (10192, 384), (10193, 384), (10194, 384), (10195, 384),
(10196, 384), (10197, 384), (10198, 384);

insert into `member_performance_history_tmp` (`member_id`, `performance_history_id`) values
(10081, 384), (10082, 384), (10083, 384), (10084, 384), (10087, 384), (10088, 384),
(10089, 384), (10090, 384), (10091, 384), (10093, 384), (10096, 384), (10110, 384),
(10126, 384), (10164, 384), (10167, 384), (10006, 384), (10063, 384), (10067, 384),
(10181, 384), (10182, 384), (10185, 384), (10186, 384), (10187, 384), (10188, 384),
(10189, 384), (10191, 384), (10192, 384), (10193, 384), (10194, 384), (10195, 384),
(10196, 384), (10197, 384), (10198, 384);


-- 每场unit的表演者
-- X 命运的X号
insert into `unit_history` (`performance_history_id`, `unit_id`, `member_id`, `rank`) values
(384, 1, 10087, 1), (384, 2, 10093, 1), (384, 2, 10088, 2), (384, 2, 10164, 3), (384, 3, 10087, 1),
(384, 3, 10089, 2), (384, 3, 10082, 3), (384, 4, 10084, 1), (384, 4, 10096, 2), (384, 4, 10081, 3),
(384, 5, 10091, 1), (384, 5, 10089, 2), (384, 6, 10090, 1), (384, 6, 10083, 2), (384, 6, 10081, 3),
(384, 6, 10126, 4);

-- SII 第48区
insert into `unit_history` (`performance_history_id`, `unit_id`, `member_id`, `rank`) values
(354, 13, 10014, 1), (354, 13, 10006, 2), (354, 14, 10008, 1), (354, 14, 10017, 2), (354, 14, 10001, 3),
(354, 14, 10073, 4), (354, 15, 10003, 1), (354, 15, 10015, 2), (354, 16, 10005, 1), (354, 16, 10002, 2),
(354, 16, 10010, 3), (354, 17, 10019, 1), (354, 17, 10013, 2), (354, 17, 10016, 3), (354, 17, 10004, 4),
(354, 18, 10007, 1);

-- NII 以爱之名
insert into `unit_history` (`performance_history_id`, `unit_id`, `member_id`, `rank`) values
(382, 7, 10023, 1), (382, 7, 10026, 2), (382, 7, 10178, 3), (382, 8, 10037, 1), (382, 8, 10063, 2),
(382, 8, 10020, 3), (382, 8, 10021, 4), (382, 9, 10030, 1), (382, 9, 10036, 2), (382, 10, 10054, 1),
(382, 10, 10076, 2), (382, 11, 10067, 1), (382, 11, 10141, 2), (382, 11, 10156, 3), (382, 11, 10177, 4),
(382, 12, 10025, 1), (382, 24, 10171, 1), (382, 24, 10178, 2);

-- Ft 梦想的旗帜
insert into `unit_history` (`performance_history_id`, `unit_id`, `member_id`, `rank`) values
(384, 19, 10191, 1), (384, 19, 10198, 2), (384, 19, 10194, 3), (384, 20, 10192, 1), (384, 20, 10188, 2),
(384, 20, 10186, 3), (384, 20, 10196, 4), (384, 21, 10006, 1), (384, 21, 10081, 2), (384, 21, 10063, 3),
(384, 22, 10067, 1), (384, 22, 10195, 2), (384, 22, 10197, 3), (384, 22, 10189, 4), (384, 23, 10193, 1),
(384, 23, 10187, 2);

-- 新增公演
insert into `performance_history` (`performance_id`, `date`, `description`) values
(9, '2018-04-18 19:30', ''), (14, '2018-04-19 19:30', ''),
(14, '2018-04-20 19:30', ''), (8, '2018-04-21 14:00', '蒋芸生日主题公演'),
(11, '2018-04-21 19:00', '出道三周年特殊公演'), (8, '2018-04-22 14:00', '徐子轩生日主题公演'),
(15, '2018-04-22 19:00', '袁一琦生日主题公演');

-- unit阵容
select mi.id, mi.name, p.name, ph.date, u.name, uh.rank from memberinfo mi, performance p, performance_history ph, unit u, unit_history uh where mi.id = uh.`member_id` and p.id = u.`performance_id` and uh.`unit_id` = u.id and p.id = ph.`performance_id` and uh.`performance_history_id` = ph.id order by uh.`performance_history_id`, u.id, uh.rank;

-- 每场公演的人数
select count(ph.id) as co, mph.`member_id`, ph.date, p.name from `member_performance_history` mph, `performance_history` ph, `performance` p where p.`id`=ph.`performance_id` and p.team=5
and ph.id=mph.`performance_history_id` group by ph.id;

-- 各队平均年龄
select mi.team, team.name,  avg((year(now())-year(birthday)-1) + ( DATE_FORMAT(birthday, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )) as age
from memberinfo mi, team where is_valid=1 and mi.team = team.id
group by team;

-- 各期平均年龄
select batch, avg((year(now())-year(birthday)-1) + ( DATE_FORMAT(birthday, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )) as age
 from memberinfo where team <> 6 and is_valid = 1 group by `batch`;
 