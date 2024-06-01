-- ENVIRONMENT --

DROP KEYSPACE IF EXISTS basecast;
CREATE KEYSPACE basecast WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };
USE basecast;

-- TABLES --

-- Users --

DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id timeuuid,
	client_id timeuuid,
	email text,
	role int,
	PRIMARY KEY (user_id, client_id)
);

INSERT INTO users (user_id, client_id, email, role) VALUES (now(), 98c8ca6a-1a4a-11ef-8519-325096b39f47, 'pstevenson6@gmail.com', 1);

-- Assets --

DROP TABLE IF EXISTS assets;

CREATE TABLE assets (
	podcast_id timeuuid,
	asset_id timeuuid,
	medallion text,
	type text,
	uri text,
	filename text,
	PRIMARY KEY (podcast_id, asset_id)
);

INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09e8b6-1a41-11ef-87d6-325096b39f47, 'gold', 'thumb', 'https://mcdn.podbean.com/mf/web/gtvdj9/logo3000x3000.png', 'logo3000x3000.png');
INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09ea96-1a41-11ef-b40e-325096b39f47, 'gold', 'thumb', 'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg', 'Daniel_THUMB.jpg');
INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb04-1a41-11ef-ae03-325096b39f47, 'bronze', 'thumb', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Daniel - Podcast.png', 'Daniel - Podcast.png');
INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb54-1a41-11ef-a3d3-325096b39f47, 'bronze', 'audio', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Church intro.wav', 'Church intro.wav');
INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb9a-1a41-11ef-8ce7-325096b39f47, 'bronze', 'audio', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Outro_Jul23.wav', 'Outro_Jul23.wav');
-- INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 51761d06-1a46-11ef-ac81-325096b39f47, 'bronze', 'video', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Blacktown Anglican Livestream 5th May 2024 _ Daniel 1.mp4', 'Blacktown Anglican Livestream 5th May 2024 _ Daniel 1.mp4');
-- INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 51761f0e-1a46-11ef-a97e-325096b39f47, 'bronze', 'video', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Blacktown Anglican Livestream 12th May 2024 _ Daniel 2.mp4', 'Blacktown Anglican Livestream 12th May 2024 _ Daniel 2.mp4');
-- INSERT INTO assets (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 51761f7c-1a46-11ef-930c-325096b39f47, 'bronze', 'video', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Blacktown Anglican Livestream 19th May 2024 _ Daniel 3.mp4', 'Blacktown Anglican Livestream 19th May 2024 _ Daniel 3.mp4');

-- Episodes --

DROP TABLE IF EXISTS episodes;

CREATE TABLE episodes (
    episode_id timeuuid,
	podcast_id timeuuid,
	intro list<text>,
	outro list<text>,
    clips list<FROZEN<list<int>>>,
	title text,
	description text,
	status text,
	type text,
	logo text,
	bronze list<text>,
	silver list<text>,
	gold list<text>,
	PRIMARY KEY (episode_id)
);

-- INSERT INTO episodes (podcast_id, episode_id, intro, outro, bronze, clips, title, description, status, type, logo) VALUES (
--     98c8cd08-1a4a-11ef-a854-325096b39f47,
--     355f0094-1bbb-11ef-a1ca-325096b39f47,
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Church intro.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Outro_Jul23.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Blacktown Anglican Livestream 5th May 2024 _ Daniel 1.mp4'],
--     [[1602,3700]],
--     'Life in the King''s Service, Daniel 1',
--     '<p>We live stream every Sunday at 10 AM (AEDT). Join us here:</p><p><a href="https://www.youtube.com/blacktownanglican">www.youtube.com/blacktownanglican</a></p><p>Or find us online at: <a href="https://bac.org.au/">bac.org.au</a></p>',
--     'publish',
--     'public',
--     'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg'
-- );
-- INSERT INTO episodes (podcast_id, episode_id, intro, outro, bronze, clips, title, description, status, type, logo) VALUES (
--     98c8cd08-1a4a-11ef-a854-325096b39f47,
--     355f030a-1bbb-11ef-958a-325096b39f47,
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Church intro.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Outro_Jul23.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Blacktown Anglican Livestream 12th May 2024 _ Daniel 2.mp4'],
--     [[1660,3831]],
--     'The King''s Dream, Daniel 2',
--     '<p>We live stream every Sunday at 10 AM (AEDT). Join us here:</p><p><a href="https://www.youtube.com/blacktownanglican">www.youtube.com/blacktownanglican</a></p><p>Or find us online at: <a href="https://bac.org.au/">bac.org.au</a></p>',
--     'publish',
--     'public',
--     'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg'
-- );
-- INSERT INTO episodes (podcast_id, episode_id, intro, outro, bronze, clips, title, description, status, type, logo) VALUES (
--     98c8cd08-1a4a-11ef-a854-325096b39f47,
--     355f038c-1bbb-11ef-91d5-325096b39f47,
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Church intro.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Outro_Jul23.wav'],
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Blacktown Anglican Livestream 19th May 2024 _ Daniel 3.mp4'],
--     [[2358,4412]],
--     'The King''s Image, Daniel 3',
--     '<p>We live stream every Sunday at 10 AM (AEDT). Join us here:</p><p><a href="https://www.youtube.com/blacktownanglican">www.youtube.com/blacktownanglican</a></p><p>Or find us online at: <a href="https://bac.org.au/">bac.org.au</a></p>',
--     'draft',
--     'public',
--     'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg'
-- );

-- Driver --

DROP TABLE IF EXISTS driver;

CREATE TABLE driver (
	job_id timeuuid,
	trigger list<text>,
	operation list<text>,
	PRIMARY KEY (job_id)
);

-- INSERT INTO driver (job_id, trigger, operation) VALUES (
--     now(),
--     ['bronze', '98c8cd08-1a4a-11ef-a854-325096b39f47', 'Blacktown Anglican Livestream 19th May 2024 _ Daniel 3.mp4'],
--     ['python', 'gold_01_assemble.py', '355f038c-1bbb-11ef-91d5-325096b39f47']
-- );

-- Podcasts --

DROP TABLE IF EXISTS podcasts;

CREATE TABLE podcasts (
    podcast_id timeuuid,
	client_id timeuuid,
	host_id text,
	host_secret text,
	title text,
	description text,
	logo text,
	intro text,
	outro text,
	blurb text,
	episode_logo text,
	PRIMARY KEY (podcast_id)
);

INSERT INTO podcasts (client_id, podcast_id, host_id, host_secret, title, description, logo, intro, outro, blurb, episode_logo) VALUES (
	98c8ca6a-1a4a-11ef-8519-325096b39f47,
	98c8cd08-1a4a-11ef-a854-325096b39f47,
	'a0de6fd07c0b8e0a09c23',
	'c117551131f73345640c7',
	'Blacktown Anglican Church',
	'Welcome to Blacktown Anglican Church! This podcast includes weekly sermons delivered by our ministry team. You can also watch the service live stream every Sunday at 10 AM AEST on YouTube at https://www.youtube.com/@BlacktownAnglican. Visit our website https://bac.org.au/ to find out more about our church, ministries, mission, and vision.',
	'https://mcdn.podbean.com/mf/web/gtvdj9/logo3000x3000.png',
	'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Church intro.wav',
	'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Outro_Jul23.wav',
	'<p>We live stream every Sunday at 10 AM (AEDT). Join us here:</p><p><a href="https://www.youtube.com/blacktownanglican">www.youtube.com/blacktownanglican</a></p><p>Or find us online at: <a href="https://bac.org.au/">bac.org.au</a></p>',
	'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg'
);

-- Clients --

DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
	client_id timeuuid,
	name text,
	PRIMARY KEY (client_id)
);

INSERT INTO clients (client_id, name) VALUES (98c8ca6a-1a4a-11ef-8519-325096b39f47, 'Blacktown Anglican Church');
