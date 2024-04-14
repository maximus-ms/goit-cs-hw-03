--Get all tasks of a specific user. Use SELECT to retrieve tasks by user_id.
select title, description, status_id
from tasks
where user_id = 5;

--Select tasks with a specific status. Use a subquery to select tasks with a specific status, for example, 'new'.
select title
from tasks
where status_id = (
	select id
	from status
	where name = 'new'
);

--Update the status of a specific task. Change the status of a specific task to 'in progress' or another status.
update tasks
set status_id = (
	select id
	from status
	where name = 'in progress'
)
where id = 72;

--Get a list of users who have no tasks at all. Use combination of SELECT, WHERE NOT IN and a subquery to get a list of users without tasks.
select *
from users
where id not in (
	select distinct user_id
	from tasks t
);
-- check results
select * from tasks where user_id = 4;

--Add a new task for a specific user. Use INSERT to add a new task.
insert into tasks (title, description, status_id, user_id)
values ('Custom task', 'It is manually added task for user #4', 1, 4);

--Get all tasks that are not yet completed. Select tasks where the status is not 'completed'.
select *
from tasks
where status_id != (
	select id
	from status
	where name = 'completed'
);

--Delete a specific task. Use DELETE to delete a task by its id.
delete from tasks
where id = 32;
-- check results
select * from tasks where id = 32;

--Find users with a specific email. Use SELECT with a LIKE condition to filter users by email.
select fullname
from users
where email like '%.net';

--Update a user's name. Change a user's name using UPDATE.
update users
set fullname = 'Котигорошко'
where id = 48;
-- check results
select * from users where id = 48;

--Get the number of tasks for each status. Use SELECT, COUNT, GROUP BY to group tasks by statuses.
select count(status_id)
from tasks
group by status_id;

--Get tasks assigned to users with a specific email domain. Use SELECT with a LIKE condition in combination with JOIN to select tasks assigned to users whose email contains a specific domain (for example, '%@example.com').
select u.fullname, u.email, title, status_id
from tasks
join users u on user_id = u.id
where email like '%@example.com';

--Get a list of tasks without a description. Select tasks where the description is missing.
select *
from tasks
where description is null;

--Get users and their tasks that are in progress. Use INNER JOIN to get a list of users and their tasks with a specific status.
select u.fullname, t.title, t.status_id
from users u
join tasks t on user_id = u.id
where status_id = (
	select id
	from status
	where name = 'in progress'
);

--Get users and the number of their tasks. Use LEFT JOIN and GROUP BY to get a list of users and the number of their tasks.
select u.fullname, count(t.user_id) task_count
from users u
left join tasks t on user_id = u.id
group by u.fullname;
